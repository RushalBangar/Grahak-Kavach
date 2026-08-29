from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="officer") # officer, admin

class Shop(Base):
    __tablename__ = "shops"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    inspections = relationship("Inspection", back_populates="shop")
    complaints = relationship("Complaint", back_populates="shop")

class Inspection(Base):
    __tablename__ = "inspections"
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), index=True)
    product_scanned = Column(String)
    is_compliant = Column(Boolean, default=True)
    violation_details = Column(String, nullable=True)
    date_logged = Column(DateTime, default=datetime.datetime.utcnow)
    officer_id = Column(Integer, ForeignKey("users.id"), index=True)
    
    shop = relationship("Shop", back_populates="inspections")
    officer = relationship("User")

class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String, unique=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), index=True)
    product_details = Column(String)
    violation_type = Column(String) # "Legal Metrology", "Food Safety", "Both"
    status = Column(String, default="Pending", index=True) # Pending, Verified, Routed, Resolved
    routed_to = Column(String, nullable=True) # "DCA", "FSSAI", "Both"
    user_email = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    evidence_url = Column(String, nullable=True)
    verification_method = Column(String) # Aadhaar QR, DigiLocker, PAN, etc.
    is_verified = Column(Boolean, default=False)
    date_filed = Column(DateTime, default=datetime.datetime.utcnow)
    
    shop = relationship("Shop", back_populates="complaints")

class OTPRequest(Base):
    __tablename__ = "otp_requests"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    otp_code = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_used = Column(Boolean, default=False)

class LegalMetrologyDocument(Base):
    __tablename__ = "legal_metrology_documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String)
    category = Column(String, index=True)
