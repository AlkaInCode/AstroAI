from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.llm_settings import LLMSettingsResponse, LLMSettingsUpdate
from app.services.encryption import encrypt_secret

router = APIRouter(prefix="/settings/llm", tags=["settings"])


def _to_response(user: User) -> LLMSettingsResponse:
    return LLMSettingsResponse(
        provider=user.llm_provider,
        model=user.llm_model,
        has_api_key=bool(user.llm_api_key_encrypted),
    )


@router.get("", response_model=LLMSettingsResponse)
def get_llm_settings(current_user: User = Depends(get_current_user)) -> LLMSettingsResponse:
    return _to_response(current_user)


@router.put("", response_model=LLMSettingsResponse)
def update_llm_settings(
    payload: LLMSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LLMSettingsResponse:
    current_user.llm_provider = payload.provider
    current_user.llm_api_key_encrypted = encrypt_secret(payload.api_key)
    current_user.llm_model = payload.model
    db.commit()
    db.refresh(current_user)
    return _to_response(current_user)


@router.delete("", response_model=LLMSettingsResponse)
def clear_llm_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LLMSettingsResponse:
    current_user.llm_provider = None
    current_user.llm_api_key_encrypted = None
    current_user.llm_model = None
    db.commit()
    db.refresh(current_user)
    return _to_response(current_user)
