import tempfile
import os
import requests
import sounddevice as sd
import soundfile as sf
import numpy as np
from config import GPTSOVITS_URL, GPTSOVITS_REF_AUDIO, GPTSOVITS_REF_TEXT, GPTSOVITS_REF_LANG

BRIDGE_URL = "http://localhost:8765"

def send_mouth(value: float):
    try:
        requests.post(f"{BRIDGE_URL}/mouth", json={"value": value}, timeout=0.5)
    except:
        pass

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

        data, fs = sf.read(tmp.name, dtype='float32')
        chunk_size = int(fs * 0.05)
        total_frames = len(data)
        pos = 0

        with sd.OutputStream(samplerate=fs, channels=1 if data.ndim == 1 else data.shape[1], dtype='float32') as stream:
            while pos < total_frames:
                chunk = data[pos:pos + chunk_size]
                if len(chunk) == 0:
                    break

                vol = float(np.abs(chunk).mean())
                vol = min(1.0, vol * 8)
                send_mouth(vol)

                stream.write(chunk.reshape(-1, 1) if data.ndim == 1 else chunk)
                pos += chunk_size

        send_mouth(0.0)
        os.unlink(tmp.name)
        print("✅ 음성 출력 완료")
    else:
        print(f"❌ TTS 실패: {res.status_code} {res.text}")