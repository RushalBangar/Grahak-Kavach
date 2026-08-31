from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import models, schemas, database, auth
import uuid
from websocket_manager import manager

import smtplib
import random
import os
from email.mime.text import MIMEText
from typing import Dict
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/api/complaints",
    tags=["complaints"]
)

# In-memory store for OTPs: { "email": {"otp": "123456", "expires_at": datetime} }
# Note: For production, this should be stored in the database.
otp_store: Dict[str, dict] = {}

def send_email_smtp(to_email: str, subject: str, body: str):
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    
    if not smtp_user or not smtp_pass:
        print(f"SMTP Credentials missing. Logging email instead:\nTo: {to_email}\nSub: {subject}\nBody:\n{body}")
        return

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = f"Grahak Kavach <{smtp_user}>"
    msg['To'] = to_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        print(f"Successfully sent email to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")

@router.post("/send-verification")
def send_verification(req: schemas.ComplaintVerificationSend):
    email = req.identifier.strip().lower()
    otp_code = str(random.randint(100000, 999999))
    
    # Store OTP with a 10 minute expiration
    otp_store[email] = {
        "otp": otp_code,
        "expires_at": datetime.now() + timedelta(minutes=10)
    }
    
    body = f"Your verification code for filing a complaint on Grahak Kavach is: {otp_code}\n\nThis code will expire in 10 minutes."
    send_email_smtp(email, "Grahak Kavach - Complaint Verification Code", body)
    
    return {"message": f"Verification code sent to {email}"}

@router.post("/verify")
def verify_verification(req: schemas.ComplaintVerificationVerify):
    email = req.identifier.strip().lower()
    
    record = otp_store.get(email)
    if not record:
        raise HTTPException(status_code=400, detail="No OTP requested for this email.")
        
    if datetime.now() > record["expires_at"]:
        del otp_store[email]
        raise HTTPException(status_code=400, detail="OTP has expired. Please request a new one.")
        
    if req.otp == record["otp"]:
        # Success! Remove it so it can't be reused
        del otp_store[email]
        return {"success": True, "message": "Identity verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid verification code")


@router.post("/", response_model=schemas.Complaint, dependencies=[Depends(auth.verify_api_signature), Depends(auth.verify_captcha)])
def create_complaint(complaint: schemas.ComplaintCreate, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    # Look up or create the shop
    shop = db.query(models.Shop).filter(models.Shop.name.ilike(complaint.shop_name)).first()
    if not shop:
        shop = models.Shop(name=complaint.shop_name, address="Unknown location (auto-created)")
        db.add(shop)
        db.commit()
        db.refresh(shop)

    # Auto-routing logic based on violation type
    routed_to = None
    if complaint.violation_type == "Legal Metrology":
        routed_to = "DCA"
    elif complaint.violation_type == "Food Safety":
        routed_to = "FSSAI"
    elif complaint.violation_type == "Both":
        routed_to = "Both"
        
    # Extract dict but exclude shop_name, and add shop_id
    complaint_data = complaint.dict()
    complaint_data.pop("shop_name", None)
    
    db_complaint = models.Complaint(
        **complaint_data,
        shop_id=shop.id,
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
        def send_complaint_ack(email: str, tracking_id: str):
            subject = f"Complaint Received - Tracking ID: {tracking_id}"
            body = f"Thank you for submitting your complaint via Grahak Kavach.\n\nYour complaint has been successfully received and verified.\nYour Tracking ID is: {tracking_id}\n\nYou can track the status of your complaint on the Grahak Kavach portal.\n\nAppropriate actions will be taken shortly."
            send_email_smtp(email, subject, body)
        
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
