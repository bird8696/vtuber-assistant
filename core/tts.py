import tempfile
import os
import requests
import sounddevice as sd
import soundfile as sf
from config import GPTSOVITS_URL, GPTSOVITS_REF_AUDIO, GPTSOVITS_REF_TEXT, GPTSOVITS_REF_LANG

def speak(text: str):
    print("🔊 TTS 생성 중...")
    payload = {
        "text": text,
        "text_lang": GPTSOVITS_REF_LANG,
        "ref_audio_path": GPTSOVITS_REF_AUDIO,
        "prompt_text": GPTSOVITS_REF_TEXT,
        "prompt_lang": GPTSOVITS_REF_LANG,
        "media_type": "wav",
        "streaming_mode": False
    }

    res = requests.post(GPTSOVITS_URL, json=payload, timeout=60)
    if res.status_code == 200:
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp.write(res.content)
        tmp.close()
        data, fs = sf.read(tmp.name)
        sd.play(data, fs)
        sd.wait()
        os.unlink(tmp.name)
        print("✅ 음성 출력 완료")
    else:
        print(f"❌ TTS 실패: {res.status_code} {res.text}")