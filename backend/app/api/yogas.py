import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.rag import search_astrology_knowledge
from app.ai.tools import get_yogas
from app.api.deps import get_current_user, get_owned_profile
from app.database.session import get_db
from app.models.user import User
from app.schemas.yoga import YogaListResponse, YogaOut

router = APIRouter(prefix="/profiles/{profile_id}/yogas", tags=["yogas"])


@router.get("", response_model=YogaListResponse)
def get_yogas_for_profile(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> YogaListResponse:
    get_owned_profile(db, profile_id, current_user)

    result = get_yogas(db, profile_id)
    if "error" in result:
        detail = "No chart generated for this profile yet" if result["error"] == "chart_not_found" else result["error"]
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    yogas = []
    for yoga in result["yogas"]:
        knowledge_results = search_astrology_knowledge(yoga["name"], top_k=1, allow_fallback=False)
        knowledge = knowledge_results[0]["content"] if knowledge_results else ""
        yogas.append(YogaOut(**yoga, knowledge=knowledge))

    return YogaListResponse(yogas=yogas)
