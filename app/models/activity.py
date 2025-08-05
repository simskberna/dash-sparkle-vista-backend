from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class UserActivity(Base):
    __tablename__=  "user_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


    user = relationship("User",back_populates="activities")