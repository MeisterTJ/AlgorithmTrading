import pybithumb

# 시가, 고가, 저가, 종가, 거래량(OHLCV) 가 저장된 Pandas DataFrame 객체를 가져온다. (과거부터 현재까지)
btc = pybithumb.get_ohlcv("BTC")

# print(btc)
close = btc['close']    # Series 객체로 반환
print(close)    # 날짜 인덱스, 종가를 과거부터 현재까지 출력 (Series 객체)


