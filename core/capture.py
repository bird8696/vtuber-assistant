import tempfile
import mss
from PIL import Image
from config import MONITOR_INDEX, CAPTURE_RESIZE

def capture_screen() -> str:
    print("🖥 화면 캡처 중...")
    with mss.mss() as sct:
        monitor = sct.monitors[MONITOR_INDEX]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img = img.resize(CAPTURE_RESIZE)
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img.save(tmp.name)
        print(f"✅ 캡처 완료: {tmp.name}")
        return tmp.name