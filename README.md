# 🧭 vtuber-assistant

화면을 보고 훈수를 놓는 AI 버튜버 어시스턴트.  
"화면 봐줘" 라고 말하면 현재 화면을 분석해서 음성으로 피드백을 준다.

---

## 📺 데모

> 추후 추가 예정

---

## 🏗 구조

```
vtuber-assistant/
├── core/
│   ├── stt.py        # 음성 인식 (faster-whisper)
│   ├── capture.py    # 화면 캡처 (mss)
│   ├── vision.py     # 화면 분석 (Qwen2.5-VL)
│   └── tts.py        # 음성 출력 (GPT-SoVITS)
├── bridge/
│   └── server.py     # FastAPI 브릿지 서버
├── overlay/
│   ├── main.js       # Electron 메인
│   ├── preload.js    # Electron preload
│   ├── index.html    # 오버레이 UI
│   └── package.json
├── config.py         # 설정값
├── main.py           # 진입점
└── start.bat         # 한번에 실행
```

---

## ⚙️ 전체 흐름

```
음성 입력 (마이크)
    ↓
STT — faster-whisper (로컬)
    ↓
트리거 키워드 감지 ("화면 봐줘" 등)
    ↓
화면 캡처 — mss
    ↓
Vision 분석 — Qwen2.5-VL (Ollama 로컬)
    ↓
FastAPI 브릿지 → Electron 말풍선 업데이트
    ↓
TTS — GPT-SoVITS (로컬)
    ↓
음성 출력
```

---

## 🖥 요구 사양

| 항목    | 권장 사양                             |
| ------- | ------------------------------------- |
| OS      | Windows 11                            |
| GPU     | NVIDIA RTX 3060 Ti 8GB 이상           |
| VRAM    | 8GB (백그라운드 프로세스 최소화 권장) |
| Python  | 3.11                                  |
| Node.js | 22+                                   |

---

## 📦 설치

### 1. Python 환경 세팅

```bash
conda create -n vtuber-assistant python=3.11 -y
conda activate vtuber-assistant
pip install faster-whisper mss pillow requests sounddevice numpy fastapi uvicorn soundfile
```

### 2. Ollama 설치 및 모델 다운로드

[https://ollama.com/download/windows](https://ollama.com/download/windows) 에서 설치 후

```bash
ollama pull qwen2.5vl:7b
```

### 3. GPT-SoVITS 설치

별도 설치 필요. 설치 후 `config.py` 에서 경로 설정.

### 4. Electron 설치

```bash
cd overlay
npm install
```

---

## ⚙️ 설정

`config.py` 에서 아래 값 수정

```python
# GPT-SoVITS 참조 오디오 경로
GPTSOVITS_REF_AUDIO = r"경로\참조오디오.wav"
GPTSOVITS_REF_TEXT = "참조 오디오 텍스트"

# Vision 모델 (VRAM 부족시 qwen2.5vl:3b 로 변경)
OLLAMA_MODEL = "qwen2.5vl:7b"

# 트리거 키워드
TRIGGER_KEYWORDS = ["화면 봐줘", "봐줘", "훈수", "뭐가 문제야", "왜 안돼", "확인해줘"]
```

---

## 🚀 실행

### 방법 1 — 배치파일 (권장)

`start.bat` 더블클릭

### 방법 2 — 수동 실행

**터미널 1 — GPT-SoVITS 서버**

```bash
conda activate GPTSoVits
cd E:\my_fun_boot\GPT-SoVITS
python api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml
```

**터미널 2 — Electron 오버레이**

```bash
cd overlay
npm start
```

**터미널 3 — 파이프라인**

```bash
conda activate vtuber-assistant
python main.py
```

---

## ⚠️ 트러블슈팅

| 증상                           | 원인                    | 해결                                                  |
| ------------------------------ | ----------------------- | ----------------------------------------------------- |
| Vision 분석 실패 (메모리 부족) | VRAM 부족               | VirtualBox 등 종료 후 재시도 또는 `qwen2.5vl:3b` 사용 |
| TTS 실패 400 에러              | GPT-SoVITS 서버 미실행  | `start.bat` 또는 수동으로 서버 먼저 실행              |
| 포트 9880 충돌                 | 이전 서버 프로세스 잔존 | `taskkill /PID [PID번호] /F` 로 종료                  |
| 트리거 인식 안됨               | STT 인식 오류           | `config.py` 에서 트리거 키워드 추가                   |

---

## 🗺 로드맵

- [x] Phase 1 — STT + 화면캡처 + Vision + TTS 파이프라인
- [x] Phase 2 — Electron 투명 오버레이 창
- [x] Phase 3 — 파이프라인 ↔ 오버레이 연결
- [ ] Phase 4 — Live2D 모델 연결 + 립싱크

---

## 📝 라이선스

MIT
