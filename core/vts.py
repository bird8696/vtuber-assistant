import asyncio
import websockets
import json
import threading
import os

VTS_URL = "ws://localhost:8001"
PLUGIN_NAME = "vtuber-assistant"
PLUGIN_DEVELOPER = "bird8696"
TOKEN_FILE = "vts_token.txt"

class VTSClient:
    def __init__(self):
        self.ws = None
        self.token = None
        self.connected = False
        self.loop = asyncio.new_event_loop()
        self.lock = asyncio.Lock()
        threading.Thread(target=self._run_loop, daemon=True).start()

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def _run(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self.loop).result(timeout=10)

    async def _request(self, msg_type: str, data: dict = {}) -> dict:
        async with self.lock:
            payload = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "req1",
                "messageType": msg_type,
                "data": data
            }
            await self.ws.send(json.dumps(payload))
            res = await self.ws.recv()
            return json.loads(res)

    async def _connect_and_auth(self):
        self.ws = await websockets.connect(VTS_URL)
        self.connected = True
        print("✅ VTube Studio 연결 완료")

        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                self.token = f.read().strip()
            print("🔑 저장된 토큰 사용")
        else:
            res = await self._request("AuthenticationTokenRequest", {
                "pluginName": PLUGIN_NAME,
                "pluginDeveloper": PLUGIN_DEVELOPER
            })
            self.token = res["data"]["authenticationToken"]
            with open(TOKEN_FILE, "w") as f:
                f.write(self.token)
            print("🔑 새 토큰 발급 및 저장")

        res = await self._request("AuthenticationRequest", {
            "pluginName": PLUGIN_NAME,
            "pluginDeveloper": PLUGIN_DEVELOPER,
            "authenticationToken": self.token
        })
        authenticated = res["data"]["authenticated"]

        if not authenticated:
            os.remove(TOKEN_FILE)
            self.token = None
            print("🔑 토큰 만료, 재발급 중...")
            await self._connect_and_auth()
            return

        print("🔑 인증 성공")

    def _reset_all_expressions(self):
        print("🔄 표정 초기화 중...")
        for i in range(1, 10):
            try:
                self.set_expression(f"expression{i}.exp3.json", False)
            except:
                pass
        # 눈 강제로 열기
        self.set_parameter("ParamEyeLOpen", 1.0)
        self.set_parameter("ParamEyeROpen", 1.0)
        print("✅ 표정 초기화 완료")

    def connect(self):
        try:
            self._run(self._connect_and_auth())
            self._reset_all_expressions()
        except Exception as e:
            print(f"❌ VTS 연결 실패: {e}")
            self.connected = False

    def set_expression(self, expression_file: str, active: bool = True):
        if not self.connected:
            return
        try:
            self._run(self._request("ExpressionActivationRequest", {
                "expressionFile": expression_file,
                "active": active
            }))
        except Exception as e:
            print(f"❌ VTS 표정 실패: {e}")

    def set_parameter(self, param_id: str, value: float):
        if not self.connected:
            return
        try:
            self._run(self._request("InjectParameterDataRequest", {
                "faceFound": False,
                "mode": "set",
                "parameterValues": [
                    {"id": param_id, "value": value}
                ]
            }))
        except Exception as e:
            pass


EXPRESSION_MAP = {
    1: "expression1.exp3.json",
    2: "expression2.exp3.json",
    3: "expression3.exp3.json",
    4: "expression4.exp3.json",
    5: "expression5.exp3.json",
    6: "expression6.exp3.json",
    7: "expression7.exp3.json",
    8: "expression8.exp3.json",
    9: "expression9.exp3.json",
}

vts_client = VTSClient()
current_expression = -1
_reset_timer = None

def vts_connect():
    vts_client.connect()

def _reset_expression():
    global current_expression
    if current_expression in EXPRESSION_MAP:
        vts_client.set_expression(EXPRESSION_MAP[current_expression], False)
    vts_client.set_parameter("ParamEyeLOpen", 1.0)
    vts_client.set_parameter("ParamEyeROpen", 1.0)
    current_expression = -1

def vts_set_expression(index: int):
    global current_expression, _reset_timer

    if _reset_timer is not None:
        _reset_timer.cancel()
        _reset_timer = None

    if index == current_expression:
        return

    if current_expression in EXPRESSION_MAP:
        vts_client.set_expression(EXPRESSION_MAP[current_expression], False)

    if index in EXPRESSION_MAP:
        vts_client.set_expression(EXPRESSION_MAP[index], True)

    current_expression = index

    if index in [1, 2, 3, 4]:
        _reset_timer = threading.Timer(25.0, _reset_expression)
        _reset_timer.start()

def vts_set_mouth(value: float):
    vts_client.set_parameter("ParamMouthOpenY", value)