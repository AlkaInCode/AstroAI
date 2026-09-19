import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_owned_profile
from app.database.session import get_db
from app.models.birth_profile import BirthProfile
from app.models.user import User
from app.schemas.birth_profile import BirthProfileCreate, BirthProfileResponse

router = APIRouter(prefix="/profiles", tags=["profiles"])


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
