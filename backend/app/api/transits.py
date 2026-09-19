import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.ai.rag import search_astrology_knowledge
from app.ai.tools import get_transits
from app.api.deps import get_current_user, get_owned_profile
from app.database.session import get_db
from app.models.user import User
from app.schemas.transit import TransitResponse

router = APIRouter(prefix="/profiles/{profile_id}/transits", tags=["transits"])


@router.get("", response_model=TransitResponse)
def get_transits_for_profile(
    profile_id: uuid.UUID,
    as_of: date | None = Query(default=None, description="Defaults to today"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransitResponse:
    get_owned_profile(db, profile_id, current_user)

    result = get_transits(db, profile_id, as_of=as_of)
    if "error" in result:
        detail = "No chart generated for this profile yet" if result["error"] == "chart_not_found" else result["error"]
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    for transit in result["transits"]:
        knowledge_results = search_astrology_knowledge(f"{transit['name']} transit", top_k=1, allow_fallback=False)
        transit["knowledge"] = knowledge_results[0]["content"] if knowledge_results else ""

    return TransitResponse(**result)
