from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int
    username: str
    age: int

users: List[User] = []


@app.get("/", response_class=templates.TemplateResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {
        "request": request,
        "users": users,
        "user": None
    })

@app.get("/user/{user_id}", response_class=templates.TemplateResponse)
async def read_user(request: Request, user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    return templates.TemplateResponse("users.html", {
        "request": request,
        "user": user,
        "users": users
    })

@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            removed_user = users.pop(index)
            return removed_user
    raise HTTPException(status_code=404, detail="User was not found")

@app.post("/user", response_model=User)
async def create_user(username: str, age: int):
    user_id = (users[-1].id + 1) if users else 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

