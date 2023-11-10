import logging

from pydantic import AmqpDsn, Field, PostgresDsn, SecretStr, FilePath
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Config(BaseSettings):
    postgres_dsn: PostgresDsn = Field(
        default="postgresql://user:pass@localhost:5432/foobar",
        env="POSTGRES_DSN",
        alias="POSTGRES_DSN",
    )

    jwt_secret: SecretStr = Field(
        default="jwt_secret", env="JWT_SECRET", alias="JWT_SECRET"
    )

    reset_password_token_secret: SecretStr = Field(
        default="reset_password_token_secret",
        env="RESET_PASSWORD_TOKEN_SECRET",
        alias="RESET_PASSWORD_TOKEN_SECRET",
    )

    verification_token_secret: SecretStr = Field(
        default="verification_token_secret",
        env="VERIFICATION_TOKEN_SECRET",
        alias="VERIFICATION_TOKEN_SECRET",
    )

    rabbitmq: AmqpDsn = Field(
        default="amqp://guest:guest@localhost:5672//",
        env="RABBIT",
        alias="RABBIT",
    )

    default_groups_config_path: FilePath = Field(
        default="default-groups.json",
        env="DEFAULT_GROUPS_CONFIG_PATH",
        alias="DEFAULT_GROUPS_CONFIG_PATH",
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
