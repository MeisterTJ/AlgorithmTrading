# 변동성 돌파 전략 백테스팅
# 목표가 계산하기

import pybithumb

# 래리 윌리엄스의 변동성 돌파 전략에서 '레인지' 값을 계산해본다.
# 레인지는 전일 고가에서 전일 저가를 뺀 값이다.
df = pybithumb.get_ohlcv("BTC")
df['range'] = (df['high'] - df['low']) * 0.5        # DataFrame 끝에 range * 0.5 를 끼워넣는다.
df['target'] = df['open'] + df['range'].shift(1)    # 목표가는 시초가 + 전날의 레인지(변동폭 * 0.5)이다.
                                                    # DataFrame 객체에서 각 컬럼은 Series 객체이다.
                                                    # Series 객체에 대해 shift() 메서드를 사용하면 데이터를 위/아래로 시프트 시킬 수 있다.
df.to_excel("btc.xlsx")
