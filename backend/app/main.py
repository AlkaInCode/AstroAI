from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, chat, charts, dasha, numerology, profiles, transits, vargas, yogas

app = FastAPI(title="AstroAI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profiles.router)
app.include_router(charts.router)
app.include_router(dasha.router)
app.include_router(yogas.router)
app.include_router(vargas.router)
app.include_router(transits.router)
app.include_router(numerology.router)
app.include_router(chat.router)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
