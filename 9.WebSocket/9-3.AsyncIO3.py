# 웹소켓을 이용한 실시간 시세 처리
# asnyc io

import asyncio

async def make_americano():
    print("Americano Start")

    # sleep를 호출한 순간 이벤트 루프가 make_latte 코루틴을 이어서 실행한다.
    # time.sleep 함수가 cpu를 점유하면서 기다리는 것과 달리
    # asyncio.sleep 함수는 CPU가 다른 코루틴을 처리할 수 있도록 CPU 점유를 해제한 상태로 기다린다.
    await asyncio.sleep(3)
    print("Americano End")
    return "Americano"

async def make_latte():
    print("Latte Start")
    await asyncio.sleep(5)
    print("Latte End")
    return "Latte"

async def main():
    coro1 = make_americano()
    coro2 = make_latte()
    result = await asyncio.gather(      # 두 개의 코루틴을 동시에 실행한다. 두 개의 코루틴이 끝날 때까지 기다린다.
        coro1,
        coro2
    )

    print(result)

print("Main Start")
asyncio.run(main())     # 이벤트 루프를 생성하여 main 코루틴을 처리하고 이벤트 루프를 닫는다.
print("Main End")