from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any
import uuid

from app.schemas.meeting import MeetingAnalysis
from app.services.ollama import analyze_transcript_with_ollama

router = APIRouter(prefix="/meetings", tags=["Meetings"])

# fake database
db_mock: Dict[str, Dict[str, Any]] = {}

class MeetingUpload(BaseModel):
    title: str
    transcript: str

class TaskResponse(BaseModel):
    task_id: str
    status: str

def task_process_meeting(task_id: str, transcript: str):
    try:
        analysis: MeetingAnalysis = analyze_transcript_with_ollama(transcript)
        
        db_mock[task_id]["status"] = "COMPLETED"
        db_mock[task_id]["result"] = analysis.model_dump()
    except Exception as e:
        db_mock[task_id]["status"] = "FAILED"
        db_mock[task_id]["error"] = str(e)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_meeting(payload: MeetingUpload, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    
    db_mock[task_id] = {
        "title": payload.title,
        "status": "PROCESSING",
        "result": None,
        "error": None
    }
    
    background_tasks.add_task(task_process_meeting, task_id, payload.transcript)
    
    return TaskResponse(task_id=task_id, status="PROCESSING")

@router.get("/{task_id}")
async def get_meeting_analysis(task_id: str):
    if task_id not in db_mock:
        raise HTTPException(status_code=404, detail="Análisis no encontrado")
    return db_mock[task_id]