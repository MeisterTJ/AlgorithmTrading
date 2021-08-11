# 빗썸 거래소 웹소켓 구독하기
# 빗썸 거래소의 웹소켓은 한 번 구독 요청을 하면 계속해서 실시간 데이터를 전송해준다.
# 다음 코드는 빗썸 거래소에 비트코인의 현재가에 대해서 구독 신청하여
# 계속해서 비트코인의 현재가를 서버로부터 전달받고 이를 출력하는 프로그램이다.

import websockets
import asyncio
import json
async def bithumb_ws_client():
    uri = "wss://pubwss.bithumb.com/pub/ws"

    # ping_interval 옵션은 웹소켓 클라이언트에서 웹소켓 서버로 해당 주기마다 Ping frame을 보내는 기능이다.
    # 빗썸에서는 이 값을 None으로 설정해야 한다. 이는 클라이언트가 서버로 Ping frame 데이터를 보내지 않는다는 뜻이다.
    async with websockets.connect(uri, ping_interval=None) as websocket:
        greeting = await websocket.recv()
        print(greeting)

        subscribe_fmt = {
            "type" : "ticker",              # type에는 현재가(ticker), 체결내역(transaction), 호가(orderbookdepth) 중 하나를 입력할 수 있다.
            "symbols" : ["BTC_KRW"],        # 구독할 코인의 티커를 정한다.
            "tickTypes" : ["1H"]            # 데이터의 기준점을 설정한다. 30M, 1H, 12H, 24H, MID를 사용할 수 있다.
        }
        subscribe_data = json.dumps(subscribe_fmt)  # json 모듈을 사용해서 파이선 딕셔너리를 JSON 타입으로 변환한다.
        await websocket.send(subscribe_data)        # 구독 요청을 서버에 전송한다.

        while True:
            data = await websocket.recv()       # 반복적으로 데이터를 받아 출력한다.
            data = json.loads(data)
            print(data)

            # {'type': 'ticker', 'content': {'tickType': '1H', 'date': '20210812', 'time': '001305', 'openPrice': '53187000',
            # 'closePrice': '53397000', 'lowPrice': '53068000', 'highPrice': '53400000', 'value': '7527581205.09646',
            # 'volume': '141.46424173', 'sellVolume': '73.90424743', 'buyVolume': '67.5599943',
            # 'prevClosePrice': '53220000', 'chgRate': '0.39', 'chgAmt': '210000', 'volumePower': '91.42', 'symbol': 'BTC_KRW'}}
            # 위 처럼 출력된다.

async def main():
    await bithumb_ws_client()

asyncio.run(main())