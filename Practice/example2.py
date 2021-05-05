import pybithumb
import time

# 빗썸 모든 가상화폐 티커와 가격을 0.1초 마다 하나씩 출력
tickers = pybithumb.get_tickers()
for ticker in tickers:
    price = pybithumb.get_current_price(ticker)
    print(ticker, price)
    time.sleep(0.1)