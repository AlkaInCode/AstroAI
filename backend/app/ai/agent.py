"""
The AI agent: understands the question, pulls chart facts via tools, pulls
knowledge via RAG, and asks the LLM to explain -- never the other way around.

Phase 1 keeps tool selection simple (always fetch profile + chart, then
search knowledge using the raw question) rather than a full function-calling
loop. Phase 8 is where this grows into a true multi-step tool-using agent.
"""

import uuid

from sqlalchemy.orm import Session

from app.ai.llm import get_llm_client
from app.ai.prompts import SYSTEM_PROMPT, build_user_context_block
from app.ai.rag import search_astrology_knowledge
from app.ai.tools import get_chart, get_dasha, get_profile
from app.models.conversation import Conversation


def answer_question(db: Session, birth_profile_id: uuid.UUID, session_id: uuid.UUID, question: str) -> str:
    profile = get_profile(db, birth_profile_id)
    chart = get_chart(db, birth_profile_id)
    dasha = get_dasha(db, birth_profile_id)
    knowledge = search_astrology_knowledge(question)

    context_block = build_user_context_block(profile, chart, knowledge, dasha)
    llm = get_llm_client()
    reply = llm.complete(system_prompt=SYSTEM_PROMPT, user_message=f"{context_block}\nCustomer question: {question}")

    db.add(Conversation(birth_profile_id=birth_profile_id, session_id=session_id, role="user", message=question))
    db.add(Conversation(birth_profile_id=birth_profile_id, session_id=session_id, role="assistant", message=reply))
    db.commit()

    return reply
