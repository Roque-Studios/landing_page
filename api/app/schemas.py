from pydantic import BaseModel, Field


class LeadCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=200)
    negocio: str = Field(min_length=1, max_length=200)
    tipo: str = Field(pattern="^(negocio|agencia)$")
    mensaje: str = Field(min_length=1, max_length=5000)
    contacto: str = Field(min_length=1, max_length=200)
    encontraste: str | None = None
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_campaign: str | None = None
    ref: str | None = None
    # Honeypot — real visitors never fill this. Not persisted, only checked.
    sitio_web: str | None = None


class LeadResponse(BaseModel):
    status: str
