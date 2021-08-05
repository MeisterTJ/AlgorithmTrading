# 9. 웹소켓을 이용한 실시간 시세 처리
# AsyncIO 기초
# 파이썬에서는 async 키워드가 있는 함수를 코루틴이라고 부른다.

import asyncio

async def async_func1():
    print("Hello")

# 이벤트 루프 동작을 세부적으로 제어하고 싶을 때
# 프로그래머가 직접 이벤트 루프를 얻고 이벤트 루프를 통해 코루틴을 처리한 후
# 이벤트 루프를 닫을 수 있다.

loop = asyncio.get_event_loop()         # 이벤트 루프를 가져온다.
loop.run_until_complete(async_func1())  # 코루틴 객체가 완료될 때가지 실행한다.
loop.close()                            # 이벤트 루프를 닫는다.