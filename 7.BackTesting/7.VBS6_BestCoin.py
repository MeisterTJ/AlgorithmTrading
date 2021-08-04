# 변동성 돌파 + 상승장 전략 백테스팅
# 특정 연도에 기간 수익률이 높은 코인 착기

import pybithumb
import numpy as np

def get_hpr(ticker):
    try:
        df = pybithumb.get_ohlcv(ticker)
        df = df['2021']

        # 각 거래일에 대해 5일 이동평균을 계산한다. (rolling으로 5개씩 그룹화), mean으로 평균 계산
        # shift(1)을 호출해서 계산된 5일 이동평균 값을 한 행 밑으로 내려 저장한다.
        # 즉 오늘의 ma5에는 전날까지의 5일 이동평균 값이 저장된다.
        df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
        df['range'] = (df['high'] - df['low']) * 0.5
        df['target'] = df['open'] + df['range'].shift(1)

        # 거래일의 시초가가 전일 종가까지 계산된 5일 이동평균보다 큰지 판단.
        df['bull'] = df['open'] > df['ma5']

        # 수수료 + 슬리피지가 이정도는 된다고 본다.
        fee = 0.0032

        # 당일 수익률 (close에 매매했다고 본다.)
        df['ror'] = np.where((df['high'] > df['target']) & df['bull'], df['close'] / df['target'] - fee, 1)

        # 기간 수익률
        df['hpr'] = df['ror'].cumprod()
        return df['hpr'][-2]        # -2 (전날)
    except:
        return 1

tickers = pybithumb.get_tickers()

hprs = []
for ticker in tickers:
    hpr = get_hpr(ticker)
    hprs.append((ticker, hpr))

sorted_hprs = sorted(hprs, key=lambda x:x[1], reverse=True)
print(sorted_hprs[:5])

