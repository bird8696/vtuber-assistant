import requests as req
from core.stt import record_audio, transcribe
from core.capture import capture_screen
from core.vision import analyze_with_vision
from core.tts import speak
from config import TRIGGER_KEYWORDS

BRIDGE_URL = "http://localhost:8765"

def update_overlay(message: str, status: str = "대기 중..."):
    try:
        req.post(f"{BRIDGE_URL}/update", json={"message": message, "status": status}, timeout=2)
    except:
        pass

def has_trigger(text: str) -> bool:
    return any(kw in text for kw in TRIGGER_KEYWORDS)

def main():
    print("\n✅ 파이프라인 시작. 말해봐뿡빵띠\n")
    while True:
        try:
            update_overlay("화면 봐줘 라고 말해봐뿡빵띠", "대기 중...")
            audio_path = record_audio()
            text = transcribe(audio_path)

            if not text:
                print("(인식 안됨)")
                continue

            print(f"📝 인식: {text}")

            if has_trigger(text):
                update_overlay("화면 분석 중...", "분석 중...")
                image_path = capture_screen()
                response = analyze_with_vision(image_path, text)
            else:
                print("(트리거 없음, 다시 대기)")
                continue

            print(f"💬 응답: {response}")
            update_overlay(response, "말하는 중...")
            speak(response)

        except KeyboardInterrupt:
            print("\n종료뿡빵띠")
            break
        except Exception as e:
            print(f"❌ 에러: {e}")
            continue

if __name__ == "__main__":
    import threading
    import uvicorn
    from bridge.server import app

    def run_bridge():
        uvicorn.run(app, host="localhost", port=8765, log_level="error")

    t = threading.Thread(target=run_bridge, daemon=True)
    t.start()

    main()