# 실시간 데이터 출력
# 거래소에서 실시간으로 전달받은 데이터를 GUI 화면을 통해 출력해본다.
# GUI 프로그램은 이벤트 처리를 위하여 자신의 이벤트 루프를 가진다.
# 코루틴도 이벤트 루프를 가진다.
# 따라서 각각을 서로 다른 프로세스로 생성해줘야 한다.
# 서로 다른 프로세스간의 데이터 전송을 위하여 큐를 사용한다.
# 하나의 프로세스는 여러 개의 쓰레드를 가질 수 있다.

# PyQt를 이용한 GUI 프로그램(프로세스)는 큐로부터 데이터를 가져오는 역할을 하는
# Dummy-1 이라는 이름의 쓰레드와 가져온 데이터를 GUI 화면에 출력하는 역할을 담당하는 'Main Thread'로 구성된다.

# 이 프로그램은 ProducerProcess와 GUI를 담당하는 MainProcess의 두 프로세스로 구성된다.

import multiprocessing as mp
import websockets
import asyncio
import json
import sys
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# 비트코인 가격을 계속해서 받아오는 코루틴
async def bithumb_ws_client(q):
    uri = "wss://pubwss.bithumb.com/pub/ws"

    async with websockets.connect(uri, ping_interval=None) as websocket:
        subscribe_fmt = {
            "type": "ticker",
            "symbols": ["BTC_KRW"],
            "tickTypes": ["1H"]
        }
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            q.put(data)


async def main(q):
    await bithumb_ws_client(q)


def producer(q):
    asyncio.run(main(q))


class Consumer(QThread):
    poped = pyqtSignal(dict)

    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):
        while True:
            if not self.q.empty():
                data = q.get()
                self.poped.emit(data)


class MyWindow(QMainWindow):
    def __init__(self, q):
        super().__init__()
        self.setGeometry(200, 200, 400, 200)
        self.setWindowTitle("Bithumb Websocket with PyQt")

        # thread for data consumer
        self.consumer = Consumer(q)
        self.consumer.poped.connect(self.print_data)
        self.consumer.start()

        # widget
        self.label = QLabel("Bitcoin: ", self)
        self.label.move(10, 10)

        # QLineEdit
        self.line_edit = QLineEdit(" ", self)
        self.line_edit.resize(150, 30)
        self.line_edit.move(100, 10)

    @pyqtSlot(dict)
    def print_data(self, data):
        content = data.get('content')
        if content is not None:
            current_price = int(content.get('closePrice'))
            self.line_edit.setText(format(current_price, ",d"))

        now = datetime.datetime.now()
        self.statusBar().showMessage(str(now))


if __name__ == "__main__":
    # 프로세스간 통신을 위한 큐
    q = mp.Queue()


    p = mp.Process(name="Producer", target=producer, args=(q,), daemon=True)
    p.start()

    # Main process
    app = QApplication(sys.argv)
    mywindow = MyWindow(q)
    mywindow.show()
    app.exec_()
