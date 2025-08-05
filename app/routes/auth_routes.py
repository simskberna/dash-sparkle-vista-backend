from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.token_repository import TokenRepository
from app.auth import verify_password, create_access_token, verify_token, logout_user
from app.repositories.activity_repository import ActivityRepository
from app.schemas.auth import RegisterSchema, LoginSchema
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    if repo.get_by_email(data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = repo.create_user(data.email, data.password)
    return {"message": "User created", "user_id": user.id}

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_email(data.email)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    TokenRepository(db).create_token(user.id, token)
    repo.update_last_login(user)
    ActivityRepository(db).log_activity(user.id, "login")

    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    return logout_user(token)

@router.get("/protected")
async def protected(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    payload = verify_token(credentials.credentials)
    return {"data": "protected"}