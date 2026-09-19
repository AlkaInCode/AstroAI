import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ai.agent import answer_question
from app.api.deps import get_current_user, get_owned_profile
from app.database.session import get_db
from app.models.conversation import Conversation
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse, ConversationMessage

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def send_message(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatResponse:
    get_owned_profile(db, payload.birth_profile_id, current_user)

    session_id = payload.session_id or uuid.uuid4()
    reply = answer_question(db, payload.birth_profile_id, session_id, payload.message)
    return ChatResponse(session_id=session_id, reply=reply)


@router.get("/{profile_id}/history", response_model=list[ConversationMessage])
def get_history(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Conversation]:
    get_owned_profile(db, profile_id, current_user)
    return (
        db.query(Conversation)
        .filter(Conversation.birth_profile_id == profile_id)
        .order_by(Conversation.created_at.asc())
        .all()
    )
