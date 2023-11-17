import logging
import typing
import json
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src import config, users, brokermanager

logger = logging.getLogger(__name__)
logging.basicConfig(level=2, format="%(levelname)-9s %(message)s")

app_config: config.Config = config.load_config()

app = FastAPI()

users.inject_secrets(
    jwt_secret=app_config.jwt_secret.get_secret_value(),
    verification_token_secret=app_config.verification_token_secret.get_secret_value(),
    reset_password_token_secret=app_config.reset_password_token_secret.get_secret_value(),
)
users.include_routers(app)

brokermanager.brokermanager.inject_brokers(app_config.rabbitmq.unicode_string())


@app.post(
    "/groups",
    status_code=201,
    response_model=users.schemas.GroupRead,
    summary="Создает новую группу пользователей",
    tags=["user-groups"],
)
async def add_group(
    group: users.schemas.GroupCreate,
    session: AsyncSession = Depends(users.models.get_async_session),
):
    return await users.groupcrud.create_group(group, session)


@app.get(
    "/groups",
    summary="Возвращает список групп пользователей",
    response_model=list[users.schemas.GroupRead],
    tags=["user-groups"],
)
async def get_group_list(
    session: AsyncSession = Depends(users.models.get_async_session),
    skip: int = 0,
    limit: int = 100,
) -> typing.List[users.schemas.GroupRead]:
    return await users.groupcrud.get_all_groups(session, skip, limit)


@app.get(
    "/groups/{group_id}",
    summary="Возвращает информацию о группе пользователей по ID",
    tags=["user-groups"],
)
async def get_group_info(
    group_id: int, session: AsyncSession = Depends(users.models.get_async_session)
) -> users.schemas.GroupRead:
    group = await users.groupcrud.get_group_by_id(session, group_id)
    if group != None:
        return group
    return JSONResponse(status_code=404, content={"message": "Группа не найдена"})


@app.put(
    "/groups/{group_id}",
    summary="Обновляет информацию о группе пользователей по ID",
    tags=["user-groups"],
)
async def update_group(
    group_id: int,
    group: users.schemas.GroupUpdate,
    session: AsyncSession = Depends(users.models.get_async_session),
) -> users.schemas.GroupRead:
    group = await users.groupcrud.update_group(session, group_id, group)
    if group != None:
        return group
    return JSONResponse(status_code=404, content={"message": "Группа не найдена"})


@app.delete(
    "/groups/{group_id}",
    summary="Удаляет информацию о группе пользователей по ID",
    tags=["user-groups"],
)
async def delete_device(
    group_id: int, session: AsyncSession = Depends(users.models.get_async_session)
) -> users.schemas.GroupRead:
    if await users.groupcrud.delete_group(session, group_id):
        return JSONResponse(
            status_code=200, content={"message": "Группа успешно удалена"}
        )
    return JSONResponse(status_code=404, content={"message": "Группа не найдена"})


@app.on_event("startup")
async def on_startup():
    await users.database.initializer.init_database(
        app_config.postgres_dsn.unicode_string()
    )

    groups = []
    with open(app_config.default_groups_config_path) as f:
        groups = json.load(f)

    async for session in users.models.get_async_session():
        for group in groups:
            await users.groupcrud.upsert_group(
                session, users.schemas.GroupUpsert(**group)
            )
