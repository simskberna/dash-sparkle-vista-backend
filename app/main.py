from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

# Import database and models
from app.database import Base, engine
from app.routes import auth_routes, user_routes, analytics_routes, activity_routes
from app.startup_data import init_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - Create tables and init data
    try:
        Base.metadata.create_all(bind=engine)
        init_data()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")

    yield

    # Shutdown
    print("Application shutting down")


# Create FastAPI app
app = FastAPI(
    title="FastAPI Auth & Dashboard API",
    description="Your API Description",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da specific domains kullan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(analytics_routes.router, prefix="/user", tags=["Analytics"])
app.include_router(activity_routes.router, prefix="/user", tags=["Activity"])


@app.get("/")
async def root():
    return {
        "message": "FastAPI Auth & Dashboard API is running!",
        "status": "healthy",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Local development
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )