import pytest
from sqlmodel import Session, create_engine, SQLModel
from app.config import settings


@pytest.fixture(scope="session")
def engine():
    return create_engine(settings.DATABASE_URL)


@pytest.fixture(scope="session", autouse=True)
def setup_database(engine):
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield


@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    
    yield session 
    
    session.close()
    transaction.rollback()
    connection.close()