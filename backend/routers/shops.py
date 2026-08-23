from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter(
    prefix="/api/shops",
    tags=["shops"]
)

@router.post("/", response_model=schemas.Shop)
def create_shop(shop: schemas.ShopCreate, db: Session = Depends(database.get_db)):
    db_shop = models.Shop(**shop.dict())
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop

@router.get("/search", response_model=list[schemas.Shop])
def search_shops(query: str, db: Session = Depends(database.get_db)):
    return db.query(models.Shop).filter(models.Shop.name.ilike(f"%{query}%")).all()

@router.get("/{shop_id}/history")
def get_shop_history(shop_id: int, db: Session = Depends(database.get_db)):
    shop = db.query(models.Shop).filter(models.Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
        
    inspections = db.query(models.Inspection).filter(models.Inspection.shop_id == shop_id).all()
    complaints = db.query(models.Complaint).filter(models.Complaint.shop_id == shop_id).all()
    
    return {
        "shop": {
            "id": shop.id,
            "name": shop.name,
            "address": shop.address
        },
        "inspections": [
            {
                "date": insp.date_logged,
                "is_compliant": insp.is_compliant,
                "details": insp.violation_details
            }
            for insp in inspections
        ],
        "resolved_complaints": [
            {
                "tracking_id": comp.tracking_id,
                "date": comp.date_filed,
                "violation_type": comp.violation_type
            }
            for comp in complaints if comp.status == "Resolved"
        ]
    }
