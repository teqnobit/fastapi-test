from fastapi import FastAPI

app = FastAPI()

# Es importante ordenar los path para que el servidor no tenga conflictos
# primero van los path fijos y luego los de parametros
@app.get("/items/me")
def item_me(nombre : str | None = None):
    if nombre:
        return {"item_id": "item actual", "nombre": nombre}
    else:
        return {"item_id": "item actual"}

@app.get("/items/{item_id}")
def items(item_id: int):
    return {"item_id": item_id}
