import pybithumb
import time

while True:
    price = pybithumb.get_current_price("BTC")
    try:
        print(price/10)
    except:
        print("에러 발생", price)
    time.sleep(0.2)