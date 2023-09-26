import typing
from sqlalchemy.orm import Session
from .database import models

import schemas
from schemas.todo import *


# Создание новой записи
def create_task(db: Session, tasks: schemas.TasksOn) -> models.Tasks:
    db_tasks = models.Tasks(
        title=Tasks.title,
        description=Tasks.description,
        is_completed=Tasks.is_completed,
        created_at=Tasks.created_at,
        updated_at=Tasks.updated_at,
    )
    db.add(db_tasks)
    db.commit()
    db.refresh(db_tasks)
    return db_tasks


# Отображение информации о всех задачах
def get_tasks(
    db: Session, skip: int = 0, limit: int = 100
) -> typing.List[models.Tasks]:
    return db.query(models.Tasks).offset(skip).limit(limit).all()


# Отображение информации о конкретной задаче
def get_tasks(db: Session, tasks_id: int) -> models.Tasks:
    return db.query(models.Tasks).filter(models.Tasks.id == tasks_id).first()


# Обновление информации об устройстве
def update_tasks(db: Session, tasks_id: int, tasks: schemas.TasksOn) -> models.Tasks:
    result = (
        db.query(models.Tasks).filter(models.Tasks.id == tasks_id).update(tasks.dict())
    )
    db.commit()

    if result == 1:
        return get_tasks(db, tasks_id)
    return None


# Удаление записи
def delete_tasks(db: Session, tasks_id: int) -> bool:
    result = db.query(models.Tasks).filter(models.Tasks.id == tasks_id).delete()
    db.commit()
    return result == 1
