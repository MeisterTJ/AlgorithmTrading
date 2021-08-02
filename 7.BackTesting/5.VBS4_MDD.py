# 변동성 돌파 전략 백테스팅
# 고가와 목표가를 비교한다.
# MDD (Maximum Draw Down) 계산하기
# MDD는 투자 기간 중에 포트폴리오의 전 고점에서 저점까지의 최대 누적 손실을 의미한다.
# MDD = ((high - low) / high) * 100

import pybithumb
import numpy as np

df = pybithumb.get_ohlcv("BTC")
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0032

# 당일수익률 = 종가(매도가) / 목표가(매수가) - 수수료%
df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'] - fee, 1)

# df['ror'] 의 모든 값을 순서대로 곱한 것을 시리즈로 반환한다. (거래일 마다의 기간 수익률)
df['hpr'] = df['ror'].cumprod()     # 기간 수익률

# dd = drawdown (낙폭)
# ((기간 수익률 중에 최대값 - 오늘까지의 기간수익률) / 기간 수익률 중에 최대값) * 100
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# dd 중 가장 큰 값을 구한다. (기간 수익률 중에 최대값과 기간 수익률 중에 최소값의 차이의 비율)
print("MDD(%): ", df['dd'].max())   # 기간 수익률 중에 가장 높았던 때로부터 가장 낮을때가 75%나 하락했다.
df.to_excel("dd.xlsx")
