# 비트코인 지정가 매도
import pybithumb
import time

with open("..\privatekey.txt") as f:
    lines = f.readlines()
    con_key = lines[0].strip()
    sec_key = lines[1].strip()
    bithumb = pybithumb.Bithumb(con_key, sec_key)

# 정해진 수량을 정해진 가격으로 매도한다.
order = bithumb.sell_limit_order("BTC", 4000000, 1)
print(order)

# 잔고를 조회해서 보유 중인 비트코인 수량만큼 지정가 매도 주문을 한다.
# 지정가 매도를 하는 경우에도 호가 가격 단위를 지켜야 한다.
unit = bithumb.get_balance("BTC")[0]
print(unit)
order = bithumb.sell_limit_order("BTC", 4000000, unit)
print(order)