# Usuarios con base de datos y mongodb

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db.models.usersModel import UserMo
from db.client import db_client
from db.schemas.userSchema import user_schema, users_schema
from bson import ObjectId


router = APIRouter(
    prefix=("/usersDB"),
    tags=["usersDB"],
    responses={404: {"message": "Mensaje de error"}}
)

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


@router.get("/", response_model=list[UserMo])
def users():
    return users_schema(db_client.users.find())

@router.get("/query")
def user(field: str, key: str):
    return searchUser(field, key)

@router.get("/{id}")
def user(id: str):
    return searchUser("_id", ObjectId(id))


@router.post("/", response_model=UserMo, status_code=201)
def user(user: UserMo):
    
    if type(searchUser("email", user.email)) == UserMo:
        raise HTTPException(status_code=404, detail="El usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]

    # inserta usuario con id nuevo en BD
    id = db_client.users.insert_one(user_dict).inserted_id 
    # Lee usuario con el id de BD
    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return UserMo(**new_user)


@router.put("/")
def user(user: UserMo):
    user_dict = dict(user)
    del user_dict["id"]

    try:
        new_user = db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, 
            user_dict
        )
        print(type(new_user))
        print(new_user)
    except:
        return {"error": "No se ha actualizado el usuario"}
    
    return searchUser("_id", ObjectId(user_schema(new_user)["id"]))


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/{id}")
def user(id: str):
    try:
        found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    except:
        return {"error": "id invalido"}

    if not found: 
        return {"error": "No se ha eliminado el usuario"}
    else:
        return {"message": "Usuario eliminado exitosamente"}


def searchUser(field: str, key):
    # users = filter(lambda user: user.id == id, users_list)
    try:
        # return list(users)[0]
        user = db_client.users.find_one({field: key})
        return UserMo(**user_schema(user))
    except:
        return {"error": "usuario no encontrado"}