from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, status, Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from fastapi.security import OAuth2PasswordBearer

JWT_SECRET_KEY = "727acad35599f01b292132174eb08ed88a292b3c22f03d358f248d68e9c37eef"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserOut(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginPayload(BaseModel):
    email: EmailStr
    password: str

class TokenPayload(BaseModel):
    sub: str
    user_id: int

users: list[dict] = []
next_user_id = 1

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def create_access_token(*, user_id: int, email: str, expires_minutes: Optional[int] = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"sub": email, "user_id": user_id, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def get_user_by_email(email: str) -> Optional[dict]:
    return next((u for u in users if u["email"] == email), None)

def get_user_by_id(user_id: int) -> Optional[dict]:
    return next((u for u in users if u["id"] == user_id), None)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        data = TokenPayload(**payload)
    except JWTError:
        raise cred_exc

    user = get_user_by_id(data.user_id)
    if not user or user["email"] != data.sub:
        raise cred_exc
    return user

app = FastAPI(title="Users API", version="1.0.0")

@app.post("/register", response_model=UserOut, status_code=201)
async def register(payload: UserCreate):
    global next_user_id
    if get_user_by_email(payload.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    user = {
        "id": next_user_id,
        "email": payload.email,
        "full_name": payload.full_name,
        "password_hash": hash_password(payload.password),
    }
    users.append(user)
    next_user_id += 1
    return user

@app.post("/login", response_model=Token)
async def login(payload: LoginPayload):
    user = get_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token(user_id=user["id"], email=user["email"])
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users", response_model=list[UserOut])
async def list_users(current_user: dict = Depends(get_current_user)):
    return [{"id": u["id"], "email": u["email"], "full_name": u["full_name"]} for u in users]


