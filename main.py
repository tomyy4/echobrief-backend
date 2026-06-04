from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello goodbye"}




@app.get("/briefs")
async def briefs():
    return {"message": "Returning briefs"}