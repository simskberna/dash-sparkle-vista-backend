from sqlalchemy.orm import Session
from app.models.activity import UserActivity

class ActivityRepository:
    def __init__(self, db:Session):
        self.db = db


    def log_activity(self, user_id:int, action:str):
        activity = UserActivity(user_id=user_id, action=action)
        self.db.add(activity)
        self.db.commit()
        return activity

    def get_activity_count_by_date(self, user_id: int):
        from sqlalchemy import func
        results = (
            self.db.query(func.date(UserActivity.timestamp), func.count(UserActivity.id))
            .filter(UserActivity.user_id == user_id)
            .group_by(func.date(UserActivity.timestamp))
            .order_by(func.date(UserActivity.timestamp))
            .all()
        )
        return [{"date": str(r[0]), "count": r[2] } for r in results]