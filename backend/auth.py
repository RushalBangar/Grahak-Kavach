from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import database, models, schemas

# Secret key to encode the JWT token (in a real app, load this from an env variable)
SECRET_KEY = "super_secret_hackathon_key_do_not_use_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/officer/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

import hmac
import hashlib
import time
import os
import json
import urllib.request
import urllib.parse
from fastapi import Header, Request

API_SECRET_KEY = os.getenv("API_SECRET_KEY", "default_dev_secret")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY", "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe")

def verify_api_signature(x_app_timestamp: str = Header(...), x_app_signature: str = Header(...)):
    try:
        ts = int(x_app_timestamp)
        now = int(time.time() * 1000)
        if abs(now - ts) > 5 * 60 * 1000:
            raise HTTPException(status_code=403, detail="Request expired")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp")
        
    expected_signature = hmac.new(
        API_SECRET_KEY.encode('utf-8'),
        x_app_timestamp.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(expected_signature, x_app_signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

async def verify_captcha(x_captcha_token: str = Header(...)):
    if not x_captcha_token:
        raise HTTPException(status_code=400, detail="Missing CAPTCHA token")
        
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = urllib.parse.urlencode({
        "secret": RECAPTCHA_SECRET_KEY,
        "response": x_captcha_token
    }).encode('utf-8')
    
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            if not result.get("success"):
                raise HTTPException(status_code=403, detail="CAPTCHA verification failed")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="CAPTCHA service error")
