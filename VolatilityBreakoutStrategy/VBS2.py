# 변동성 돌파 전략 구현
# 가격 변동폭 계산 : 투자하려는 가상화폐의 전일 고가에서 전일 저가를 빼서 가상화폐의 가격 변동폭을 구한다.
# 매수 기준 : 당일 시간에서 (변동폭 * 0.5) 이상 상승하면 해당 가격에 바로 매수한다.
# 매도 기준 : 당일 종가에 매도한다.

# ex) 전일 고가 460, 저가 300, 가격 변동폭 160만원 매수 목표가 480만원
#     현재가가 매수 목표가인 480만원을 넘어서면 바로 매수한다.
#     매도는 00:00:00 초에 갖고 있는 비트코인을 시장가로 전량 매도한다.

import pybithumb

with open("..\privatekey.txt") as f:
    lines = f.readlines()
    con_key = lines[0].strip()
    sec_key = lines[1].strip()
    bithumb = pybithumb.Bithumb(con_key, sec_key)

# ticker에 대한 목표가를 계산하는 함수
def get_target_price(ticker):
    df = pybithumb.get_ohlcv("BTC")     # 비트코인의 일봉 정보를 dataframe 객체로 얻어온다.
    yesterday = df.iloc[-2]     # 끝에서 두 번째 행 (전일 데이터)를 가져온다. yesterday에는 전일 데이터가 Series 객체로 바인딩된다.

    today_open = yesterday['close']     # 당일 시가를 얻어온다.
    yesterday_high = yesterday['high']  # 전일 고가를 얻어온다.
    yesterday_low = yesterday['low']    # 전일 저가를 얻어온다.
    target = today_open + (yesterday_high - yesterday_low) * 0.5    # 래리 윌리엄스 변동성 돌파 전략의 목표가를 계산한다. (당일 시가 + 레인지 x 0.5)
    return target