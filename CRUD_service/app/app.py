import typing
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from schemas.todo import Tasks, TasksOn
from database.database import engine, SessionLocal, Base
import crud

# Base.metadata.create_all(bind=engine)

app = FastAPI(title="ToDoist API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Получить все задачи
@app.get("/tasks", summary="Возвращает все задачи", response_model=list[Tasks])
async def get_tasks_list(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> typing.List[Tasks]:
    return crud.get_tasks(db=get_db(), skip=skip, limit=limit)


# Получить определенную задачу по ее ID
@app.get("/tasks/{tasks_id}", summary="Возвращает задачу по ее ID")
async def get_tasks_by_id(tasks_id: int, db: Session = Depends(get_db)) -> Tasks:
    tasks = crud.get_tasks(db=get_db(), tasks_id=tasks_id)
    if tasks != None:
        return tasks
    raise HTTPException(status_code=404, detail="Задача не найдена")


# Создать новую задачу
@app.post(
    "/tasks", response_model=Tasks, status_code=201, summary="Добавляет задачу в базу"
)
async def create_task(tasks: TasksOn, db: Session = Depends(get_db)) -> Tasks:
    return crud.create_task(db=db, tasks=tasks)


# Обновить задачу по ее ID
@app.put("/tasks/{tasks_id}", summary="Обновляет задачу по ее ID", response_model=Tasks)
async def update_task(
    tasks_id: int, tasks: TasksOn, db: Session = Depends(get_db)
) -> Tasks:
    tasks = crud.update_tasks(db=db, tasks_id=tasks_id, tasks=tasks)
    if tasks != None:
        return tasks
    return HTTPException(status_code=404, detail="Задача не найдена")


# Удалить задачу по ее ID
@app.delete(
    "/tasks/{tasks_id}", summary="Удаляет задачу по ее ID", response_model=Tasks
)
async def delete_task_by_id(tasks_id: int, db: Session = Depends(get_db)) -> Tasks:
    if crud.delete_tasks(db=db, tasks_id=tasks_id):
        return HTTPException(status_code=200, detail="Задача успешно удалена")

    raise HTTPException(status_code=404, detail="Задача не найдена")
