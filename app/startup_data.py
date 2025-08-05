# app/startup_data.py
from app.database import SessionLocal, Base, engine
from app.models.analytics import Revenue, DeviceUsage, ProductPerformance, OverallMetrics
from app.models.user import User
from app.auth import get_password_hash
import traceback


def init_data():
    """Initialize default data - safe for multiple calls"""
    print("Starting data initialization...")

    try:
        # Önce tabloları oluştur
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")

        db = SessionLocal()

        try:
            # Revenue data
            if not db.query(Revenue).first():
                print("Adding revenue data...")
                revenue_data = [
                    Revenue(month="Jan", revenue=4000, growth=5),
                    Revenue(month="Feb", revenue=3000, growth=-2),
                    Revenue(month="Mar", revenue=7000, growth=10),
                ]
                db.add_all(revenue_data)
                db.commit()  # Her grup için commit
                print("Revenue data added")

            # Device usage data
            if not db.query(DeviceUsage).first():
                print("Adding device usage data...")
                device_data = [
                    DeviceUsage(device_type="Desktop", percentage=50),
                    DeviceUsage(device_type="Mobile", percentage=30),
                    DeviceUsage(device_type="Tablet", percentage=15),
                    DeviceUsage(device_type="Other", percentage=5),
                ]
                db.add_all(device_data)
                db.commit()
                print("Device usage data added")

            # Product performance data
            if not db.query(ProductPerformance).first():
                print("Adding product performance data...")
                product_data = [
                    ProductPerformance(product_name="Product A", sales=5000, revenue=2000),
                    ProductPerformance(product_name="Product B", sales=4500, revenue=2500),
                    ProductPerformance(product_name="Product C", sales=8000, revenue=3500),
                ]
                db.add_all(product_data)
                db.commit()
                print("Product performance data added")

            # Overall metrics data
            if not db.query(OverallMetrics).first():
                print("Adding overall metrics data...")
                metrics_data = [
                    OverallMetrics(
                        total_revenue=4523189,
                        total_revenue_change=20.1,
                        active_users=2350,
                        active_users_change=180.1,
                        sales=12234,
                        sales_change=19
                    ),
                ]
                db.add_all(metrics_data)
                db.commit()
                print("Overall metrics data added")

            print("Data initialization completed successfully!")
            return True

        except Exception as e:
            print(f"Error during data insertion: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            db.rollback()
            return False
        finally:
            db.close()

    except Exception as e:
        print(f"Error during table creation: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return False


def check_data():
    """Check if data exists - for debugging"""
    db = SessionLocal()
    try:
        revenue_count = db.query(Revenue).count()
        device_count = db.query(DeviceUsage).count()
        product_count = db.query(ProductPerformance).count()
        metrics_count = db.query(OverallMetrics).count()

        print(
            f"Data counts - Revenue: {revenue_count}, Devices: {device_count}, Products: {product_count}, Metrics: {metrics_count}")
        return {
            "revenue": revenue_count,
            "devices": device_count,
            "products": product_count,
            "metrics": metrics_count
        }
    except Exception as e:
        print(f"Error checking data: {e}")
        return None
    finally:
        db.close()

