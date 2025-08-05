from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.token_repository import TokenRepository
from app.auth import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
bearer_scheme = HTTPBearer()
router = APIRouter()

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = creds.credentials
    decoded = decode_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = UserRepository(db).get_by_id(int(decoded["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/me")
def get_user_info(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
        "last_login": user.last_login
    }

@router.get("/stats")
def get_user_stats(user=Depends(get_current_user), db: Session = Depends(get_db)):
    count = TokenRepository(db).count_active_tokens(user.id)
    return {"active_sessions": count, "last_login": user.last_login}