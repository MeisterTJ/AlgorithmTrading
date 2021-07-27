# 상승장/하락장 구분하는 함수 구현하기
# 현재가가 전일 이동평균보다 높으면 상승장이고, 그렇지 않으면 하락장으로 판단하겠다.
import pybithumb


# 상승장, 하락장 구하는 함수
def bull_market(ticker):
    df = pybithumb.get_ohlcv(ticker)  # 티커의 과거 시세 가져오기
    ma5 = df['close'].rolling(window=5).mean()  # close(종가)를 5개씩 그룹화하여 평균을 낸다.
    price = pybithumb.get_current_price(ticker)  # 티커의 현재가 가져오기
    last_ma5 = ma5[-2]  # 끝에서 두 번째 위치한 전일 이동평균을 last_ma5 변수에 바인딩한다.

    if price > last_ma5:
        print("TICKER : {}, 상승장, 현재가격 : {},  전일이동평균 : {}".format(ticker, price, last_ma5))
        return True
    else:
        print("TICKER : {}, 하락장, 현재가격 : {},  전일이동평균 : {}".format(ticker, price, last_ma5))
        return False


tickers = pybithumb.get_tickers()
for ticker in tickers:
    bull_market(ticker)