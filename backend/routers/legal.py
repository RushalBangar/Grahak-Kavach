from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import database, models
from typing import List

router = APIRouter(
    prefix="/api/legal-metrology",
    tags=["Legal Metrology"]
)

@router.get("/")
def get_documents(db: Session = Depends(database.get_db)):
    docs = db.query(models.LegalMetrologyDocument).all()
    return docs
