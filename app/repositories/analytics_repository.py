from sqlalchemy.orm import Session
from app.models.analytics import Revenue,DeviceUsage,ProductPerformance


class AnalyticsRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_revenue_overview(self):
        return self.db.query(Revenue).all()

    def get_device_usage(self):
        return self.db.query(DeviceUsage).all()

    def get_product_performance(self):
        return self.db.query(ProductPerformance).all()