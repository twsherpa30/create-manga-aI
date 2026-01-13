from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from models.job import MangaJob
from schemas.job import MangaJobResponse

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)


@router.get("/{job_id}", response_model=MangaJobResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(MangaJob).filter(MangaJob.job_id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job