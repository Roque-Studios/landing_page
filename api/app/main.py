import structlog
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from .config import settings
from .logger import setup_logging
from .database import get_db, engine, Base
from . import models
from .schemas import LeadCreate, LeadResponse
from .email import notify_new_lead

setup_logging()
logger = structlog.get_logger()

app = FastAPI(title="Roque Studios — leads API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

if settings.SENTRY_DSN:
    import sentry_sdk

    sentry_sdk.init(dsn=settings.SENTRY_DSN, environment=settings.ENVIRONMENT, traces_sample_rate=1.0)


@app.on_event("startup")
def on_startup():
    # Single small table — Alembic would be overkill here.
    Base.metadata.create_all(bind=engine)
    logger.info("Startup complete")


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error("DB health check failed", error=str(e))
        db_status = "error"
    return {"status": "ok" if db_status == "ok" else "error", "db": db_status}


@app.post("/leads", response_model=LeadResponse)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    # Honeypot: silently accept without storing or emailing, so bots get no signal.
    if payload.sitio_web:
        logger.info("Dropped honeypot submission")
        return LeadResponse(status="ok")

    lead = models.Lead(
        nombre=payload.nombre,
        negocio=payload.negocio,
        tipo=models.LeadTipo(payload.tipo),
        mensaje=payload.mensaje,
        contacto=payload.contacto,
        encontraste=payload.encontraste,
        utm_source=payload.utm_source,
        utm_medium=payload.utm_medium,
        utm_campaign=payload.utm_campaign,
        ref=payload.ref,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    logger.info("Lead stored", lead_id=str(lead.id), tipo=lead.tipo.value)

    notify_new_lead(lead)

    return LeadResponse(status="ok")
