from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Union
from datetime import timedelta

from apps.backend.database import get_db, User # Assuming User model is in database.py
from apps.backend.services.auth import get_password_hash, verify_password, create_access_token # Assuming auth functions are in auth.py

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    learning_preferences: Optional[str] = None
    hardware_software_background: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        learning_preferences=user.learning_preferences,
        hardware_software_background=user.hardware_software_background
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/signin", response_model=Token)
async def signin(user_login: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user_login.username).first()
    if not db_user or not verify_password(user_login.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
