import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine
from app.main import app
from db import get_session
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DATABASE_URL')
engine = create_engine(
    db_url, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
    )

@pytest.fixture(name="session")
def session_fixture(engine):
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
async def client_fixture(session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()