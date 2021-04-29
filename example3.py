import pybithumb
import datetime

detail = pybithumb.get_market_detail("BTC")

# 저가, 고가, 평균 거래 금액, 거래량 (튜플)
print(detail)

# 해당 가상화폐에 대한 호가 정보를 파이썬 딕셔너리로 얻어온다.
orderbook = pybithumb.get_orderbook("BTC")
print(orderbook)

# timestamp, payment_currency, order_currency, bids, asks
for k in orderbook:
    print(k)

print(orderbook["payment_currency"])             # 거래가능 화폐 (현재는 KRW)
print(orderbook["order_currency"])               # 티커
ms = int(orderbook['timestamp'])                 # 1970년 1월 1일부터 지나간 ms
dt = datetime.datetime.fromtimestamp(ms/1000)    # 초 단위를 넘겨서 현재 날짜 시간 계산
print(dt)

bids = orderbook['bids']
asks = orderbook['asks']

# 매수 호가 출력
for bid in bids:
    price = bid['price']
    quant = bid['quantity']
    print("매수호가:", price, " 매수잔량:", quant)

# 매도 호가 출력
for ask in asks:
    price = ask['price']
    quant = ask['quantity']
    print("매도호가:", price, " 매도잔량:", quant)