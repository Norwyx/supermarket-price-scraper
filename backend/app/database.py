from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

# Create the database engine
# echo=True will log generated SQL, useful for debugging
engine = create_engine(settings.DATABASE_URL, echo=True)

def get_session():
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Create the database tables based on the models."""
    SQLModel.metadata.create_all(engine)
