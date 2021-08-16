# pybithumb 모듈을 이용한 실시간 데이터 출력
# pybithumb 모듈을 사용하면 웹소켓을 보다 쉽게 이용할 수 있다.
# pybithumb 모듈이 서버로부터 데이터를 받은 후 내부에서 생성한 큐에 데이터를 저장까지 해준다.
# 따라서 PyQt를 이용한 GUI 프로그램에서 큐로부터 데이터를 계속 빼가는 쓰레드를 통해
# 데이터를 뽑은 후 이를 위젯에 출력해 주는 부분만 구현해주면 된다.

# pybithumb 모듈을 사용하면 asyncio를 통해 데이터를 받는 부분을 직접 코딩할 필요가 없기 때문에
# 조금 더 편리하게 사용할 수 있다.

from pybithumb import WebSocketManager
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
import time


class Worker(QThread):
    recv = pyqtSignal(str)  # pyqtSignal 객체는 인스턴스 변수가 아닌 클래스 변수로 만들어야 한다.

    def run(self):
        # create websocket for Bithumb
        # pybithumb의 웹소켓 매니저를 사용한다.
        wm = WebSocketManager("ticker", ["BTC_KRW"])
        while True:
            data = wm.get()

            # str을 이벤트로 보낸다 -> pyqtSlot(str) 이 호출된다.
            self.recv.emit(data['content']['closePrice'])


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        label = QLabel("BTC", self)
        label.move(20, 20)

        self.price = QLabel("-", self)
        self.price.move(80, 20)
        self.price.resize(100, 20)

        button = QPushButton("Start", self)
        button.move(20, 50)
        button.clicked.connect(self.click_btn)

        self.th = Worker()
        self.th.recv.connect(self.receive_msg)
    
    # 이벤트가 발생할 때 호출되는 함수
    @pyqtSlot(str)
    def receive_msg(self, msg):
        print(msg)
        self.price.setText(msg)

    def click_btn(self):
        self.th.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
