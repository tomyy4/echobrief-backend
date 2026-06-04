from pydantic import BaseModel, Field
from typing import List

class Commitment(BaseModel):
    owner: str = Field(..., description="Name of the person that commits")
    task: str = Field(..., description="Detailed description of the task or commitment")
    deadline: str = Field(..., description="Deadline or 'No specified'")

class MeetingAnalysis(BaseModel):
    summary: str = Field(..., description="Summary of the meeting")
    sentiment: str = Field(..., description="General feeling (ex Productive, Tense, Colaborative)")
    key_topics: List[str] = Field(..., description="Subjects disscused")
    commitments: List[Commitment] = Field(..., description="Commitments detected")


class MeetingUpload(BaseModel):
    """Frontend Payload"""
    title: str
    transcript: str

class TaskResponse(BaseModel):
    task_id: str
    status: str