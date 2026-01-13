from sqlalchemy.orm import Session

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.models import MangaLLMResponse, MangaNodeLLM
from core.models import MangaLLMResponse
from core.prompts import MANGA_STORY_PROMPT
from models.manga import Manga, MangaNode

from dotenv import load_dotenv
import os

load_dotenv()
class MangaGenerator:

    @classmethod
    def _get_llm(cls):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        return ChatOpenAI(
            model="gpt-4o-mini",
            openai_api_key=openai_api_key
        )
    
    @classmethod
    def generate_manga(cls, db: Session, session_id: str, theme: str = "fantasy")-> Manga:
        llm = cls._get_llm()
        manga_parser = PydanticOutputParser(pydantic_object=MangaLLMResponse)

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                MANGA_STORY_PROMPT
            ),
            (
                "human",
                f"Create the manga with this theme: {theme}"
            )
        ]).partial(format_instructions=manga_parser.get_format_instructions())

        raw_response = llm.invoke(prompt.invoke({}))

        response_text = raw_response
        if hasattr(raw_response, "content"):
            response_text = raw_response.content

        manga_structure = manga_parser.parse(response_text)

        manga_db = Manga(title=manga_structure.title, session_id=session_id)
        db.add(manga_db)
        db.flush()

        root_node_data = manga_structure.rootNode
        if isinstance(root_node_data, dict):
            root_node_data = MangaNodeLLM.model_validate(root_node_data)

        cls._process_manga_node(db, manga_db.id, root_node_data, is_root=True)
        db.commit()
        return manga_db
    
    @classmethod
    def _process_manga_node(cls, db: Session, manga_id: int, node_data: MangaNodeLLM, is_root: bool = False) -> MangaNode:
        node = MangaNode(
            manga_id=manga_id,
            content=node_data.content if hasattr(node_data, "content") else node_data["content"],
            is_root=is_root,
            is_ending=node_data.isEnding if hasattr(node_data, "isEnding") else node_data["isEnding"],
            is_winning_ending=node_data.isWinningEnding if hasattr(node_data, "isWinningEnding") else node_data["isWinningEnding"],
            options=[]
        )
        db.add(node)
        db.flush()

        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            options_list = []
            for option_data in node_data.options:
                next_node = option_data.nextNode

                if isinstance(next_node, dict):
                    next_node = MangaNodeLLM.model_validate(next_node)

                child_node = cls._process_manga_node(db, manga_id, next_node, False)

                options_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                })

            node.options = options_list

        db.flush()
        return node