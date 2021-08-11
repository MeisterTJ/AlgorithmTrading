# 웹소켓 클라이언트
# websocket 모듈을 사용하여 웹소켓 기반으로 서버와 클라이언트 프로그램을 개발할 수 있다.

import websockets
import asyncio

async def bithumb_ws_client():
    uri = "wss://pubwss.bithumb.com/pub/ws"     # 빗썸 거래소의 웹소켓 서버 주소

    # 웹소켓 자원을 얻고 반환하는 것을 with로 한번에 처리할 수 있다.
    async with websockets.connect(uri) as websocket:
        greeting = await websocket.recv()
        print(greeting) # {"status":"0000","resmsg":"Connected Successfully"}

async def main():
    await bithumb_ws_client()

asyncio.run(main())

