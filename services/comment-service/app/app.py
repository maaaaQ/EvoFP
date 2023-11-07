import typing
from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
import httpx
from sqlalchemy.orm import Session
from .database import DB_INITIALIZER
from .schemas import CommentsCreate, CommentsUpdate, Comments
from .brokermanager import brokermanager
from . import crud, config

import logging
from fastapi.logger import logger

# Настройка журнала для сообщений о событиях
logger = logging.getLogger(__name__)
logging.basicConfig(level=2, format="%(levelname)-9s %(message)s")


cfg: config.Config = config.load_config()

brokermanager.inject_brokers(cfg.rabbitmq.unicode_string())
# Загрузка конфигурации
logger.info(
    "Service configuration loaded:\n"
    + f"{cfg.model_dump_json(by_alias=True, indent=4)}"
)

SessionLocal = DB_INITIALIZER.init_database(str(cfg.postgres_dsn))

app = FastAPI(title="ToDoist API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_email_from_user_service(token: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.get("http://user-service:5000/users/me", headers=headers)
    user_data = response.json()
    email = user_data.get("email")
    return email


# Создание комментария
@app.post(
    "/comments",
    status_code=201,
    summary="Создает новый комментарий",
    response_model=Comments,
    tags=["comments"],
)
async def add_comment(
    comments: CommentsCreate,
    db: Session = Depends(get_db),
    broker_manager: brokermanager.BrokerManager = Depends(
        brokermanager.get_broker_manager
    ),
    authorization: str = Header(None),
) -> Comments:
    if comments.task_id < 1:
        raise HTTPException(
            status_code=400, detail="Значение поля tasks_id не может быть меньше 1"
        )
    token = authorization.split(" ")[1]
    email = await get_email_from_user_service(token)
    emails = email
    comments = crud.create_comment(db, comments)
    if comments:
        message = {
            "tasks_id": str(comments.task_id),
            "text": str(comments.text),
            "user_id": str(comments.user_id),
            "email": str(emails),
        }
        broker_manager.publish_message(
            exchange_name="comments",
            routing_key="comment.created",
            message=message,
        )
        return comments
    return JSONResponse(status_code=404, content={"message": "Комментарий не создан"})


# Отображение информации о всех комментариях
@app.get(
    "/comments",
    summary="Возвращает все комментарии",
    response_model=list[Comments],
    tags=["comments"],
)
async def get_comments_list(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    tasks_id: int = 1,
) -> typing.List[Comments]:
    return crud.get_comments(db, skip, limit, tasks_id)


# Получить определенный комментарий по ID
@app.get(
    "/comments/{comments_id}",
    summary="Возвращает комментарий по ID",
    tags=["comments"],
)
async def get_comments_by_id(
    tasks_id: int, comments_id: int, db: Session = Depends(get_db)
) -> Comments:
    comments = crud.get_comments_about(db, tasks_id, comments_id)
    if comments:
        return comments
    return JSONResponse(status_code=404, content={"message": "Комментарий не найден"})


# Обновить определенный комментарий
@app.put(
    "/comments/{comments_id}",
    summary="Обновляет комментарий по ID",
    tags=["comments"],
)
async def update_comment(
    comments_id: int,
    comments: CommentsUpdate,
    db: Session = Depends(get_db),
) -> CommentsUpdate:
    upd_comment = crud.update_comment(db, comments_id, comments)
    if upd_comment:
        return upd_comment
    return JSONResponse(status_code=404, content={"message": "Комментарий не найден"})


# Удалить определенный комментарий
@app.delete(
    "/comments/{comments_id}",
    summary="Удаляет комментарий по ID",
    tags=["comments"],
)
async def delete_comment(
    tasks_id: int, comments_id: int, db: Session = Depends(get_db)
) -> Comments:
    if crud.delete_comment(db, tasks_id, comments_id):
        return JSONResponse(status_code=200, content={"message": "Комментарий удален"})
    return JSONResponse(status_code=404, content={"message": "Комментарий не найден"})
