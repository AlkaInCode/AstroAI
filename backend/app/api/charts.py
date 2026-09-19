import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.life_areas import build_life_areas
from app.api.deps import get_current_user, get_owned_profile
from app.astrology.factory import get_astrology_provider
from app.astrology.provider import BirthInput
from app.database.session import get_db
from app.models.chart import Chart
from app.models.user import User
from app.schemas.chart import ChartResponse

router = APIRouter(prefix="/profiles/{profile_id}/chart", tags=["charts"])


def _to_chart_response(chart: Chart) -> ChartResponse:
    planets = chart.planetary_data.get("planets", [])
    return ChartResponse(
        id=chart.id,
        birth_profile_id=chart.birth_profile_id,
        lagna=chart.lagna,
        lagna_degree=chart.lagna_degree,
        rashi=chart.rashi,
        ayanamsa=chart.ayanamsa,
        house_system=chart.house_system,
        calculation_provider=chart.calculation_provider,
        planetary_data=chart.planetary_data,
        life_areas=build_life_areas(chart.lagna, chart.rashi, planets),
        created_at=chart.created_at,
    )


@router.post("", response_model=ChartResponse, status_code=status.HTTP_201_CREATED)
def generate_chart(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChartResponse:
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
        lagna_degree=result.lagna_degree,
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
    return _to_chart_response(chart)


@router.get("", response_model=ChartResponse)
def get_latest_chart(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChartResponse:
    profile = get_owned_profile(db, profile_id, current_user)
    chart = (
        db.query(Chart)
        .filter(Chart.birth_profile_id == profile.id)
        .order_by(Chart.created_at.desc())
        .first()
    )
    if chart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No chart generated for this profile yet")
    return _to_chart_response(chart)
