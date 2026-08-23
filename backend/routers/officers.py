from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import models, schemas, database, auth

router = APIRouter(
    prefix="/api/officer",
    tags=["officer"]
)

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
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
