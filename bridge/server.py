from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

latest = {"message": "", "status": "대기 중..."}

class Message(BaseModel):
    message: str
    status: str = "대기 중..."

@app.post("/update")
def update(msg: Message):
    latest["message"] = msg.message
    latest["status"] = msg.status
    return {"ok": True}

@app.get("/latest")
def get_latest():
    return latest