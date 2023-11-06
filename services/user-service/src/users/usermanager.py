import json
import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, models, schemas, exceptions

from src.users import models, secretprovider
from kombu import Connection, Exchange, Queue
from src import config
from src.brokermanager import brokermanager
from fastapi_users.db import SQLAlchemyUserDatabase


class UserManager(UUIDIDMixin, BaseUserManager[models.User, uuid.UUID]):
    def __init__(
        self,
        broker_manager: brokermanager.BrokerManager,
        user_db: SQLAlchemyUserDatabase,
        password_helper: BaseUserManager.password_helper,
    ):
        super().init(user_db, password_helper)
        self.broker_manager = broker_manager

    async def on_after_register(
        self, user: models.User, request: Optional[Request] = None
    ):
        print(f"User {user.id} has registered.")
        message = {
            "user_id": str(user.id),
            "email": user.email,
            "nickname": user.nickname,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        await self.broker_manager.publish_message(
            exchange_name="registered",
            routing_key="user.registered",
            message=json.dumps(message),
        )

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.User:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["group_id"] = 2
        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_forgot_password(
        self, user: models.User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: models.User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(
    user_db=Depends(models.get_user_db),
    secret_provider: secretprovider.SecretProvider = Depends(
        secretprovider.get_secret_provider
    ),
    broker_manager: brokermanager.BrokerManager = Depends(
        brokermanager.get_broker_manager
    ),
):
    user_manager = UserManager(broker_manager, user_db)
    user_manager.reset_password_token_secret = (
        secret_provider.reset_password_token_secret
    )
    user_manager.verification_token_secret = secret_provider.verification_token_secret
    yield user_manager
