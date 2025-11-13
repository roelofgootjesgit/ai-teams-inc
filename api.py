from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from ai_team import AITeam

app = FastAPI()

# Serve frontend static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

# Request model
class ChatRequest(BaseModel):
    message: str

# Initialize AI team
team = AITeam()

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Endpoint for AI team queries
    Returns formatted response from AI agents
    """
    try:
        result = team.run(request.message)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)