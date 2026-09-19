import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.tools import compute_dasha_for_profile
from app.api.deps import get_current_user, get_owned_profile
from app.database.session import get_db
from app.models.user import User
from app.schemas.dasha import DashaResponse

router = APIRouter(prefix="/profiles/{profile_id}/dasha", tags=["dasha"])


@router.get("", response_model=DashaResponse)
def get_dasha_timeline(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashaResponse:
    get_owned_profile(db, profile_id, current_user)

    result = compute_dasha_for_profile(db, profile_id)
    if "error" in result:
        detail = "No chart generated for this profile yet" if result["error"] == "chart_not_found" else result["error"]
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    return DashaResponse(**result)
