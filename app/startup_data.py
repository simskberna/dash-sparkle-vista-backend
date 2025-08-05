# app/startup_data.py
from app.database import SessionLocal
from app.models.user import User
from app.auth import get_password_hash


def init_data():
    """Initialize default data - safe for multiple calls"""
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin_user = db.query(User).filter(User.email == "admin@admin.com").first()

        if not admin_user:
            # Create admin user
            admin_user = User(
                email="admin@admin.com",
                password_hash=get_password_hash("admin123"),
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created")
        else:
            print("Admin user already exists")

    except Exception as e:
        print(f"Error initializing data: {e}")
        db.rollback()
    finally:
        db.close()