import typing
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .database import models
from . import schemas
from fastapi import Query


# Создание нового комментария
def create_comment(db: Session, comments: schemas.CommentsCreate) -> models.Comment:
    db_comments = models.Comment(
        text=comments.text,
        user_id=comments.user_id,
        created_at=comments.created_at,
        task_id=comments.task_id,
    )
    db.add(db_comments)
    db.commit()
    db.refresh(db_comments)
    return db_comments


# Отображение информации о всех комментариях
def get_comments(
    db: Session, skip: int = 0, limit: int = 100, tasks_id: int = 0
) -> typing.List[models.Comment]:
    return (
        db.query(models.Comment)
        .filter(models.Comment.task_id == tasks_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# Отображение информации о конкретном комментарии
def get_comments_about(db: Session, tasks_id: int, comments_id: int) -> models.Comment:
    if tasks_id and comments_id:
        return (
            db.query(models.Comment)
            .filter(models.Comment.task_id == tasks_id)
            .filter(models.Comment.id == comments_id)
            .first()
        )


# Обновить комментарий по ID
def update_comment(
    db: Session, comments_id: int, upd_comments: schemas.CommentsUpdate
) -> models.Comment:
    comment = (
        db.query(models.Comment)
        .filter(models.Comment.id == comments_id)
        .update(upd_comments.dict())
    )
    db.commit()
    if comment == 1:
        return db.query(models.Comment).filter(models.Comment.id == comments_id).first()


# Удаление комментария
def delete_comment(db: Session, tasks_id: int, comments_id: int) -> bool:
    result = (
        db.query(models.Comment)
        .filter(models.Comment.task_id == tasks_id, models.Comment.id == comments_id)
        .delete()
    )
    db.commit()
    return result == 1
