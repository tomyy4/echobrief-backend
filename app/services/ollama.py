import instructor
from openai import OpenAI
from app.schemas.meeting import MeetingAnalysis

client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama", # Ignored by ollama
    ),
    mode=instructor.Mode.JSON
)

def analyze_transcript_with_ollama(transcript: str) -> MeetingAnalysis:
    response = client.chat.completions.create(
        model="llama3.2",
        response_model=MeetingAnalysis,
        messages=[
            {"role": "system", "content": "Eres un asistente experto en analizar transcripciones de reuniones corporativas."},
            {"role": "user", "content": f"Analiza la siguiente transcripción:\n\n{transcript}"}
        ],
    )
    return response