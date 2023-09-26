from fastapi import FastAPI, HTTPException
from psycopg2 import OperationalError
from sqlalchemy.orm import Session
from .database import engine, SessionLocal, Base
from . import crud


app = FastAPI(title="ToDoist API")


def check_database():
    try:
        connection = engine.connect()
    except OperationalError:
        engine.execute("Create DATABASE todos")
        engine.execute("Use DATABASE todos")
    finally:
        connection.close()


# Получить все задачи
@app.get("/todos")
def get_todos():
    return todos


# Получить определенную задачу по ее ID
@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo_by_id(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Задача не найдена")


# Создать новую задачу
@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: Todo):
    todos.append(todo.dict())
    return todo


# Обновить задачу по ее ID
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo_by_id(todo_id: int, todo: Todo):
    for index, item in enumerate(todos):
        if item["id"] == todo_id:
            todos[index] = todo.dict()
            return todo
    raise HTTPException(status_code=404, detail="Задача не найдена")


# Удалить задачу по ее ID
@app.delete("/todos/{todo_id}")
def delete_todo_by_id(todo_id: int):
    for index, item in enumerate(todos):
        if item["id"] == todo_id:
            todos.pop(index)
            return {"message": "Задача успешно удалена"}
    raise HTTPException(status_code=404, detail="Задача не найдена")
