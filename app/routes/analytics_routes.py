from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.analytics_repository import AnalyticsRepository
from app.routes.user_routes import get_current_user

router = APIRouter()

@router.get("/analytics/revenue")
def revenue_overview(user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = AnalyticsRepository(db)
    return [{"month": r.month, "revenue": r.revenue, "growth": r.growth} for r in repo.get_revenue_overview()]

@router.get("/analytics/device-usage")
def device_usage(user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = AnalyticsRepository(db)
    return [{"device": d.device_type, "percentage": d.percentage} for d in repo.get_device_usage()]

@router.get("/analytics/product-performance")
def product_performance(user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = AnalyticsRepository(db)
    return [{"product": p.product_name, "sales": p.sales, "revenue": p.revenue} for p in repo.get_product_performance()]

@router.get("/analytics/overall-metrics")
def overall_metrics(user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = AnalyticsRepository(db)
    return [{"total_revenue": p.total_revenue, "total_revenue_change":p.total_revenue_change, "sales": p.sales,"sales_change":p.sales_change, "active_users": p.active_users, "active_users_change": p.active_users_change} for p in repo.get_overall_metrics()]