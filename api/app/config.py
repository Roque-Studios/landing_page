import structlog
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

logger = structlog.get_logger()

load_dotenv()


class Settings(BaseSettings):
    # Required
    DATABASE_URL: str

    # Optional with defaults
    ENVIRONMENT: str = "dev"
    ALLOWED_ORIGINS: str = "http://localhost,http://localhost:8090"
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: str | None = None

    # Email (Resend) — leads are stored regardless; email is best-effort.
    # Leave RESEND_API_KEY unset to run with email sending disabled.
    RESEND_API_KEY: str | None = None
    RESEND_FROM_EMAIL: str = "onboarding@resend.dev"
    NOTIFY_EMAIL: str = "contacto@roquestudios.io"

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

    class Config:
        env_file = ".env"
        extra = "ignore"


def get_settings() -> Settings:
    try:
        logger.info("Loading application settings")
        settings = Settings()
        logger.info("Settings loaded successfully")
        if not settings.RESEND_API_KEY:
            logger.warning("RESEND_API_KEY not set — lead notification emails are disabled")
        return settings
    except Exception as e:
        logger.error("Configuration error", error=str(e))
        raise RuntimeError(
            f"Configuration error: {e}\nMake sure DATABASE_URL is set (see .env.example)"
        )


settings = get_settings()
