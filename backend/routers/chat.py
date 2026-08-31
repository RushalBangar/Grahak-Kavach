from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas, database
from database import get_db

router = APIRouter(
    prefix="/api/chat",
    tags=["chat"]
)

@router.post("/", response_model=dict)
def chat_endpoint(query: schemas.ChatQuery, db: Session = Depends(get_db)):
    message = query.message.lower()
    
    # Fetch all rules from database
    rules = db.query(models.ChatRule).all()
    
    # Basic keyword matching
    for rule in rules:
        keywords = [k.strip().lower() for k in rule.keywords.split(",")]
        for kw in keywords:
            if kw and kw in message:
                return {"response": rule.response_text}
                
    # Fallback
    return {"response": "I can help you with rules regarding MRP, Expiry Dates, Net Quantity, or how to file a complaint. Could you rephrase your question?"}
