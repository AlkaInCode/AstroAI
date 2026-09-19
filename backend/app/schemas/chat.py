import uuid
from datetime import datetime

from pydantic import BaseModel


class ChatRequest(BaseModel):
    birth_profile_id: uuid.UUID
    session_id: uuid.UUID | None = None
    message: str


class ChatResponse(BaseModel):
    session_id: uuid.UUID
    reply: str


class ConversationMessage(BaseModel):
    role: str
    message: str
    created_at: datetime

    model_config = {"from_attributes": True}
