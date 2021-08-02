# 변동성 돌파 전략 백테스팅
# 고가와 목표가를 비교한다.

import pybithumb
import numpy as np

df = pybithumb.get_ohlcv("BTC")
#df = df['2021']     # 2021년
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)

# 고가가 목표가보다 높으면 매수조건에 해당하고 그때의 수익률은 매도가 / 매수가이다.
# 매수 조건을 만족하지 못한 경우 수익률은 1이 된다.
# close는 장이 끝날때 무조건 매도한다고 가정하기 때문에 종가이다.

# 일반적으로 수수료는 0.32%가 발생한다고 본다. (매수, 매도 합산)
# 시장가 주문을 넣을 때 거래량 부족으로 생각하는 가격대보다 조금 더 비싸게 매수되거나
# 조금 더 싸게 매도될 수 있는데, 이때 발생하는 비용을 슬리피지라고 한다.
fee = 0.0016

# 수익률 = 종가(매도가) / 목표가(매수가)
df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'] - fee, 1)
ror = df['ror'].cumprod()[-2]   # df['ror'] 의 모든 값을 곱한 것을 시리즈로 반환한다.
print(type(ror))    #  pandas.series
print(ror)      # 2013년도 부터 했을 경우 54배의 수익률이 나온다.

df.to_excel("trade.xlsx")