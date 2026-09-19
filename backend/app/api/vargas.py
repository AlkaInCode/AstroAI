import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.tools import get_varga_chart
from app.api.deps import get_current_user, get_owned_profile
from app.astrology.vargas import VARGA_REGISTRY
from app.database.session import get_db
from app.models.user import User
from app.schemas.varga import VargaChartResponse, VargaListResponse

router = APIRouter(prefix="/profiles/{profile_id}/vargas", tags=["vargas"])


@router.get("", response_model=VargaListResponse)
def list_available_vargas() -> VargaListResponse:
    return VargaListResponse(
        available=[
            {"key": v.key, "label": v.label, "significance": v.significance} for v in VARGA_REGISTRY.values()
        ]
    )


@router.get("/{varga_key}", response_model=VargaChartResponse)
def get_varga(
    profile_id: uuid.UUID,
    varga_key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> VargaChartResponse:
    get_owned_profile(db, profile_id, current_user)

    result = get_varga_chart(db, profile_id, varga_key)
    if "error" in result:
        status_code = (
            status.HTTP_404_NOT_FOUND if result["error"] in ("chart_not_found", "unknown_varga") else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=result.get("detail", result["error"]))

    return VargaChartResponse(**result)
