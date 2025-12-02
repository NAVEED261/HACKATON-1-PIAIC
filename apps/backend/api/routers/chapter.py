from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from apps.backend.database import get_db, User # Assuming User model is in database.py
from apps.backend.services.auth import get_current_user # To get the authenticated user
from apps.backend.services.personalization import personalize_chapter_content # To personalize content
from apps.backend.services.translation import translate_chapter_content_to_urdu # To translate content

router = APIRouter()

class PersonalizeRequest(BaseModel):
    chapter_content: str

class PersonalizeResponse(BaseModel):
    personalized_content: str

class TranslateRequest(BaseModel):
    chapter_content: str

class TranslateResponse(BaseModel):
    translated_content: str

@router.post("/personalize", response_model=PersonalizeResponse)
async def personalize_chapter(
    request: PersonalizeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint to personalize chapter content based on the authenticated user's profile.
    """
    if not request.chapter_content:
        raise HTTPException(status_code=400, detail="Chapter content cannot be empty.")

    # The personalize_chapter_content function will use the user_profile from current_user
    personalized_content = personalize_chapter_content(current_user, request.chapter_content)

    if "An error occurred" in personalized_content:
        raise HTTPException(status_code=500, detail=personalized_content)

    return PersonalizeResponse(personalized_content=personalized_content)

@router.post("/translate", response_model=TranslateResponse)
async def translate_chapter(
    request: TranslateRequest,
    current_user: User = Depends(get_current_user) # Assuming translation might also be user-contextualized
):
    """
    Endpoint to translate chapter content to Urdu.
    """
    if not request.chapter_content:
        raise HTTPException(status_code=400, detail="Chapter content cannot be empty.")

    translated_content = translate_chapter_content_to_urdu(request.chapter_content)

    if "An error occurred" in translated_content:
        raise HTTPException(status_code=500, detail=translated_content)

    return TranslateResponse(translated_content=translated_content)
