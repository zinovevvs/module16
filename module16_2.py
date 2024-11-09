from fastapi import FastAPI, Path
from fastapi.responses import HTMLResponse
from typing import Annotated

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "Главная страница"

@app.get("/user/admin", response_class=HTMLResponse)
async def read_admin():
    return "Вы вошли как администратор"

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def read_user(
    user_id: Annotated[int, Path(
        description="Enter User ID",
        gt=0,  # больше 0
        le=100  # меньше или равно 100
    )]
):
    return f"Вы вошли как пользователь № {user_id}"

@app.get("/user/{username}/{age}", response_class=HTMLResponse)
async def read_user_info(
    username: Annotated[str, Path(
        description="Enter username",
        min_length=5,  # больше или равно 5
        max_length=20  # меньше или равно 20
    )],
    age: Annotated[int, Path(
        description="Enter age",
        ge=18,  # больше или равно 18
        le=120  # меньше или равно 120
    )]
):
    return f"Информация о пользователе. Имя: {username}, Возраст: {age}"