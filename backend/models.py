from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from .database import Base

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
    shop_id = Column(Integer, ForeignKey("shops.id"))
    product_scanned = Column(String)
    is_compliant = Column(Boolean, default=True)
    violation_details = Column(String, nullable=True)
    date_logged = Column(DateTime, default=datetime.datetime.utcnow)
    officer_id = Column(Integer, ForeignKey("users.id"))
    
    shop = relationship("Shop", back_populates="inspections")
    officer = relationship("User")

class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String, unique=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"))
    product_details = Column(String)
    violation_type = Column(String) # "Legal Metrology", "Food Safety", "Both"
    status = Column(String, default="Pending") # Pending, Verified, Routed, Resolved
    routed_to = Column(String, nullable=True) # "DCA", "FSSAI", "Both"
    evidence_url = Column(String, nullable=True)
    verification_method = Column(String) # Aadhaar QR, DigiLocker, PAN, etc.
    is_verified = Column(Boolean, default=False)
    date_filed = Column(DateTime, default=datetime.datetime.utcnow)
    
    shop = relationship("Shop", back_populates="complaints")
