import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.charts import generate_chart_for_profile
from app.api.deps import get_current_user, get_owned_profile
from app.api.numerology import generate_numerology_for_profile
from app.database.session import get_db
from app.models.birth_profile import BirthProfile
from app.models.chart import Chart
from app.models.numerology_result import NumerologyResult
from app.models.user import User
from app.schemas.birth_profile import BirthProfileCreate, BirthProfileResponse, BirthProfileUpdate

router = APIRouter(prefix="/profiles", tags=["profiles"])

# Editing any of these invalidates the cached chart -- it was fetched from the
# (expensive, rate-limited) astrology provider for the *old* birth details and
# would silently keep showing a wrong Kundli otherwise.
_CHART_FIELDS = {"dob", "birth_time", "latitude", "longitude", "timezone"}
# Numerology is derived from name + DOB only.
_NUMEROLOGY_FIELDS = {"full_name", "dob"}


@router.post("", response_model=BirthProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    payload: BirthProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BirthProfile:
    profile = BirthProfile(user_id=current_user.id, **payload.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("", response_model=list[BirthProfileResponse])
def list_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[BirthProfile]:
    return db.query(BirthProfile).filter(BirthProfile.user_id == current_user.id).all()


@router.get("/{profile_id}", response_model=BirthProfileResponse)
def get_profile_by_id(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BirthProfile:
    return get_owned_profile(db, profile_id, current_user)


@router.patch("/{profile_id}", response_model=BirthProfileResponse)
def update_profile(
    profile_id: uuid.UUID,
    payload: BirthProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BirthProfile:
    profile = get_owned_profile(db, profile_id, current_user)
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)

    changed_fields = updates.keys()

    if changed_fields & _CHART_FIELDS:
        db.query(Chart).filter(Chart.birth_profile_id == profile.id).delete()
        db.commit()
        generate_chart_for_profile(db, profile)

    if changed_fields & _NUMEROLOGY_FIELDS:
        db.query(NumerologyResult).filter(NumerologyResult.birth_profile_id == profile.id).delete()
        db.commit()
        generate_numerology_for_profile(db, profile)

    return profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    profile = get_owned_profile(db, profile_id, current_user)
    db.delete(profile)
    db.commit()
