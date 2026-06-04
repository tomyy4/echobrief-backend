import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool
from app.main import app
from app.core.database import get_session
from app.schemas.meeting import MeetingAnalysis

DATABASE_URL = "sqlite:///:memory:"
engine_test = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool 
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine_test) 
    with Session(engine_test) as session:
        yield session
    SQLModel.metadata.drop_all(engine_test) 

@pytest.fixture(name="client")
def client_fixture(session):
    def _get_session_override():
        yield session

    app.dependency_overrides[get_session] = _get_session_override
    
    with TestClient(app) as client:
        yield client
        
    app.dependency_overrides.clear()

@pytest.fixture
def mock_meeting_analysis():
    return MeetingAnalysis(
        summary="Reunión de prueba exitosa.",
        sentiment="Positivo",
        key_topics=["Testing", "FastAPI"],
        commitments=[
            {"owner": "Tester", "task": "Escribir pruebas unitarias", "deadline": "Hoy"}
        ]
    )