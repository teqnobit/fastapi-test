from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "13ccb61748fa569b93d3f4dbd69ea6fde4a488570f0ed5f0690d1d88e777def4"

router = APIRouter(
    prefix="/loginJWT",
    tags=["loginJWT"],
    responses={404: {"message": "No encontrado"}}
)

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "$2a$12$j5rpyFlkoCx3NfhxrJN0fuic0DdX9x8QBR5lCSWPw50hGu70CRSJS", 
    },
    "teqnobit2": {
        "username": "teqnobit2",
        "full_name": "Ariel Tequida2",
        "email": "ariel.tequida2@gmail.com",
        "disabled": False,
        "password": "$2a$12$JDCFBQ8IyEpXIdWXwnXxkeB02v5X3FmDfrg5QA9HU7eU0s9fsP50K",
    }, 
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) # El doble asterisco "desenvuelve" el diccionario y lo pasa como parametro

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
def authUser(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Credenciales de autenticacion invalidas",
        headers={"WWW_Authenticate": "Bearer"}
    )

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception
    
    return search_user(username)

# login con token 
def current_user(user: User = Depends(authUser)):
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo"
        )
    
    return user

@router.get("/me")
def me(user: User = Depends(current_user)):
    return user

# login con formulario
@router.post("/")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(404, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta"
        )
    
    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION),
    }

    return {
        "access_token": jwt.encode(
            access_token,
            SECRET,
            algorithm=ALGORITHM
        ), 
        "token_type": "bearer"
    }








    