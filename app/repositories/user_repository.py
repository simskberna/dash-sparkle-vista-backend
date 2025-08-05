from sqlalchemy.orm import Session
from app.models.user import User
from app.auth import hash_password


class UserRepository:
    def __init__(self, db:Session):
        self.db = db

    def create_user(self,email:str, password:str):
        user = User(email=email, password_hash=hash_password(password))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email:str):
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id:int):
        return self.db.query(User).filter(User.id == user_id).first()

    def update_last_login(self, user:User):
        from datetime import datetime
        user.last_login = datetime.utcnow()
        self.db.commit()
        return user