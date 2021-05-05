import pybithumb

# 여러 가상화폐에 대한 정보 한번에 얻기
# opening_price     : 최근 24시간 내 시작 거래 금액
# closing_price     : 최근 24시간 내 마지막 거래 금액
# min_price         : 24시간 내 최저 거래 금액
# max_price         : 24시간 내 최고 거래 금액
# average_price     : 최근 24시간 내 평균 거래 금액
# units_traded      : 최근 24시간 내 Currency 거래량
# volume_1day       : 최근 1일간 Currency 거래량
# volume_7day       : 최근 7일간 Currency 거래량
# buy_price         : 거래 대기건 최고 구매가
# sell_price        : 거래 대기건 최소 판매가
# 24H_fluctate      : 24시간 변동금액
# 24H_flucate_rate  : 24시간 변동률
all = pybithumb.get_current_price("ALL")
for k, v in all.items():
    print(k, v)

# 모든 가상화폐의 현재가를 출력한다.
all = pybithumb.get_current_price("ALL")
for ticker, data in all.items() :
    print(ticker, data['closing_price'])