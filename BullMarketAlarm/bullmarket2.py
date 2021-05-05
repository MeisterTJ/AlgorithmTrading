# 5일 종가 이평선 구하기 (종가 24:00)
import pybithumb

btc = pybithumb.get_ohlcv("BTC")
close = btc['close']
print((close[0] + close[1] + close[2] + close[3] + close[4])/5)     # 종가로 이평선 계산
print((close[1] + close[2] + close[3] + close[4] + close[5])/5)
print((close[2] + close[3] + close[4] + close[5] + close[6])/5)

window = close.rolling(5)   # 5일씩 모든 데이터를 그룹화한다.
ma5 = window.mean()     # 그룹화된 값의 평균
print(ma5)  # 5일 이동 평균이 바인딩 되어서 출력된다. 데이터가 충분하지 않은 앞부분에는 값없음이 표시된다.

