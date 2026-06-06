import tempfile
import time
import mss
import requests
from PIL import Image
from config import MONITOR_INDEX, CAPTURE_RESIZE

OVERLAY_URL = "http://localhost:8766"

def capture_screen() -> str:
    print("🖥 화면 캡처 중...")
    try:
        requests.post(f"{OVERLAY_URL}/hide", timeout=1)
        time.sleep(0.3)
    except:
        pass

    with mss.mss() as sct:
        monitor = sct.monitors[MONITOR_INDEX]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img = img.resize(CAPTURE_RESIZE)
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img.save(tmp.name)

    try:
        requests.post(f"{OVERLAY_URL}/show", timeout=1)
    except:
        pass

    print(f"✅ 캡처 완료: {tmp.name}")
    return tmp.name