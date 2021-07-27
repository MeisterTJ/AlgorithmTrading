# 상승장 알리미 (2) - 타이머 만들기
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import pybithumb

tickers = ["BTC", "ETH", "BCH", "ETC"]
form_class = uic.loadUiType("BullMarket.ui")[0]

# GUI가 버벅대는 현상이 발생
# 파이썬 인터프리터가 현재가를 조회하고 화면에 GUI를 그리는 두 가지 일을 순차적으로 실행하기 때문에 발생한다.
# 네트워크 지연이 발생하거나 현재가를 조회하는 코드가 복잡해서 시간이 걸리는 경우에는 GUI를 바로 그려줄 수 없기 때문에 프로그램이 버벅대는 현상이 발생한다.
class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.timer = QTimer(self)
        self.timer.start(5000)
        self.timer.timeout.connect(self.timeout)

    def get_market_infos(self, ticker):
        df = pybithumb.get_ohlcv(ticker)
        ma5 = df['close'].rolling(window=5).mean()
        last_ma5 = ma5[-2]
        price = pybithumb.get_current_price(ticker)

        state = None
        if price > last_ma5:
            state = "상숭장"
        else:
            state = "하락장"

        return price, last_ma5, state

    def timeout(self):
        for i, ticker in enumerate(tickers):
            item = QTableWidgetItem(ticker)
            self.tableWidget.setItem(i, 0, item)

            price, last_ma5, state = self.get_market_infos(ticker)
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(price)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(last_ma5)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(state)))

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()