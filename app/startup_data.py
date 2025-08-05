from app.database import Base, engine, SessionLocal
from app.models.analytics import Revenue, DeviceUsage, ProductPerformance, OverallMetrics


def init_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if not db.query(Revenue).first():
        db.add_all([
            Revenue(month="Jan", revenue=4000, growth=5),
            Revenue(month="Feb", revenue=3000, growth=-2),
            Revenue(month="Mar", revenue=7000, growth=10),
        ])

    if not db.query(DeviceUsage).first():
        db.add_all([
            DeviceUsage(device_type="Desktop", percentage=50),
            DeviceUsage(device_type="Mobile", percentage=30),
            DeviceUsage(device_type="Tablet", percentage=15),
            DeviceUsage(device_type="Other", percentage=5),
        ])

    if not db.query(ProductPerformance).first():
        db.add_all([
            ProductPerformance(product_name="Product A", sales=5000, revenue=2000),
            ProductPerformance(product_name="Product B", sales=4500, revenue=2500),
            ProductPerformance(product_name="Product C", sales=8000, revenue=3500),
        ])

    if not db.query(OverallMetrics).first():
        db.add_all([
            OverallMetrics(total_revenue=4523189,total_revenue_change=20.1,active_users=2350, active_users_change=180.1, sales=12234, sales_change=19),
        ])

    db.commit()
    db.close()
