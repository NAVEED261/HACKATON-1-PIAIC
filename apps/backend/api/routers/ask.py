from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
from ..services.rag import get_rag_answer # Relative import

router = APIRouter()

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest) -> AskResponse:
    """
    Endpoint to ask questions about the textbook content using the RAG pipeline.
    """
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    answer = get_rag_answer(request.question)
    return AskResponse(answer=answer)
