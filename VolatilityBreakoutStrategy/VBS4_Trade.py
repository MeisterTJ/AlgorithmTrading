# 변동성 돌파 전략 구현 + 상승장 투자 전략 구현
# 매수, 매도 시도
# 1초 마다 계산

# 목표가가 현재가 이상일 경우 잔고를 조회하고 주문 가능한 수량을 계산한 후에 시장가로 매수한다.

import time
import datetime
import pybithumb

# ticker에 대한 목표가를 계산하는 함수
def get_target_price(ticker):
    df = pybithumb.get_ohlcv("BTC")     # 비트코인의 일봉 정보를 dataframe 객체로 얻어온다.
    yesterday = df.iloc[-2]     # 끝에서 두 번째 행 (전일 데이터)를 가져온다. yesterday에는 전일 데이터가 Series 객체로 바인딩된다.

    today_open = yesterday['close']     # 당일 시가를 얻어온다.
    yesterday_high = yesterday['high']  # 전일 고가를 얻어온다.
    yesterday_low = yesterday['low']    # 전일 저가를 얻어온다.
    target = today_open + (yesterday_high - yesterday_low) * 0.5    # 래리 윌리엄스 변동성 돌파 전략의 목표가를 계산한다. 목표가 = (당일 시가 + 레인지 x 0.5)
    return target

# 매수 시도 함수
def buy_crypto_currency(ticker):
    krw = bithumb.get_balance("BTC")[2]         # 보유 중인 원화를 얻어온다.
    orderbook = pybithumb.get_orderbook("BTC")  # 호가창을 조회해서 최우선 매도 호가를 조회한다.
    sell_price = orderbook['asks'][0]['price']
    unit = krw / float(sell_price)
    bithumb.buy_market_order("BTC", unit)  # 시장가로 살수 있는 만큼 모두 매수한다.

# 매도 시도 함수
def sell_crpyto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)     # 인자로 들어온 ticker의 모든 unit을 시장가 매도한다.'

# 이동평균 계산 함수
def get_yesterday_ma5(ticker):
    df = pybithumb.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(window=5).mean()
    return ma[-2]

# 외부 파일에서 private key 읽어오기.
with open("..\privatekey.txt") as f:
    lines = f.readlines()
    con_key = lines[0].strip()
    sec_key = lines[1].strip()
    bithumb = pybithumb.Bithumb(con_key, sec_key)

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
ma5 = get_yesterday_ma5("BTC")
target_price = get_target_price("BTC")

# 메인 로직
while True:
    try:
        now = datetime.datetime.now()
        if mid < now < mid + datetime.timedelta(seconds=10):  # 정확한 정각의 00초 비교가 힘들기 때문에 10초 범위 안에 있는지 판단한다.
            target_price = get_target_price("BTC")  # 정각마다 목표가를 얻어온다.
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            ma5 = get_yesterday_ma5("BTC")
            sell_crpyto_currency("BTC")     # 정각마다 가지고 있는 모든 비트코인을 판다.

        current_price = pybithumb.get_current_price("BTC")
        if (current_price > target_price) and (current_price > ma5) :        # 현재 가격이 타겟 가격, 5일 이동평균보다 높으면 매수
            buy_crypto_currency("BTC")

        print("------------------------")
        print("Time : ", now)
        print("Target  Price : ", target_price)
        print("MA5     Price : ", ma5)
        print("Current Price : ", current_price)
    except:
        print("에러 발생")

    time.sleep(1)