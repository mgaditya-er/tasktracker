from app.core.config import settings


def validate_settings():
    required = [
        settings.DATABASE_URL,
        settings.APP_PORT,
        settings.LOG_LEVEL
    ]

    if not all(required):
        raise ValueError(
            "Required environment variables are missing"
        )