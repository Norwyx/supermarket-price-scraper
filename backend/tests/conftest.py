import pytest
from sqlmodel import Session, create_engine
from app.config import settings

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(settings.DATABASE_URL)
    connection = engine.connect()
    transaction = connection.begin()
    
    session = Session(bind=connection)
    
    yield session 
    
    session.close()
    transaction.rollback() 
    connection.close()