# 변동성 돌파 전략 백테스팅
# 고가와 목표가를 비교한다.
#
# 가장 좋은 k를 구하기 (전날 고가에서 저가를 뺀 후 곱해주는 값)

import pybithumb
import numpy as np

    df = pybithumb.get_ohlcv("BTC")
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    # 고가가 목표가보다 높으면 매수조건에 해당하고 그때의 수익률은 매도가 / 매수가이다.
    # 매수 조건을 만족하지 못한 경우 수익률은 1이 된다.
    # close는 장이 끝날때 무조건 매도한다고 가정하기 때문에 종가이다.

    # 일반적으로 수수료는 0.32%가 발생한다고 본다. (매수, 매도 합산)
    # 시장가 주문을 넣을 때 거래량 부족으로 생각하는 가격대보다 조금 더 비싸게 매수되거나
    # 조금 더 싸게 매도될 수 있는데, 이때 발생하는 비용을 슬리피지라고 한다.
    fee = 0.0032

    # 수익률 = 종가(매도가) / 목표가(매수가) - 수수료%
    df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'] - fee, 1)
    ror = df['ror'].cumprod()[-2]   # df['ror'] 의 모든 값을 순서대로 곱한 것을 시리즈로 반환한다.
    return ror

# 0.1 부터 1.0까지 0.1씩 증가한 값으로 for loop를 만든다.
# 참고로 파이썬의 range() 함수는 정수값만 사용 가능하다.
for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k)
    print("%.1f %f" % (k, ror)) # 0.1 ~ 0.9 까지의 k값을 대입했을 때의 수익률을 출력한다.