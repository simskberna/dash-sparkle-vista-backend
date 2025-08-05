from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.routes.user_routes import get_current_user
from app.repositories.activity_repository import ActivityRepository

router = APIRouter()

@router.get("/activity/chart")
def get_activity_chart(user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = ActivityRepository(db)
    return repo.get_activity_count_by_date(user.id)
