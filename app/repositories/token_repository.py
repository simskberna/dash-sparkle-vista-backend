from sqlalchemy.orm import Session
from app.models.token import UserToken

class TokenRepository:
    def __init__(self, db:Session):
        self.db = db

    def create_token(self, user_id: int, token:str):
        db_token = UserToken(user_id=user_id, token=token)
        self.db.add(db_token)
        self.db.commit()
        return db_token

    def count_active_tokens(self, user_id:int):
        return self.db.query(UserToken).filter(UserToken.user_id == user_id).count()

    def delete_token(self,token:str):
        self.db.query(UserToken).filter(UserToken.token == token).delete()
        self.db.commit()