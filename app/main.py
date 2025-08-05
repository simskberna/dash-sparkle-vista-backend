from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth_routes, user_routes, analytics_routes, activity_routes
from app.startup_data import init_data

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Auth & Dashboard API")

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(analytics_routes.router, prefix="/user", tags=["Analytics"])
app.include_router(activity_routes.router, prefix="/user", tags=["Activity"])

@app.on_event("startup")
def startup_event():
    init_data()
