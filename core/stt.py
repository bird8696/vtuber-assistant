import sounddevice as sd
import numpy as np
import tempfile
import wave
import os
from faster_whisper import WhisperModel
from config import WHISPER_MODEL, SAMPLE_RATE, CHANNELS, RECORD_SECONDS

print("Whisper 로딩 중...")
_model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
print("Whisper 준비 완료")

def record_audio() -> str:
    print("\n🎤 말해봐 (5초)...")
    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16"
    )
    sd.wait()

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    with wave.open(tmp.name, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())
    return tmp.name

def transcribe(audio_path: str) -> str:
    segments, _ = _model.transcribe(audio_path, language="ko")
    text = "".join(s.text for s in segments).strip()
    os.unlink(audio_path)
    return text