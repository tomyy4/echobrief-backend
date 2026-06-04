from app.models.meeting import MeetingTask

def test_upload_meeting_success(client, session, mocker, mock_meeting_analysis):
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

  
    task_in_db = session.get(MeetingTask, task_id)
    
    assert task_in_db is not None
    assert task_in_db.status == "COMPLETED"
    assert task_in_db.title == "Daily Test"
    assert task_in_db.result["sentiment"] == "Positivo"
    assert len(task_in_db.result["commitments"]) == 1


def test_get_meeting_not_found(client):
    response = client.get("/api/v1/meetings/not-existing")
    assert response.status_code == 404
    assert response.json()["detail"] == "Análisis no encontrado"


def test_get_all_meeting_titles(client, session):
    task1 = MeetingTask(id="1", title="Reunión A", status="COMPLETED")
    task2 = MeetingTask(id="2", title="Reunión B", status="PROCESSING")
    session.add(task1)
    session.add(task2)
    session.commit()

    response = client.get("/api/v1/meetings/tasks/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Reunión A"
    assert "result_json" not in data[0] 