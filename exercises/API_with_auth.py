from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status, Path, Query, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field

# ---------------- Конфиг ----------------
JWT_SECRET_KEY = "CHANGE_ME_IN_PROD"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# ---------------- Модели ----------------
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserOut(UserBase):
    id: int

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=8)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    user_id: int

# ---------------- "БД" в памяти ----------------
users: list[dict] = []
next_user_id = 1

# ---------------- Хелперы ----------------
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

# ---------------- Инициализация ----------------
app = FastAPI(title="Users API (in-memory + JWT)", version="1.0.0")

# ---------------- AUTH ----------------
@app.post("/auth/register", response_model=UserOut, status_code=201)
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

@app.post("/auth/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form.username)
    if not user or not verify_password(form.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token(user_id=user["id"], email=user["email"])
    return {"access_token": token, "token_type": "bearer"}

# ---------------- USERS (JWT required) ----------------
@app.get("/users/me", response_model=UserOut)
async def read_me(current: dict = Depends(get_current_user)):
    return current

@app.get("/users", response_model=list[UserOut])
async def list_users(
    current: dict = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    return users[skip: skip + limit]

@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int = Path(ge=1), current: dict = Depends(get_current_user)):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@app.patch("/users/{user_id}", response_model=UserOut)
async def patch_user(
    user_id: int = Path(ge=1),
    payload: UserUpdate = Body(default=None),
    current: dict = Depends(get_current_user),
):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    if current["id"] != user_id:
        raise HTTPException(403, "You can update only your own profile")

    if payload.full_name is not None:
        user["full_name"] = payload.full_name
    if payload.password is not None:
        user["password_hash"] = hash_password(payload.password)
    return user

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int = Path(ge=1), current: dict = Depends(get_current_user)):
    global users
    user = get_user_by_id(user_id)
    if not user:
        return
    if current["id"] != user_id:
        raise HTTPException(403, "You can delete only your own account")
    users = [u for u in users if u["id"] != user_id]
