# vtuber-assistant

화면 위에 상주하는 AI 버튜버 어시스턴트. 고대 용족 소녀 류아가 코딩을 도와주고 일상 대화를 나눈다.

---

## 스크린샷

**전체 화면**

![overview](메인화면.png)

**류아 모델**

![model](류아모델.png)

**채팅창**

![chat](채팅창.png)

**실행 방법**

![how-to-run](실행방법.png)

---

## 시연 영상

[![demo](메인화면.png)](시연영상.mp4)

> 시연영상.mp4 참고

---

## 기능

- 음성 대화 — 마이크 버튼 클릭 후 말하면 음성 인식 후 류아가 답변
- 텍스트 대화 — 채팅창에 직접 입력해서 대화
- 화면 분석 — "화면 봐줘" 라고 말하면 현재 화면을 분석해서 피드백
- 감정 표현 — 대화 내용에 따라 류아 표정 자동 변경
- 립싱크 — TTS 음성 출력 중 입 모양 실시간 연동
- 먼저 말걸기 — 일정 시간이 지나면 류아가 먼저 말을 걺
- 자유 배치 — 모델창/채팅창 드래그로 위치 조정, 휠로 크기 조절

---

## 구조

```
vtuber-assistant/
├── core/
│   ├── stt.py        # 음성 인식 (faster-whisper)
│   ├── capture.py    # 화면 캡처 (mss)
│   ├── vision.py     # 화면 분석 (Qwen2.5-VL)
│   ├── tts.py        # 음성 출력 + 립싱크 (GPT-SoVITS)
│   └── llm.py        # 일상 대화 + 감정 분석 (gemma3:4b)
├── bridge/
│   └── server.py     # FastAPI 브릿지 서버
├── overlay/
│   ├── main.js       # Electron 메인
│   ├── bubble.html   # 채팅창
│   ├── model.html    # Live2D 모델
│   └── package.json
├── config.py
├── main.py
└── start.bat
```

---

## 흐름

```
텍스트 입력 or 음성 입력
        |
트리거 키워드 감지?
   |          |
  Yes         No
   |          |
화면 캡처   일상 대화 LLM (gemma3:4b)
   |          |
Vision 분석  감정 분석 -> 표정 변경
   |          |
   +----------+
        |
  FastAPI 브릿지
        |
  채팅창 업데이트
        |
  TTS + 립싱크
```

---

## 요구 사양

| 항목    | 사양                        |
| ------- | --------------------------- |
| OS      | Windows 11                  |
| GPU     | NVIDIA RTX 3060 Ti 8GB 이상 |
| Python  | 3.11                        |
| Node.js | 22+                         |

---

## 설치

### 1. Python 환경

```bash
conda create -n vtuber-assistant python=3.11 -y
conda activate vtuber-assistant
pip install faster-whisper mss pillow requests sounddevice numpy fastapi uvicorn soundfile
```

### 2. Ollama 모델

```bash
ollama pull qwen2.5vl:7b
ollama pull gemma3:4b
```

### 3. GPT-SoVITS

별도 설치 후 `config.py` 경로 설정.

### 4. Cubism 코어

```powershell
Invoke-WebRequest -Uri "https://cubism.live2d.com/sdk-web/cubismcore/live2dcubismcore.min.js" -OutFile "overlay/live2dcubismcore.min.js"
```

### 5. Electron

```bash
cd overlay
npm install
```

---

## 설정

`config.py` 수정

```python
# GPT-SoVITS 참조 오디오
GPTSOVITS_REF_AUDIO = r"경로\참조오디오.wav"
GPTSOVITS_REF_TEXT = "참조 오디오 텍스트"

# Live2D 모델 경로 (overlay/model.html 에서 수정)
MODEL_PATH = 'E:/path/to/model.model3.json'

# 류아가 먼저 말거는 간격 (초)
PROACTIVE_INTERVAL = 120
```

---

## 실행

**1. GPT-SoVITS 서버**

`start.bat` 더블클릭

**2. Electron 오버레이**

```bash
cd overlay
npm start
```

**3. 파이프라인**

```bash
conda activate vtuber-assistant
python main.py
```

---

## 사용법

| 방법        | 설명                                |
| ----------- | ----------------------------------- |
| 텍스트 입력 | 채팅창 입력창에 타이핑 후 Enter     |
| 음성 입력   | 마이크 버튼 클릭 후 5초 안에 말하기 |
| 화면 분석   | "화면 봐줘", "뭐가 문제야" 등       |
| 모델 이동   | 캔버스 드래그                       |
| 모델 크기   | 마우스 휠                           |
| 창 이동     | 상단 핸들 드래그                    |

---

## 트러블슈팅

| 증상                 | 원인                   | 해결                               |
| -------------------- | ---------------------- | ---------------------------------- |
| Vision 분석 실패     | VRAM 부족              | 백그라운드 프로세스 종료 후 재시도 |
| TTS 400 에러         | GPT-SoVITS 서버 미실행 | start.bat 먼저 실행                |
| 포트 9880 충돌       | 이전 서버 잔존         | `taskkill /PID [PID] /F`           |
| 채팅창 업데이트 안됨 | bridge 서버 미실행     | python main.py 확인                |

---

## 로드맵

- [x] Phase 1 — STT + 화면캡처 + Vision + TTS
- [x] Phase 2 — Electron 투명 오버레이
- [x] Phase 3 — 파이프라인 연결
- [x] Phase 4 — Live2D + 립싱크 + 감정 표현
- [x] Phase 5 — 일상 대화 + 텍스트 입력 + 페르소나
- [ ] Phase 6 — 시작 자동화
- [ ] Phase 7 — 품질 개선
- [ ] Phase 8 — 포트폴리오 마무리

---

## 라이선스

MIT

---

## 크레딧

### Live2D 모델

본 프로젝트에서 사용한 Live2D 모델은 **絵夢社(huimengxue)** 님의 작품입니다.

모델을 정식 구매하여 사용하고 있으며, 본 프로젝트는 개인 학습 및 포트폴리오 목적으로만 제작되었습니다. **상업적 목적으로 사용하지 않습니다.**

| 플랫폼   | 링크                                                                |
| -------- | ------------------------------------------------------------------- |
| Twitter  | [@huimengxue3745](https://twitter.com/huimengxue3745)               |
| pixiv    | [pixiv](https://www.pixiv.net)                                      |
| BOOTH    | [huimengshe.booth.pm](https://huimengshe.booth.pm/)                 |
| BiliBili | [bilibili](https://space.bilibili.com/3493085814196605)             |
| YouTube  | [YouTube](https://www.youtube.com/channel/UCMTP_CKGDKXGRuhzedCtyeQ) |

> Copyright © 絵夢社. All rights reserved.  
> This model is used for non-commercial, personal purposes only.
