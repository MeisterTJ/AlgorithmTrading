# 시장가 매수
import pybithumb
import time

with open("..\privatekey.txt") as f:
    lines = f.readlines()
    con_key = lines[0].strip()
    sec_key = lines[1].strip()
    bithumb = pybithumb.Bithumb(con_key, sec_key)

order = bithumb.buy_market_order("BTC", 1)
print(order)

time.sleep(3)
cancel = bithumb.cancel_order(order)    # cancel_order 메서드의 입력으로 넣어 주문 취소 메서드를 호출한다.
print(cancel)
