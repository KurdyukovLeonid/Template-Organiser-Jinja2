from fastapi import FastAPI, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/', response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users, "title": "User List"})


@app.get('/users/{user_id}', response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user, "title": "User Details"})
    raise HTTPException(status_code=404, detail='User not found')


@app.post('/user/{username}/{age}')
def user_reg(username: str, age: int) -> User:
    user = User(id=len(users) + 1, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
def user_put(user_id: int, user: User) -> User:
    for index, existing_user in enumerate(users):
        if existing_user.id == user_id:
            users[index].username = user.username
            users[index].age = user.age
            return users[index]
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
def delete_user(user_id: int) -> User:
    for index, existing_user in enumerate(users):
        if existing_user.id == user_id:
            return users.pop(index)
    raise HTTPException(status_code=404, detail='User was not found')


user_reg("UrbanUser", 24)
user_reg("UrbanTest", 22)
user_reg("Capybara", 60)