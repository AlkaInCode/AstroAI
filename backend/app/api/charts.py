import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_owned_profile
from app.astrology.factory import get_astrology_provider
from app.astrology.provider import BirthInput
from app.database.session import get_db
from app.models.chart import Chart
from app.models.user import User
from app.schemas.chart import ChartResponse

router = APIRouter(prefix="/profiles/{profile_id}/chart", tags=["charts"])


@router.post("", response_model=ChartResponse, status_code=status.HTTP_201_CREATED)
def generate_chart(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Chart:
    profile = get_owned_profile(db, profile_id, current_user)

    provider = get_astrology_provider()
    result = provider.calculate_chart(
        BirthInput(
            dob=profile.dob,
            birth_time=profile.birth_time,
            latitude=profile.latitude,
            longitude=profile.longitude,
            timezone=profile.timezone,
        )
    )

    chart = Chart(
        birth_profile_id=profile.id,
        lagna=result.lagna,
        rashi=result.rashi,
        ayanamsa=result.ayanamsa,
        house_system=result.house_system,
        calculation_provider=provider.name,
        planetary_data={"planets": [p.__dict__ for p in result.planets]},
        raw_provider_response=result.raw_response,
    )
    db.add(chart)
    db.commit()
    db.refresh(chart)
    return chart


@router.get("", response_model=ChartResponse)
def get_latest_chart(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Chart:
    profile = get_owned_profile(db, profile_id, current_user)
    chart = (
        db.query(Chart)
        .filter(Chart.birth_profile_id == profile.id)
        .order_by(Chart.created_at.desc())
        .first()
    )
    if chart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No chart generated for this profile yet")
    return chart
