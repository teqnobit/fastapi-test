from fastapi import FastAPI
from routers import items, users_db
import authenticationJWT
from routers import users

app = FastAPI()
app.include_router(items.router)
app.include_router(users.router)
app.include_router(authenticationJWT.router)
app.include_router(users_db.router)

@app.get("/")
def mainApi():
    return {"Hola": "Mundo"}