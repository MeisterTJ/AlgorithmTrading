import pybithumb
import time

# ticker 얻어오기
tickers = pybithumb.get_tickers()
print(tickers)  # 모든 티커 출력
print(len(tickers)) # 티커 개수 출력

while True:
    price = pybithumb.get_current_price("BTC")
    print(price)    # BTC의 현재 가격 얻어오기
    time.sleep(1)


