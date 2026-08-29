from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import models, schemas, database, auth

router = APIRouter(
    prefix="/api/officer",
    tags=["officer"]
)

import random
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

# --- Native Email OTP Logic ---

import urllib.request
import json

def send_email(to_email: str, otp: str):
    script_url = os.getenv("GOOGLE_SCRIPT_URL")

    print(f"\n{'='*40}")
    print(f"🔒 OTP LOGGED FOR: {to_email}")
    print(f"🔑 YOUR LOGIN OTP IS: {otp}")
    print(f"{'='*40}\n")

    if script_url:
        try:
            data = json.dumps({"email": to_email, "otp": otp}).encode('utf-8')
            req = urllib.request.Request(
                script_url, 
                data=data, 
                headers={'Content-Type': 'application/json'}
            )
            response = urllib.request.urlopen(req, timeout=10)
            print("Successfully relayed email request to Google Apps Script")
        except Exception as e:
            print(f"Failed to relay email: {e}")

ALLOWED_OFFICER_EMAILS = [
    "ghotekarabhay0@gmail.com",
    "vaishnavilokhande671@gmail.com",
    "duyantinchaudhari@gmail.com",
    "rushikeshwagh2501@gmail.com",
    "sanskarmuthe186@gmail.com",
    "rushalbangar19@gmail.com"
]

@router.post("/send-otp")
def send_otp(request: schemas.SendOTPRequest, db: Session = Depends(database.get_db)):
    if request.email not in ALLOWED_OFFICER_EMAILS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not authorized for officer access.")
    
    # 1. Generate 6-digit OTP
    otp_code = str(random.randint(100000, 999999))
    
    # 2. Save to database
    db_otp = models.OTPRequest(email=request.email, otp_code=otp_code)
    db.add(db_otp)
    db.commit()

    # 3. Send email (or print to console)
    send_email(request.email, otp_code)
    
    return {"message": "OTP sent successfully"}

@router.post("/verify-otp", response_model=schemas.Token)
def verify_otp(request: schemas.VerifyOTPRequest, db: Session = Depends(database.get_db)):
    # 1. Check if OTP is valid and not used
    db_otp = db.query(models.OTPRequest).filter(
        models.OTPRequest.email == request.email,
        models.OTPRequest.otp_code == request.otp,
        models.OTPRequest.is_used == False
    ).order_by(models.OTPRequest.created_at.desc()).first()

    if not db_otp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired OTP")
    
    # 2. Mark OTP as used
    db_otp.is_used = True
    
    # 3. Ensure a User exists for this email (auto-create if not)
    # In a real app you'd strictly control this. For the hackathon, we allow auto-creation.
    user = db.query(models.User).filter(models.User.username == request.email).first()
    if not user:
        # Create a placeholder user
        hashed_pw = auth.get_password_hash("placeholder")
        user = models.User(username=request.email, hashed_password=hashed_pw, role="officer")
        db.add(user)
        db.commit()
        db.refresh(user)

    # 4. Generate Access Token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    if form_data.username not in ALLOWED_OFFICER_EMAILS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not authorized for officer access.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
@router.post("/inspections", response_model=schemas.Inspection)
def create_inspection(
    inspection: schemas.InspectionCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Verify shop exists
    shop = db.query(models.Shop).filter(models.Shop.id == inspection.shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
        
    db_inspection = models.Inspection(**inspection.dict(), officer_id=current_user.id)
    db.add(db_inspection)
    db.commit()
    db.refresh(db_inspection)
    return db_inspection

@router.get("/inspections", response_model=list[schemas.Inspection])
def get_inspections(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.Inspection).filter(models.Inspection.officer_id == current_user.id).all()
