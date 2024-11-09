from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse
from typing import Dict, Annotated

app = FastAPI()

# Инициализация словаря пользователей
users: Dict[str, str] = {'1': 'Имя: Example, возраст: 18'}

@app.get("/users", response_class=JSONResponse)
async def get_users():
    return users

@app.post("/user/{username}/{age}", response_class=JSONResponse)
async def create_user(
    username: Annotated[str, Path(
        description="Введите имя пользователя",
        min_length=3,
        max_length=20
    )],
    age: Annotated[int, Path(
        description="Введите возраст пользователя",
        ge=0,  # больше или равно 0
        le=120  # меньше или равно 120
    )]
):
    user_id = str(max(map(int, users.keys()), default=0) + 1)  # Найти максимальный id
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return JSONResponse(content={"message": f"User {user_id} is registered"})

@app.put("/user/{user_id}/{username}/{age}", response_class=JSONResponse)
async def update_user(
    user_id: Annotated[str, Path(
        description="Введите id пользователя"
    )],
    username: Annotated[str, Path(
        description="Введите имя пользователя",
        min_length=3,
        max_length=20
    )],
    age: Annotated[int, Path(
        description="Введите возраст пользователя",
        ge=0,
        le=120
    )]
):
    if user_id in users:
        users[user_id] = f"Имя: {username}, возраст: {age}"
        return JSONResponse(content={"message": f"User {user_id} has been updated"})
    else:
        return JSONResponse(content={"message": f"User {user_id} does not exist"}, status_code=404)

@app.delete("/user/{user_id}", response_class=JSONResponse)
async def delete_user(
    user_id: Annotated[str, Path(
        description="Введите id пользователя"
    )]
):
    if user_id in users:
        del users[user_id]
        return JSONResponse(content={"message": f"User {user_id} has been deleted"})
    else:
        return JSONResponse(content={"message": f"User {user_id} does not exist"}, status_code=404)

