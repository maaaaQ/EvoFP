from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings
import logging

logger = logging.getLogger(__name__)


class Config(BaseSettings):
    postgres_dsn: PostgresDsn = Field(
        default="postgresql://user:pass@localhost:5432/foobar",
        env="POSTGRES_DSN",
        alias="POSTGRES_DSN",
    )

    smtp_host: str = Field(
        default="smtp.example.com",
        env="SMTP_HOST",
        alias="SMTP_HOST",
    )

    smtp_port: int = Field(
        default=587,
        env="SMTP_PORT",
        alias="SMTP_PORT",
    )
    smtp_user: str = Field(
        default="username",
        env="SMTP_USER",
        alias="SMTP_USER",
    )
    smtp_pass: str = Field(
        default="password",
        env="SMTP_PASS",
        alias="SMTP_PASS",
    )

    rabbitmq: str = Field(
        default="amqp://guest:guest@localhost:5672//",
        env="RABBIT",
        alias="RABBIT",
    )

    class Config:
        env_file = ".env"
        extra = "allow"


def load_config() -> Config:
    app_config: Config = Config()
    logger.info(
        "Service configuration loaded:\n"
        + f"{app_config.model_dump_json(by_alias=True, indent=4)}"
    )
    return app_config
