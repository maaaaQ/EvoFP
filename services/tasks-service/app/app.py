import typing
from fastapi import Depends, FastAPI, Query
from fastapi.responses import JSONResponse
import httpx
from sqlalchemy.orm import Session
from .database import DB_INITIALIZER
from .schemas import Tasks, TasksOn
from .enums import FilterPriority, FilterCompleted

from . import crud, config
import logging
from fastapi.logger import logger
from .brokermanager import brokermanager

# Настройка журнала для сообщений о событиях
logger = logging.getLogger(__name__)
logging.basicConfig(level=2, format="%(levelname)-9s %(message)s")


cfg: config.Config = config.load_config()

# Загрузка конфигурации
logger.info(
    "Service configuration loaded:\n"
    + f"{cfg.model_dump_json(by_alias=True, indent=4)}"
)

# Инициализация базы данных
logger.info("Initializing database...")
SessionLocal = DB_INITIALIZER.init_database(str(cfg.postgres_dsn))

brokermanager.inject_brokers(cfg.rabbitmq.unicode_string())

app = FastAPI(title="ToDoist API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Получить все задачи
@app.get(
    "/tasks",
    summary="Возвращает все задачи",
    response_model=list[Tasks],
    tags=["tasks"],
)
async def get_tasks_list(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    priority: FilterPriority | None = None,
    is_completed: FilterCompleted | None = None,
) -> typing.List[Tasks]:
    return crud.get_tasks(db, skip, limit, priority, is_completed)


# Получить определенную задачу по ее ID
@app.get("/tasks/{tasks_id}", summary="Возвращает задачу по ее ID", tags=["tasks"])
async def get_tasks_by_id(tasks_id: int, db: Session = Depends(get_db)) -> Tasks:
    tasks = crud.get_tasks_about(db, tasks_id)
    if tasks != None:
        return tasks
    return JSONResponse(status_code=404, content={"message": "Задача не найдена"})


# Создать новую задачу
@app.post(
    "/task",
    status_code=201,
    summary="Создает новую задачу",
    response_model=Tasks,
    tags=["tasks"],
)
async def add_task(
    tasks: TasksOn,
    db: Session = Depends(get_db),
    broker_manager: brokermanager.BrokerManager = Depends(
        brokermanager.get_broker_manager
    ),
) -> Tasks:
    tasks = crud.create_task(db, tasks)
    if tasks != None:
        message = {
            "id": str(tasks.id),
            "title": str(tasks.title),
            "priority": str(tasks.priority),
            "user_id": str(tasks.user_id),
        }
        broker_manager.publish_message(
            exchange_name="tasks",
            routing_key="task.created",
            message=message,
        )
        return tasks
    return JSONResponse(status_code=404, content={"message": "Задача не создана"})


# Обновить задачу по ее ID
@app.put("/tasks/{tasks_id}", summary="Обновляет задачу по ее ID", tags=["tasks"])
async def update_task(
    tasks_id: int, tasks: TasksOn, db: Session = Depends(get_db)
) -> Tasks:
    tasks = crud.update_tasks(db, tasks_id, tasks)
    if tasks != None:
        return tasks
    return JSONResponse(status_code=404, content={"message": "Задача не найдена"})


# Удалить задачу по ее ID
@app.delete("/tasks/{tasks_id}", summary="Удаляет задачу по ее ID", tags=["tasks"])
async def delete_task_by_id(tasks_id: int, db: Session = Depends(get_db)) -> Tasks:
    if crud.delete_tasks(db, tasks_id):
        return JSONResponse(
            status_code=200, content={"message": "Задача успешно удалена"}
        )
    return JSONResponse(status_code=404, content={"message": "Задача не найдена"})
