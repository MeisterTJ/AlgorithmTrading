# 가상화폐 일봉 데이터 얻기
# DataFrame 객체를 엑셀로 저장하기

import pybithumb

df = pybithumb.get_ohlcv("BTC")     # 암호화폐의 일봉 차트 데이터를 DataFrame으로 얻어온다.
print(df.tail())                    # 마지막 5줄을 출력해본다.
df.to_excel("btc.xlsx")             # DataFrame의 모든 데이터를 엑셀 파일로 출력한다. 