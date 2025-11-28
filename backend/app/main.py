from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the database tables on startup
    create_db_and_tables()
    yield

app = FastAPI(
    title="Supermarket Price Scraper",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "Server working correctly!"}
