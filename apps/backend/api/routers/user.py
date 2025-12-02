from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from apps.backend.database import get_db, User # Assuming User model is in database.py
from apps.backend.services.auth import get_current_user, get_password_hash # Assuming auth functions are in auth.py

router = APIRouter()

class UserProfile(BaseModel):
    username: str
    email: str
    learning_preferences: Optional[str] = None
    hardware_software_background: Optional[str] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[str] = None
    learning_preferences: Optional[str] = None
    hardware_software_background: Optional[str] = None
    password: Optional[str] = None # For password change

@router.get("/profile", response_model=UserProfile)
async def read_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserProfile)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_update.email is not None and user_update.email != current_user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        current_user.email = user_update.email

    if user_update.learning_preferences is not None:
        current_user.learning_preferences = user_update.learning_preferences

    if user_update.hardware_software_background is not None:
        current_user.hardware_software_background = user_update.hardware_software_background

    if user_update.password is not None:
        current_user.hashed_password = get_password_hash(user_update.password)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
