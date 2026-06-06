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

state = {
    "messages": [],
    "mouth": 0.0,
    "expression": -1,
    "text_input": "",
    "voice_trigger": False
}

class ChatMessage(BaseModel):
    role: str
    content: str

class Mouth(BaseModel):
    value: float

class Expression(BaseModel):
    index: int

class TextInput(BaseModel):
    text: str

@app.post("/chat")
def add_chat(msg: ChatMessage):
    state["messages"].append({"role": msg.role, "content": msg.content})
    if len(state["messages"]) > 50:
        state["messages"] = state["messages"][-50:]
    return {"ok": True}

@app.post("/mouth")
def mouth(m: Mouth):
    state["mouth"] = max(0.0, min(1.0, m.value))
    return {"ok": True}

@app.post("/expression")
def expression(e: Expression):
    state["expression"] = e.index
    return {"ok": True}

@app.post("/text_input")
def text_input(t: TextInput):
    state["text_input"] = t.text
    return {"ok": True}

@app.post("/trigger_voice")
def trigger_voice():
    state["voice_trigger"] = True
    return {"ok": True}

@app.get("/latest")
def get_latest():
    return state

@app.get("/pop_text_input")
def pop_text_input():
    text = state["text_input"]
    state["text_input"] = ""
    return {"text": text}

@app.get("/pop_voice_trigger")
def pop_voice_trigger():
    triggered = state["voice_trigger"]
    state["voice_trigger"] = False
    return {"triggered": triggered}