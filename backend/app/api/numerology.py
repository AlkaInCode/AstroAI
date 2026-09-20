import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.rag import search_numerology_knowledge
from app.api.deps import get_current_user, get_owned_profile
from app.database.session import get_db
from app.models.numerology_result import NumerologyResult
from app.models.user import User
from app.numerology.calculations import compute_numerology
from app.schemas.numerology import NumerologyNumberOut, NumerologyResponse

router = APIRouter(prefix="/profiles/{profile_id}/numerology", tags=["numerology"])


_MASTER_NUMBERS = {11, 22, 33}


def _knowledge_for(*queries: str) -> str:
    for query in queries:
        results = search_numerology_knowledge(query, top_k=1, allow_fallback=False)
        if results:
            return results[0]["content"]
    return ""


def _number_knowledge(number: int) -> str:
    # A number query must be exact ("master number 2" would otherwise wrongly
    # substring-match the "master number 22" topic) -- only ask for the
    # master-number topic when the number actually is one.
    query = f"master number {number}" if number in _MASTER_NUMBERS else f"number {number} meaning"
    return _knowledge_for(query)


def _to_response(result: NumerologyResult) -> NumerologyResponse:
    return NumerologyResponse(
        id=result.id,
        birth_profile_id=result.birth_profile_id,
        full_name_used=result.full_name_used,
        life_path=NumerologyNumberOut(number=result.life_path_number, knowledge=_number_knowledge(result.life_path_number)),
        expression=NumerologyNumberOut(number=result.expression_number, knowledge=_number_knowledge(result.expression_number)),
        soul_urge=NumerologyNumberOut(number=result.soul_urge_number, knowledge=_number_knowledge(result.soul_urge_number)),
        personality=NumerologyNumberOut(number=result.personality_number, knowledge=_number_knowledge(result.personality_number)),
        chaldean_destiny=NumerologyNumberOut(
            number=result.chaldean_destiny_number, knowledge=_number_knowledge(result.chaldean_destiny_number)
        ),
        created_at=result.created_at,
    )


def generate_numerology_for_profile(db: Session, profile) -> NumerologyResult:
    computed = compute_numerology(profile.full_name, profile.dob)
    result = NumerologyResult(
        birth_profile_id=profile.id,
        full_name_used=computed["full_name_used"],
        life_path_number=computed["life_path_number"],
        expression_number=computed["expression_number"],
        soul_urge_number=computed["soul_urge_number"],
        personality_number=computed["personality_number"],
        chaldean_destiny_number=computed["chaldean_destiny_number"],
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.post("", response_model=NumerologyResponse, status_code=status.HTTP_201_CREATED)
def generate_numerology(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NumerologyResponse:
    profile = get_owned_profile(db, profile_id, current_user)
    result = generate_numerology_for_profile(db, profile)
    return _to_response(result)


@router.get("", response_model=NumerologyResponse)
def get_latest_numerology(
    profile_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NumerologyResponse:
    profile = get_owned_profile(db, profile_id, current_user)
    result = (
        db.query(NumerologyResult)
        .filter(NumerologyResult.birth_profile_id == profile.id)
        .order_by(NumerologyResult.created_at.desc())
        .first()
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No numerology computed for this profile yet"
        )
    return _to_response(result)
