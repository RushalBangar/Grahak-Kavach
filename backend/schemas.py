from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ShopBase(BaseModel):
    name: str
    address: str

class ShopCreate(ShopBase):
    pass

class Shop(ShopBase):
    id: int

    class Config:
        from_attributes = True

class InspectionBase(BaseModel):
    shop_id: int
    product_scanned: str
    is_compliant: bool
    violation_details: Optional[str] = None

class InspectionCreate(InspectionBase):
    pass

class Inspection(InspectionBase):
    id: int
    date_logged: datetime
    officer_id: int

    class Config:
        from_attributes = True

class ComplaintBase(BaseModel):
    shop_name: str
    product_details: str
    violation_type: str
    verification_method: str
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    evidence_url: Optional[str] = None

class ComplaintCreate(ComplaintBase):
    pass

class Complaint(ComplaintBase):
    id: int
    shop_id: int
    tracking_id: str
    status: str
    routed_to: Optional[str] = None
    is_verified: bool
    date_filed: datetime

    class Config:
        from_attributes = True

class ComplaintWithShop(Complaint):
    shop: Shop

    class Config:
        from_attributes = True

class ComplaintUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None

class ScanResult(BaseModel):
    extracted_text: str
    legal_metrology: dict # e.g. {"is_compliant": True, "details": "MRP, quantity present"}
    food_safety: dict # e.g. {"health_score": "B", "harmful_ingredients": []}

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class SendOTPRequest(BaseModel):
    email: str

class VerifyOTPRequest(BaseModel):
    email: str
    otp: str

class ComplaintVerificationSend(BaseModel):
    method: str
    identifier: str

class ComplaintVerificationVerify(BaseModel):
    method: str
    identifier: str
    otp: str

class ChatQuery(BaseModel):
    message: str

class ChatRule(BaseModel):
    id: int
    keywords: str
    response_text: str

    class Config:
        from_attributes = True
