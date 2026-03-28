from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from app.environment import EmailEnvironment

app = FastAPI(title="Email OpenEnv")
env = EmailEnvironment()

class StepRequest(BaseModel):
    action: str

class ResetRequest(BaseModel):
    task_id: Optional[str] = None

@app.get("/")
def root():
    return {"status": "ok", "message": "Email OpenEnv is running!"}

@app.post("/reset")
def reset(request: ResetRequest = ResetRequest()):
    result = env.reset(task_id=request.task_id)
    return result

@app.post("/step")
def step(request: StepRequest):
    result = env.step(action=request.action)
    return result

@app.get("/state")
def state():
    return env.state()