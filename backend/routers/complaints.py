from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
import uuid

router = APIRouter(
    prefix="/api/complaints",
    tags=["complaints"]
)

@router.post("/", response_model=schemas.Complaint)
def create_complaint(complaint: schemas.ComplaintCreate, db: Session = Depends(database.get_db)):
    # Auto-routing logic based on violation type
    routed_to = None
    if complaint.violation_type == "Legal Metrology":
        routed_to = "DCA"
    elif complaint.violation_type == "Food Safety":
        routed_to = "FSSAI"
    elif complaint.violation_type == "Both":
        routed_to = "Both"
        
    db_complaint = models.Complaint(
        **complaint.dict(),
        tracking_id=str(uuid.uuid4())[:8].upper(),
        routed_to=routed_to,
        status="Verified" if complaint.verification_method != "None" else "Pending",
        is_verified=complaint.verification_method != "None"
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

@router.get("/queue", response_model=list[schemas.ComplaintWithShop])
def get_complaints_queue(db: Session = Depends(database.get_db)):
    # Note: For hackathon simplicity, we are returning all complaints. 
    # In production, this should be protected by the auth dependency:
    # current_user: models.User = Depends(auth.get_current_user)
    return db.query(models.Complaint).order_by(models.Complaint.date_filed.desc()).all()

@router.get("/{tracking_id}", response_model=schemas.Complaint)
def get_complaint(tracking_id: str, db: Session = Depends(database.get_db)):
    db_complaint = db.query(models.Complaint).filter(models.Complaint.tracking_id == tracking_id).first()
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return db_complaint

@router.patch("/{tracking_id}", response_model=schemas.Complaint)
def update_complaint_status(tracking_id: str, update_data: schemas.ComplaintUpdate, db: Session = Depends(database.get_db)):
    db_complaint = db.query(models.Complaint).filter(models.Complaint.tracking_id == tracking_id).first()
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    if update_data.status:
        db_complaint.status = update_data.status
    
    # We could also save `notes` if we add a `notes` column to the Complaint model, 
    # but for the hackathon, updating the status is sufficient.
    
    db.commit()
    db.refresh(db_complaint)
    return db_complaint
