from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import models, schemas, database, auth
import uuid
from websocket_manager import manager

router = APIRouter(
    prefix="/api/complaints",
    tags=["complaints"]
)

@router.post("/", response_model=schemas.Complaint, dependencies=[Depends(auth.verify_api_signature), Depends(auth.verify_captcha)])
def create_complaint(complaint: schemas.ComplaintCreate, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
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
    
    background_tasks.add_task(manager.broadcast, {"type": "NEW_COMPLAINT"})
    
    if complaint.user_email:
        # Mocking email send to user or using the same Google Script relay
        def send_complaint_ack(email: str, tracking_id: str):
            print(f"\n{'='*40}")
            print(f"📧 EMAIL SENT TO: {email}")
            print(f"SUBJECT: Complaint Received - Tracking ID: {tracking_id}")
            print(f"BODY: Thank you for submitting your complaint. We have received it and it will be reviewed soon. Appropriate actions will be taken.")
            print(f"{'='*40}\n")
            # If there's an actual email relay, we could hook it here.
        
        background_tasks.add_task(send_complaint_ack, complaint.user_email, db_complaint.tracking_id)
    
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
def update_complaint_status(tracking_id: str, update_data: schemas.ComplaintUpdate, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    db_complaint = db.query(models.Complaint).filter(models.Complaint.tracking_id == tracking_id).first()
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    if update_data.status:
        db_complaint.status = update_data.status
    
    # We could also save `notes` if we add a `notes` column to the Complaint model, 
    # but for the hackathon, updating the status is sufficient.
    
    db.commit()
    db.refresh(db_complaint)
    
    background_tasks.add_task(manager.broadcast, {"type": "STATUS_UPDATE", "tracking_id": tracking_id, "status": update_data.status})
    
    return db_complaint
