from typing import List, Optional

from cornflakes import AnyUrl, config, config_field


@config(files=".env", eval_env=True, validate=True)
class Settings:
    """Some Fastapi settings."""

    PROJECT_NAME: str = "fastapi-boilerplate"

    SENTRY_DSN: Optional[AnyUrl] = None

    API_PATH: str = "/api/v1"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7 days

    BACKEND_CORS_ORIGINS: List[AnyUrl] = None

    # The following variables need to be defined in environment
    TEST_DATABASE_URL: Optional[AnyUrl] = None
    DATABASE_URL: AnyUrl = config_field(no_default=True)  # no default value (required)
    ASYNC_DATABASE_URL: Optional[AnyUrl] = None

    SECRET_KEY: str = ""
    #  END: required environment variables
