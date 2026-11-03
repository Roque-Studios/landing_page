import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from .database import Base


class LeadTipo(enum.Enum):
    negocio = "negocio"
    agencia = "agencia"


class Lead(Base):
    __tablename__ = "lead"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    negocio = Column(String, nullable=False)
    tipo = Column(SQLEnum(LeadTipo), nullable=False, default=LeadTipo.negocio)
    mensaje = Column(Text, nullable=False)
    contacto = Column(String, nullable=False)
    encontraste = Column(String, nullable=True)
    utm_source = Column(String, nullable=True)
    utm_medium = Column(String, nullable=True)
    utm_campaign = Column(String, nullable=True)
    ref = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
