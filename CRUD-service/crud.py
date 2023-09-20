from fastapi import FastAPI

app = FastAPI(title="ToDoist API")


# Демо-данные
todos = [
    {"id": 1, "title": "Купить продукты", "completed": False},
    {"id": 2, "title": "Сделать уборку", "completed": True},
    {"id": 3, "title": "Погулять с собакой", "completed": False},
]


@app.get("/todos")
def get_todos():
    return todos
