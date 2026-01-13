import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from schemas import manga
from db.database import SessionLocal, get_db
from models.manga import Manga, MangaNode
from models.job import MangaJob
from schemas.manga import CompleteMangaNodeResponse, CreateMangaRequest, CompleteMangaResponse
from schemas.job import MangaJobResponse
from core.manga_generator import MangaGenerator



router = APIRouter(
    prefix="/mangas",
    tags=["mangas"]
)

def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


@router.post("/create", response_model=MangaJobResponse)
def create_manga(
        request: CreateMangaRequest,
        background_tasks: BackgroundTasks,
        response: Response,
        session_id: str = Depends(get_session_id),
        db: Session = Depends(get_db)
):
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = str(uuid.uuid4())

    job = MangaJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status="pending"
    )
    db.add(job)
    db.commit()

    background_tasks.add_task(
        generate_manga_task,
        job_id=job_id,
        theme=request.theme,
        session_id=session_id
    )

    return job

def generate_manga_task(job_id: str, theme: str, session_id: str):
    db = SessionLocal()
    
    try:
        job = db.query(MangaJob).filter(MangaJob.job_id == job_id).first()
        if not job:
            return

        try:
            job.status = "processing"
            db.commit()

            manga = MangaGenerator.generate_manga(db, session_id, theme)

            job.manga_id = manga.id 
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()
    finally:
        db.close()

@router.get("/{manga_id}/complete", response_model=CompleteMangaResponse)
def get_complete_manga(manga_id: int, db: Session = Depends(get_db)):
    manga = db.query(Manga).filter(Manga.id == manga_id).first()
    if not manga:
        raise HTTPException(status_code=404, detail="Manga not found")
    complete_manga = build_complete_manga_tree(db, manga)
    return complete_manga


def build_complete_manga_tree(db: Session, manga: Manga) -> CompleteMangaResponse:
    nodes = db.query(MangaNode).filter(MangaNode.manga_id == manga.id).all()

    node_dict = {}
    for node in nodes:
        node_response = CompleteMangaNodeResponse(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_winning_ending=node.is_winning_ending,
            options=node.options
        )
        node_dict[node.id] = node_response

    root_node = next((node for node in nodes if node.is_root), None)
    if not root_node:
        raise HTTPException(status_code=500, detail="Root node not found")
    
    return CompleteMangaResponse(
        id=manga.id,
        title= manga.title,
        session_id=manga.session_id,
        created_at=manga.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict
    )