from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Revenue(Base):
    __tablename__ = "revenues"
    id = Column(Integer, primary_key=True, index=True)
    month = Column(String)
    revenue = Column(Float)
    growth = Column(Float)

class DeviceUsage(Base):
    __tablename__ = "device_usage"
    id = Column(Integer, primary_key=True, index=True)
    device_type = Column(String)
    percentage = Column(Float)


class ProductPerformance(Base):
    __tablename__ = "product_performance"
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    sales = Column(Float)
    revenue = Column(Float)