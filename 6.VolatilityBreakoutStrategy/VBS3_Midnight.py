# 변동성 돌파 전략 구현 
# 단계 3 - 자정에 목표가 갱신하기
# 변동성 돌파 전략에서 목표가는 프로그램이 시작될 때 한 번 그리고 매일 자정마다 갱신해야 한다.
# 현재 시각 및 자정인지 아닌지를 판단해야 한다.

import time
import datetime

while True:
    now = datetime.datetime.now()
    if mid < now < mid + datetime.timedelta(seconds=10):  # 정확한 정각의 00초 비교가 힘들기 때문에 10초 범위 안에 있는지 판단한다.
        print("정각입니다.")
        now = datetime.datetime.now()
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

    print(now, "vs", mid)
    time.sleep(1)

