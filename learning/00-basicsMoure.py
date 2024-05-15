from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

"""
Version mouredev
"""

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

@app.get("/users")
def ingresarUsuario():
    return users_list

@app.post("/user/")
def buscarUsuario(user : User):
    if type(search_user(user.id)) == User:
        return {"error": "El usuario ya existe"}
    else:
        users_list.append(user)

@app.put("/user/")
def actualizarUsuarios(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "No se actualizo el usuario"}
    
@app.delete("/user/{id}")
def borrarUser(id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        {"error": "No se ha encontrado el usuario"}