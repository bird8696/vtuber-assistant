import asyncio
import websockets
import json

async def main():
    async with websockets.connect("ws://localhost:8001") as ws:
        with open("vts_token.txt") as f:
            token = f.read().strip()

        await ws.send(json.dumps({
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "req2",
            "messageType": "AuthenticationRequest",
            "data": {"pluginName": "vtuber-assistant", "pluginDeveloper": "bird8696", "authenticationToken": token}
        }))
        await ws.recv()
        print("인증 완료")

        # 입 벌리기 테스트
        import time
        for i in range(20):
            val = 0.8 if i % 2 == 0 else 0.0
            await ws.send(json.dumps({
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "req3",
                "messageType": "InjectParameterDataRequest",
                "data": {
                    "faceFound": False,
                    "mode": "set",
                    "parameterValues": [{"id": "MouthOpen", "value": val}]
                }
            }))
            await ws.recv()
            time.sleep(0.3)

asyncio.run(main())