import threading
import time
import requests as req
import uvicorn
from core.stt import record_audio, transcribe
from core.capture import capture_screen
from core.vision import analyze_with_vision
from core.tts import speak
from core.llm import chat, get_proactive_line
from core.vts import vts_connect, vts_set_expression
from config import TRIGGER_KEYWORDS, PROACTIVE_INTERVAL
from bridge.server import app

BRIDGE_URL = "http://localhost:8765"
lock = threading.Lock()

def update_overlay(role: str, content: str):
    try:
        req.post(f"{BRIDGE_URL}/chat", json={"role": role, "content": content}, timeout=2)
    except:
        pass

def send_expression(index: int):
    try:
        req.post(f"{BRIDGE_URL}/expression", json={"index": index}, timeout=2)
        vts_set_expression(index)
    except:
        pass

def has_trigger(text: str) -> bool:
    return any(kw in text for kw in TRIGGER_KEYWORDS)

def handle_input(text: str):
    with lock:
        update_overlay("user", text)
        if has_trigger(text):
            update_overlay("assistant", "화면 분석 중...")
            image_path = capture_screen()
            response = analyze_with_vision(image_path, text)
            send_expression(-1)
        else:
            response, expression = chat(text)
            send_expression(expression)
        print(f"💬 응답: {response}")
        update_overlay("assistant", response)
        speak(response)

def proactive_loop():
    time.sleep(30)
    while True:
        time.sleep(PROACTIVE_INTERVAL)
        if not lock.locked():
            line, expression = get_proactive_line()
            print(f"💬 류아 먼저 말걸기: {line}")
            update_overlay("assistant", line)
            send_expression(expression)
            speak(line)

def text_input_loop():
    while True:
        try:
            res = req.get(f"{BRIDGE_URL}/pop_text_input", timeout=2)
            text = res.json().get("text", "").strip()
            if text:
                print(f"⌨️ 텍스트 입력: {text}")
                threading.Thread(target=handle_input, args=(text,), daemon=True).start()
        except:
            pass
        time.sleep(0.5)

def voice_loop():
    while True:
        try:
            res = req.get(f"{BRIDGE_URL}/pop_voice_trigger", timeout=2)
            triggered = res.json().get("triggered", False)
            if triggered:
                print("🎤 음성 입력 활성화")
                update_overlay("assistant", "듣고 있어~ 말해봐 🎤")
                audio_path = record_audio()
                text = transcribe(audio_path)
                if text:
                    print(f"📝 인식: {text}")
                    threading.Thread(target=handle_input, args=(text,), daemon=True).start()
                else:
                    print("(인식 안됨)")
                    update_overlay("assistant", "잘 못 들었어, 다시 말해줘 😅")
        except:
            pass
        time.sleep(0.3)

def main():
    print("\n✅ 파이프라인 시작. 말해봐뿡빵띠\n")

    print("🔌 VTube Studio 연결 중...")
    vts_connect()

    threading.Thread(target=proactive_loop, daemon=True).start()
    threading.Thread(target=text_input_loop, daemon=True).start()
    threading.Thread(target=voice_loop, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n종료뿡빵띠")

if __name__ == "__main__":
    def run_bridge():
        uvicorn.run(app, host="localhost", port=8765, log_level="error")

    t = threading.Thread(target=run_bridge, daemon=True)
    t.start()
    time.sleep(1)
    main()