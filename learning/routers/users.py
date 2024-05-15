# from fastapi import FastAPI
from fastapi import APIRouter
from pydantic import BaseModel

# app = FastAPI()
router = APIRouter()

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [
    User(id = 1, name = "Ariel", surname = "Tequida", url = "http://teqnobit.com", age = 27),
    User(id = 2, name = "Jesus", surname = "Andujo", url = "http://www.google.com", age = 27),
    User(id = 3, name = "Fer", surname = "Luna", url = "Ferluna.com", age = 23)
]

@router.get("/users/{id}")
def ingresarUsuario(id: int):
    return users_list[id-1]