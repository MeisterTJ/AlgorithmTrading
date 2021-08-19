# 실시간 개요창
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pybithumb import WebSocketManager


class OverviewWorker(QThread):
    data24Sent = pyqtSignal(int, float, int, float, int, int)
    dataMidSent = pyqtSignal(int, float, float)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        # 24시간을 기준으로 비트코인의 가격 정보 (ticker)를 요청하는 웹 소켓을 정의한다.
        # 빗썸 웹페이지에서는 항목에 24시간 전, 전일을 섞어서 표시하고 있다.
        wm = WebSocketManager("ticker", [f"{self.ticker}_KRW"], ["24H", "MID"])
        while self.alive:
            # 웹 서버가 보내온 정보를 얻어온다.
            data = wm.get()

            # 전송된 데이터에서 필요한 값들을 인덱싱한다.
            if data['content']['tickType'] == "MID":
                self.dataMidSent.emit(int(data['content']['closePrice']),
                                      float(data['content']['chgRate']),
                                      float(data['content']['volumePower']))
            else:
                self.data24Sent.emit(int(data['content']['closePrice']),
                                     float(data['content']['volume']),
                                     int(data['content']['highPrice']),
                                     float(data['content']['value']),
                                     int(data['content']['lowPrice']),
                                     int(data['content']['prevClosePrice']))


        # 작업이 끝나면 웹소켓 매니저를 터미네이트 시켜야 한다.
        wm.terminate()

    def close(self):
        self.alive = False


class OverviewWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC"):
        super().__init__(parent)
        uic.loadUi("resource/overview.ui", self)
        self.ticker = ticker

        self.ovw = OverviewWorker(ticker)
        self.ovw.data24Sent.connect(self.fill24Data)
        self.ovw.dataMidSent.connect(self.fillMidData)
        self.ovw.start()

    # 슬롯으로 전달된 데이터를 Label에 출력한다. 문자열 포매팅을 위해 f-string을 사용했다.
    def fill24Data(self, currPrice, volume, highPrice, value, lowPrice, prevClosePrice):
        self.label_1.setText(f"{currPrice:,}")
        self.label_4.setText(f"{volume:.4f} {self.ticker}")
        self.label_6.setText(f"{highPrice:,}")
        self.label_8.setText(f"{value / 100000000:,.1f} 억")
        self.label_10.setText(f"{lowPrice:,}")
        self.label_14.setText(f"{prevClosePrice:,}")
        self.__updateStyle()

    def fillMidData(self, currPrice, chgRate, volumePower):
        self.label_1.setText(f"{currPrice:,}")
        self.label_2.setText(f"{chgRate:+.2f}%")
        self.label_12.setText(f"{volumePower:.2f}%")
        self.__updateStyle()
        
    # 가격에 따라 빨강, 파랑으로 변하기 위한 함수
    def __updateStyle(self):
        if '-' in self.label_2.text():
            self.label_1.setStyleSheet("color:blue")
            self.label_2.setStyleSheet("background-color:blue;color:white")
        else:
            self.label_1.setStyleSheet("color:red")
            self.label_2.setStyleSheet("background-color:red;color:white")

    def closeEvent(self, event):
        self.ovw.close()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ob = OverviewWidget()
    ob.show()
    exit(app.exec_())
