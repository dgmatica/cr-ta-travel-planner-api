from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import places, projects

app = FastAPI(
    title="Travel Planner API",
    description="API for managing travel projects and places.",
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "Travel Planner API is online"}


app.include_router(projects.router)
app.include_router(places.router)
