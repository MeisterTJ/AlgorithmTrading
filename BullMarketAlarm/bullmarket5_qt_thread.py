import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import pybithumb
import time

tickers = ["BTC", "ETH", "BCH", "ETC"]
form_class = uic.loadUiType("BullMarket.ui")[0]

class Worker(QThread):
    finished = pyqtSignal(dict)

    def run(self):
        while True:
            data = {}

            for ticker in tickers:
                data[ticker] = self.get_market_infos(ticker)

            self.finished.emit(data)    # finished로 data를 emit
            self.msleep(500)            # 쓰레드를 0.5초 슬립한다.

    def get_market_infos(self, ticker):
        try:
            df = pybithumb.get_ohlcv(ticker)
            ma5 = df['close'].rolling(window=5).mean()
            last_ma5 = ma5[-2]
            price = pybithumb.get_current_price(ticker)

            state = None
            if price > last_ma5:
                state = "상승장"
            else:
                state = "하락장"

            return (price, last_ma5, state)
        except:
            return (None, None, None)

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.worker = Worker()
        self.worker.finished.connect(self.update_table_widget)  # finished라는 시그널이 발생하면 메서드 호출한다.
        self.worker.start()

    @pyqtSlot(dict) # dictionary 객체를 받을 수 있는 슬롯임을 지정한다.
    def update_table_widget(self, data):    # data는 dictionary이다.
        try:
            for ticker, infos in data.items():
                index = tickers.index(ticker)
                self.tableWidget.setItem(index, 0, QTableWidgetItem(ticker))
                self.tableWidget.setItem(index, 1, QTableWidgetItem(str(infos[0])))
                self.tableWidget.setItem(index, 2, QTableWidgetItem(str(infos[1])))
                self.tableWidget.setItem(index, 3, QTableWidgetItem(str(infos[2])))
        except:
            pass

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()

