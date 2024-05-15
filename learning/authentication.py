from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="login") 

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
    
class UserDB(User):
    password: str

# users_db: dict[str, dict[str, Any]]
users_db = {
    "teqnobit": {
        "username": "teqnobit",
        "full_name": "Ariel Tequida",
        "email": "ariel.tequida@gmail.com",
        "disabled": False,
        "password": "123456", # De forma general esto deberia de llevar una encriptacion
    },
    "teqnobit2": {
        "username": "teqnobit2",
        "full_name": "Ariel Tequida2",
        "email": "ariel.tequida2@gmail.com",
        "disabled": False,
        "password": "654321", # De forma general esto deberia de llevar una encriptacion
    }, 
}

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) # El doble asterisco "desenvuelve" el diccionario y lo pasa como parametro
    
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
# login con token 
def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Credenciales de autenticacion invalidas",
            headers={"WWW_Authenticate": "Bearer"}
        )
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo"
        )
    
    return user

# login con formulario
@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(404, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta"
        )
    
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
def me(user: User = Depends(current_user)):
    return user





## Login html
from fastapi.responses import HTMLResponse

@app.post("/loginHTML", response_class=HTMLResponse)
def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(404, detail="El usuario no existe")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta"
        )
    
    return """{"access_token": user.username, "token_type": "bearer"}
        <html>
        <body>
            <a href="http://127.0.0.1:8000/users/me">
                <button type="button">Ir a otra página</button>
            </a>
        </body>
        </html>
    """