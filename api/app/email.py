import structlog
from .config import settings
from .models import Lead

logger = structlog.get_logger()


def notify_new_lead(lead: Lead) -> None:
    """Best-effort email notification. Never raises — a failed send must not
    affect the already-stored lead or the API response."""
    if not settings.RESEND_API_KEY:
        logger.info("Skipping lead notification email (RESEND_API_KEY not set)", lead_id=str(lead.id))
        return

    try:
        import resend

        resend.api_key = settings.RESEND_API_KEY
        resend.Emails.send(
            {
                "from": settings.RESEND_FROM_EMAIL,
                "to": settings.NOTIFY_EMAIL,
                "subject": f"Nuevo lead ({lead.tipo.value}): {lead.nombre} — {lead.negocio}",
                "text": (
                    f"Nombre: {lead.nombre}\n"
                    f"Negocio: {lead.negocio}\n"
                    f"Tipo: {lead.tipo.value}\n"
                    f"Contacto: {lead.contacto}\n"
                    f"Cómo nos encontró: {lead.encontraste or '-'}\n"
                    f"UTM: source={lead.utm_source or '-'} medium={lead.utm_medium or '-'} "
                    f"campaign={lead.utm_campaign or '-'} ref={lead.ref or '-'}\n\n"
                    f"Mensaje:\n{lead.mensaje}"
                ),
            }
        )
        logger.info("Lead notification email sent", lead_id=str(lead.id))
    except Exception as e:
        logger.error("Failed to send lead notification email", lead_id=str(lead.id), error=str(e))
