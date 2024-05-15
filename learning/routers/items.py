# from fastapi import FastAPI
from fastapi import APIRouter

# app = FastAPI()
router = APIRouter(prefix="/items",
                   tags=["products"],
                   responses={404: {"message": "No encontrado"}})

items_list = ["platano", "leche", "huevos"]

@router.get("/")
def obtenerItem():
    return items_list

@router.get("/{indice}")
def obtenerItem(indice: int):
    return items_list[indice]
