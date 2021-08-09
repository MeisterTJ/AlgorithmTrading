import multiprocessing as mp
import time

def worker():
    proc = mp.current_process()
    print(proc.name)
    print(proc.pid)
    time.sleep(5)
    print("SubProcess End")

if __name__ == "__main__":
    # main process
    proc = mp.current_process()     # 프로세스에 대한 정보를 담고 있는 객체를 얻는다.
    print(proc.name)    # MainProcess
    print(proc.pid)

    # process spawning
    # 프로세스 스포닝을 통해서 자식 프로세스를 만들 수 있다.
    # 파이썬은 전역 인터프리터 락 문제가 있어서 쓰레드보다는 프로세스를 사용하는 것이 더 성능이 좋다.

    # 프로세스 클래스의 인스턴스 생성
    # 인스턴스를 생성할 때 자식 프로세스의 이름과 함수를 전달한다.
    p = mp.Process(name="SubProcess", target=worker)
    p.start()   # 프로세스 실행

    print("MainProcess End")