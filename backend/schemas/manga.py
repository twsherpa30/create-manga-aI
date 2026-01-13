from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel


class MangaOptionsSchema(BaseModel):
    text: str
    node_id: Optional[int] = None


class MangaNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False


class CompleteMangaNodeResponse(MangaNodeBase):
    id: int
    options: List[MangaOptionsSchema] = []

    class Config:
        from_attributes = True


class MangaBase(BaseModel):
    title: str
    session_id: Optional[str] = None

    class Config:
        from_attributes = True


class CreateMangaRequest(BaseModel):
    theme: str


class CompleteMangaResponse(MangaBase):
    id: int
    created_at: datetime
    root_node: CompleteMangaNodeResponse
    all_nodes: Dict[int, CompleteMangaNodeResponse]
    class Config:
        from_attributes = True