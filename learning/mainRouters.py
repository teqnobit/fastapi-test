from fastapi import FastAPI
from routers import items, users_db
import authenticationJWT
from routers import users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(items.router)
app.include_router(users.router)
app.include_router(authenticationJWT.router)
app.include_router(users_db.router)

# Configurar el middleware CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Esto permitirá solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def mainApi():
    return {"Hola": "Mundo"}
