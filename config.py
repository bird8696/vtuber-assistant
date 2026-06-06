import os

# ── STT ───────────────────────────────────────────
WHISPER_MODEL = "base"
SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 5

# ── 트리거 키워드 ──────────────────────────────────
TRIGGER_KEYWORDS = [
    "화면 봐줘", "화면에 봐줘", "화면을 봐줘",
    "봐줘", "훈수", "뭐가 문제야", "왜 안돼",
    "확인해줘", "뭐가 틀렸어", "어디가 문제야",
    "화면 봐", "이거 봐줘"
]

# ── Vision LLM (Ollama) ───────────────────────────
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5vl:7b"

# ── GPT-SoVITS ────────────────────────────────────
GPTSOVITS_URL = "http://127.0.0.1:9880/tts"
GPTSOVITS_REF_AUDIO = r"E:\my_fun_boot\GPT-SoVITS\output\slicer_opt\2024 타비 보이스.mp3_0000028480_0000173120.wav"
GPTSOVITS_REF_TEXT = "안녕~뿡빵띠~ 바람을 가르고"
GPTSOVITS_REF_LANG = "ko"

# ── 화면 캡처 ─────────────────────────────────────
MONITOR_INDEX = 1
CAPTURE_RESIZE = (1280, 720)

# ── LLM 일상대화 ──────────────────────────────────
OLLAMA_CHAT_URL = "http://localhost:11434/api/generate"
OLLAMA_CHAT_MODEL = "gemma3:4b"

# ── 류아 먼저 말걸기 간격 (초) ────────────────────
PROACTIVE_INTERVAL = 120