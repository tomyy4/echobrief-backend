import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routers.meetings import db_mock
from app.schemas.meeting import MeetingAnalysis

client = TestClient(app)

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

def test_upload_meeting_success(mocker, mock_meeting_analysis):
    mocker.patch(
        "app.routers.meetings.analyze_transcript_with_ollama",
        return_value=mock_meeting_analysis
    )

    payload = {
        "title": "Daily Test",
        "transcript": "Tester dice que hay que escribir pruebas hoy."
    }

    response = client.post("/api/v1/meetings/", json=payload)
    
    assert response.status_code == 202
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "PROCESSING"

    task_id = data["task_id"]
    assert db_mock[task_id]["status"] == "COMPLETED"
    assert db_mock[task_id]["result"]["sentiment"] == "Positivo"


def test_get_meeting_not_found():
    response = client.get("/api/v1/meetings/id-inexistente")
    assert response.status_code == 404
    assert response.json()["detail"] == "Análisis no encontrado"