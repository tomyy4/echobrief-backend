from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any
import json

class MeetingTask(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str
    status: str # PENDING, PROCESSING, COMPLETED, FAILED
    # Store the JSON as text
    result_json: Optional[str] = Field(default=None)
    error: Optional[str] = Field(default=None)

    @property
    def result(self) -> Optional[Dict[str, Any]]:
        """Return the stored text as JSON to let the API work with it"""
        if self.result_json:
            return json.loads(self.result_json)
        return None

    @result.setter
    def result(self, value: Dict[str, Any]):
        if value:
            self.result_json = json.dumps(value)