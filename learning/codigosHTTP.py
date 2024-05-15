from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

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

@app.get("/users/")
def obtenerUsers():
    return users_list


@app.post("/user/", response_model=User, status_code=201)
def buscarUser(user : User):
    if type(search_user(user.id)) == User:
        # return {"error": "El usuario ya existe"}
        raise HTTPException(404, detail="El usuario ya existe")
        # return HTTPException(201, detail="El usuario ya existe")
    users_list.append(user)
    return user

@app.get("/user/{id}")
def buscarUser(id: int):
    for index, user in enumerate(users_list):
        if user.id == id:
            return users_list[index]
    return {"error": "Usuario no encontrado"}

@app.delete("/user/{id}")
def eliminarUser(id: int):
    for index, user in enumerate(users_list):
        if user.id == id:
            del users_list[index]
    return {"error": "Usuario no encontrado"}

    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        {"error": "usuario no encontrado"}
