from src import config


cfg: config.Config = config.load_config()


class SecretProvider:
    reset_password_token_secret = cfg.reset_password_token_secret
    verification_token_secret = cfg.verification_token_secret
    jwt_secret = cfg.jwt_secret


secret_provider: SecretProvider = SecretProvider()


def inject_secrets(
    jwt_secret: str, reset_password_token_secret: str, verification_token_secret: str
):
    secret_provider.jwt_secret = jwt_secret
    secret_provider.reset_password_token_secret = reset_password_token_secret
    secret_provider.verification_token_secret = verification_token_secret


async def get_secret_provider() -> SecretProvider:
    yield secret_provider
