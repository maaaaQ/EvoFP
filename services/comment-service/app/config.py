from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    postgres_dsn: PostgresDsn = Field(
        default="postgresql://user:pass@localhost:5432/foobar",
        env="POSTGRES_DSN",
        alias="POSTGRES_DSN",
    )

    int_example: int = Field(default=5, env="INT_EXAMPLE", alias="INT_EXAMPLE")

    bool_example: bool = Field(default=False, env="BOOL_EXAMPLE", alias="BOOL_EXAMPLE")

    rabbitmq: str = Field(
        default="amqp://guest:guest@localhost:5672//",
        env="RABBIT",
        alias="RABBIT",
    )

    class Config:
        env_file = ".env"


def load_config() -> Config:
    return Config()
