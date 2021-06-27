# 지정가 매수
# 지정가 매수를 하는 경우 다음 세 가지에 유의해서 주문을 넣어야 한다.
# 최소 주문 수량 / 유효 자릿수 / 호가 단위
import pybithumb

with open("..\privatekey.txt") as f:
    lines = f.readlines()
    con_key = lines[0].strip()
    sec_key = lines[1].strip()
    bithumb = pybithumb.Bithumb(con_key, sec_key)

# 6005000 금액으로 0.001 단위를 주문 (1BTC가 6005000일때 0.001 단위만큼만 사겠다는 의미)
# pybithumb 모듈은 소수점 네 자리 이하는 버림 후에 주문을 발행한다.
# 가상화폐 또한 주식과 같이 '호가 단위'가 존재한다.
# 비트코인의 가격은 천원 단위로 결정된다.
order = bithumb.buy_limit_order("BTC", 6005000, 0.001)
print(order)

