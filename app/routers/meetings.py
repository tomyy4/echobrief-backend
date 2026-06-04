from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, status, Depends
from sqlmodel import Session, select
import uuid

from app.core.database import get_session
from app.models.meeting import MeetingTask
from app.schemas.meeting import MeetingAnalysis, MeetingTitleResponse, MeetingUpload, TaskResponse
from app.services.ollama import analyze_transcript_with_ollama

router = APIRouter(prefix="/meetings", tags=["Meetings"])


@router.get("/tasks/")
async def get_all_meeting_tasks(
    session: Session = Depends(get_session),
    limit: int = Query(default=50, le=100)
    ):
    
    statement = select(MeetingTask.id, MeetingTask.title, MeetingTask.status).limit(limit)
    tasks = session.exec(statement).all()
    return [MeetingTitleResponse(id=row[0], title=row[1], status=row[2]) for row in tasks]


def task_process_meeting(task_id: str, transcript: str, engine_instance):
    """Process the LLM in the background with its own db session"""
    with Session(engine_instance) as session:

        task = session.get(MeetingTask, task_id)
        if not task:
            return

        try:
            analysis: MeetingAnalysis = analyze_transcript_with_ollama(transcript)
            
            task.status = "COMPLETED"
            task.result = analysis.model_dump()
        except Exception as e:
            task.status = "FAILED"
            task.error = str(e)
        
        session.add(task)
        session.commit()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_meeting(
    payload: MeetingUpload, 
    background_tasks: BackgroundTasks, 
    session: Session = Depends(get_session)
):
    task_id = str(uuid.uuid4())
    
    # create the task in DB
    new_task = MeetingTask(
        id=task_id,
        title=payload.title,
        status="PROCESSING"
    )
    session.add(new_task)
    session.commit()
    
    background_tasks.add_task(task_process_meeting, task_id, payload.transcript, session.bind)
    
    return TaskResponse(task_id=task_id, status="PROCESSING")

@router.get("/{task_id}")
async def get_meeting_analysis(task_id: str, session: Session = Depends(get_session)):
    task = session.get(MeetingTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Análisis no encontrado")
    
    return {
        "title": task.title,
        "status": task.status,
        "result": task.result,
        "error": task.error
    }