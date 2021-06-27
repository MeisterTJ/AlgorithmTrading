# 보유 원화를 조회하고 최우선 매도 호가 금액을 얻어와 매수할 수 있는 비트코인 개수를 계산한다.
import pybithumb
import time

with open("..\privatekey.txt") as f:
    lines = f.readlines()
    con_key = lines[0].strip()
    sec_key = lines[1].strip()
    bithumb = pybithumb.Bithumb(con_key, sec_key)

krw = bithumb.get_balance("BTC")[2]
orderbook = pybithumb.get_orderbook("BTC")

asks = orderbook['asks']
sell_price = asks[0]['price']
unit = krw/float(sell_price)

# 살수 있는 비트코인의 개수를 출력한다.
print(unit)
