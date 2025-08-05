from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_database_url():
    """Get database URL based on environment"""
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return database_url

    # Default SQLite database
    # In Vercel, use /tmp directory for temporary files
    if os.getenv("VERCEL"):
        return "sqlite:///tmp/app.db"
    else:
        return "sqlite:///./test.db"


DATABASE_URL = get_database_url()

# Create engine with appropriate settings
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False  # Set to True for SQL debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Helper function to initialize database
def init_database():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print(f"Database initialized at: {DATABASE_URL}")
        return True
    except Exception as e:
        print(f"Database initialization failed: {e}")
        return False