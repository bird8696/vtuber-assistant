import asyncio
import websockets
import json
import time

async def main():
    async with websockets.connect("ws://localhost:8001") as ws:
        # 토큰 요청
        await ws.send(json.dumps({
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "req1",
            "messageType": "AuthenticationTokenRequest",
            "data": {"pluginName": "vtuber-assistant", "pluginDeveloper": "bird8696"}
        }))
        res = json.loads(await ws.recv())
        token = res["data"]["authenticationToken"]

        # 인증
        await ws.send(json.dumps({
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "req2",
            "messageType": "AuthenticationRequest",
            "data": {"pluginName": "vtuber-assistant", "pluginDeveloper": "bird8696", "authenticationToken": token}
        }))
        await ws.recv()
        print("인증 완료")

        # expression2 (화남) 적용
        await ws.send(json.dumps({
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "req3",
            "messageType": "ExpressionActivationRequest",
            "data": {"expressionFile": "expression2.exp3.json", "active": True}
        }))
        res = json.loads(await ws.recv())
        print(f"표정 적용 결과: {res}")

asyncio.run(main())