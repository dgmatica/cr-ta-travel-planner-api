from fastapi import FastAPI

app = FastAPI(
    title="Travel Planner API",
    description="API for managing travel projects and places.",
)


@app.get("/")
def read_root():
    return {"message": "Travel Planner API is online"}
