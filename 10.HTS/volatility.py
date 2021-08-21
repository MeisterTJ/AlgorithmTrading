# 변동성 돌파 전략에 필요한 함수들을 모은 모듈
import time
import pybithumb


def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]  # 끝에서 두 번째 행 (전일 데이터)를 가져온다. yesterday에는 전일 데이터가 Series 객체로 바인딩된다.

    today_open = yesterday['close']  # 당일 시가를 얻어온다.
    yesterday_high = yesterday['high']  # 전일 고가를 얻어온다.
    yesterday_low = yesterday['low']  # 전일 저가를 얻어온다.
    target = today_open + (
                yesterday_high - yesterday_low) * 0.5  # 래리 윌리엄스 변동성 돌파 전략의 목표가를 계산한다. 목표가 = (당일 시가 + 레인지 x 0.5)
    return target


# 매수 시도 함수
def buy_crypto_currency(bithumb, ticker):
    krw = bithumb.get_balance(ticker)[2]            # 보유 중인 원화를 얻어온다.
    orderbook = pybithumb.get_orderbook(ticker)     # 호가창을 조회해서 최우선 매도 호가를 조회한다.
    sell_price = orderbook['asks'][0]['price']

    # 빗썸의 시장가 API는 수수료 이외에도 30%의 여유가 존재해야 주문이 가능하다. 보유 현금의 100%를 채워서 주문하면
    # "주문량이 사용 가능 KRW를 초과하였습니다" 에러 메시지를 반환한다.
    unit = krw / float(sell_price) * 0.7
    return bithumb.buy_market_order(ticker, unit)   # unit 만큼 매수한다. 


# 매도 시도 함수
def sell_crypto_currency(bithumb, ticker):
    unit = bithumb.get_balance(ticker)[0]
    return bithumb.sell_market_order(ticker, unit)  # 인자로 들어온 ticker의 모든 unit을 시장가 매도한다.


# 이동평균 계산 함수
def get_yesterday_ma5(ticker):
    df = pybithumb.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean()    # 5일간의 종가의 평균을 낸다.
    return ma[-2]                   # 전날까지의 이동평균 반환
