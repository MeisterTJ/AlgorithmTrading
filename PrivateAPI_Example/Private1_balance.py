# No Commit
import pybithumb
import time

with open("..\privatekey.txt") as f:
    lines = f.readlines()
    con_key = lines[0].strip()
    sec_key = lines[1].strip()
    bithumb = pybithumb.Bithumb(con_key, sec_key)

# 모든 가상화폐의 잔고를 조회할 수 있다.
for ticker in pybithumb.get_tickers() :
    balance = bithumb.get_balance(ticker)
    # print(format(balance[0], 'f'))        # 매우 크거나 작은 수를 효과적으로 표현하기 위해서 파이썬이 지수승 형태로 출력을 한다. 사람이 읽기 좋은 실수로 값을 출력하는 방법
    print(ticker, ":", balance)
    time.sleep(0.1)

