from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import meetings

app = FastAPI(
    title="EchoBrief API",
    description="Backend asíncrono para estructurar reuniones con Ollama e Instructor",
    version="1.0.0"
)

# will point tou our frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meetings.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"status": "online", "message": "EchoBrief Backend está listo"}