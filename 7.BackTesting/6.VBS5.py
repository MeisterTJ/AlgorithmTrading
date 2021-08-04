# 변동성 돌파 + 상승장 전략 백테스팅
# 5일 이동평균을 사용해서 상승장/하락장을 판단한 후
# 상승장이면서 변동성 돌파 전략의 조건을 만족할 때 매수하면 된다.

import pybithumb
import numpy as np

df = pybithumb.get_ohlcv("BTC")

# 각 거래일에 대해 5일 이동평균을 계산한다. (rolling으로 5개씩 그룹화), mean으로 평균 계산
# shift(1)을 호출해서 계산된 5일 이동평균 값을 한 행 밑으로 내려 저장한다.
# 즉 오늘의 ma5에는 전날까지의 5일 이동평균 값이 저장된다.
df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)
df['targetBuy'] = df['high'] > df['target']

# 거래일의 시초가가 전일 종가까지 계산된 5일 이동평균보다 큰지 판단.
df['bull'] = df['open'] > df['ma5']

fee = 0.0032

# 당일 수익률 (close에 매매했다고 본다.)
df['ror'] = np.where((df['high'] > df['target']) & df['bull'], df['close'] / df['target'] - fee, 1)

# 기간 수익률
df['hpr'] = df['ror'].cumprod()     

# dd = drawdown (낙폭)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

print("MDD(%): ", df['dd'].max())
print("HPR: ", df['hpr'][-2])
df.to_excel("larry_ma.xlsx")

