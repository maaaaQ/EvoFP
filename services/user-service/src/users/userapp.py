import uuid

from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from src.users import models, schemas, secretprovider, usermanager


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy(
    secret_provider: secretprovider.SecretProvider = Depends(
        secretprovider.get_secret_provider
    ),
) -> JWTStrategy:
    return JWTStrategy(secret=secret_provider.jwt_secret, lifetime_seconds=1800)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[models.User, uuid.UUID](
    usermanager.get_user_manager, [auth_backend]
)


def include_routers(app: FastAPI):
    app.include_router(
        fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
    )
    app.include_router(
        fastapi_users.get_register_router(schemas.UserRead, schemas.UserCreate),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(schemas.UserRead),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(schemas.UserRead, schemas.UserUpdate),
        prefix="/users",
        tags=["users"],
    )
