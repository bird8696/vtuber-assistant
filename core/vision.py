import base64
import os
import requests
from config import OLLAMA_URL, OLLAMA_MODEL

def analyze_with_vision(image_path: str, user_text: str) -> str:
    print("🔍 Qwen 로딩 중... (10~20초 걸려)")
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    # 파일 읽은 후 바로 삭제 (base64로 변환 완료된 시점)
    try:
        os.unlink(image_path)
    except:
        pass

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"너는 코딩 도우미야. 한국어로 짧고 핵심만 답해.\n\n유저 질문: {user_text}\n\n화면을 보고 문제점이나 개선점을 알려줘.",
        "images": [img_b64],
        "stream": False
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=300)
        data = res.json()
        print(f"🔍 Ollama 응답 raw: {list(data.keys())}")
        result = data.get("response") or data.get("message") or str(data)
        if not result:
            result = "분석 결과 없음"
    except Exception as e:
        result = f"에러: {e}"

    print("✅ Qwen 분석 완료")
    return result