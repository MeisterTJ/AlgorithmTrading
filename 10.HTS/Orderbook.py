# 실시간 호가창
import sys
import time
import pybithumb
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidgetItem, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation


class OrderbookWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC"):
        super().__init__(parent)
        uic.loadUi("resource/orderbook.ui", self)
        self.ticker = ticker
        self.asksAnim = []
        self.bidsAnim = []

        for i in range(self.tableBids.rowCount()):
            # 매도호가
            # 매도 호가 테이블의 1열에 저장될 문자열 객체 생성 및 오른쪽 정렬
            item_0 = QTableWidgetItem(str(""))
            item_0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableAsks.setItem(i, 0, item_0)

            # 매도 호가 테이블의 2열에 저장될 문자열 객체 생성 및 오른쪽 정렬
            item_1 = QTableWidgetItem(str(""))
            item_1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableAsks.setItem(i, 1, item_1)

            # 3열에 저장될 호가 잔량을 시각화 하기 위한 QProgressBar 객체를 생성한다.
            item_2 = QProgressBar(self.tableAsks)
            # QProgressBar에 출력될 텍스트는 가운데 정렬한다.
            item_2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            # CSS로 셀의 배경 색상을 흰색, ProgressBar의 게이지를 투명도가 부여된 빨강으로 지정한다.
            item_2.setStyleSheet("""
                QProgressBar {background-color : rgba(0, 0, 0, 0%);border : 1}
                QProgressBar::Chunk {background-color : rgba(255, 0, 0, 50%);border : 1}
            """)

            # 객체를 테이블의 3열에 저장한다.
            self.tableAsks.setCellWidget(i, 2, item_2)

            # 애니메이션
            anim = QPropertyAnimation(item_2, b"value")
            anim.setDuration(200)       # 0.2초 짜리 애니메이션
            self.asksAnim.append(anim)

            # 매수호가
            item_0 = QTableWidgetItem(str(""))
            item_0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBids.setItem(i, 0, item_0)

            item_1 = QTableWidgetItem(str(""))
            item_1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBids.setItem(i, 1, item_1)

            item_2 = QProgressBar(self.tableBids)
            item_2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_2.setStyleSheet("""
                QProgressBar {background-color : rgba(0, 0, 0, 0%);border : 1}
                QProgressBar::Chunk {background-color : rgba(0, 255, 0, 40%);border : 1} 
            """)
            self.tableBids.setCellWidget(i, 2, item_2)

            anim = QPropertyAnimation(item_2, b"value")
            anim.setDuration(200)
            self.bidsAnim.append(anim)

        # OrderbookWorker를 생성하고 dataSent 시그널을 연결할 슬롯을 정의한다.
        self.ow = OrderbookWorker(ticker)
        self.ow.dataSent.connect(self.updateData)
        self.ow.start()

    def updateData(self, data):
        # print(data)
        tradingBidValues = []

        for v in data['bids']:
            # 가격과 수량을 곱한 총액을 리스트에 추가한 뒤에
            # 전체 데이터의 최대값을 계산해 maxTradingValue 변수에 저장한다.
            tradingBidValues.append(int(v['price'] * v['quantity']))
        tradingAskValues = []

        for v in data['asks'][::-1]:
            tradingAskValues.append(int(v['price'] * v['quantity']))
        maxtradingValue = max(tradingBidValues + tradingAskValues)

        # 호가와 수량을 차례대로 출력한다.
        for i, v in enumerate(data['asks'][::-1]):
            item_0 = self.tableAsks.item(i, 0)
            item_0.setText(f"{v['price']:,}")
            item_1 = self.tableAsks.item(i, 1)
            item_1.setText(f"{v['quantity']:,}")

            # 총액의 최대가를 100%로 설정하고 현재가를 QProgressBar에 출력한다.
            item_2 = self.tableAsks.cellWidget(i, 2)
            item_2.setRange(0, maxtradingValue)
            item_2.setFormat(f"{tradingAskValues[i]:,}")
            # item_2.setValue(tradingAskValues[i])
            self.asksAnim[i].setStartValue(item_2.value() if item_2.value() > 0 else 0)
            self.asksAnim[i].setEndValue(tradingAskValues[i])
            self.asksAnim[i].start()

        for i, v in enumerate(data['bids']):
            item_0 = self.tableBids.item(i, 0)
            item_0.setText(f"{v['price']:,}")
            item_1 = self.tableBids.item(i, 1)
            item_1.setText(f"{v['quantity']:,}")
            item_2 = self.tableBids.cellWidget(i, 2)
            item_2.setRange(0, maxtradingValue)
            item_2.setFormat(f"{tradingBidValues[i]:,}")
            # item_2.setValue(tradingBidValues[i])

            # StartValue부터 EndValue까지 200ms 시간 동안 움직이도록 한다.
            self.bidsAnim[i].setStartValue(item_2.value() if item_2.value() > 0 else 0)
            self.bidsAnim[i].setEndValue(tradingAskValues[i])
            self.bidsAnim[i].start()

    def closeEvent(self, event):
        self.ow.close()


# 데이터를 얻어오는 쓰레드
class OrderbookWorker(QThread):
    dataSent = pyqtSignal(dict)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        while self.alive:
            data = pybithumb.get_orderbook(self.ticker, limit=10)
            # 초당 20번의 요청을 수행한다.
            time.sleep(0.05)
            # API로 조회한 호가 정보는 딕셔너리로 반환되는데, 이를 그대로 슬롯으로 전달한다.
            self.dataSent.emit(data)

    def close(self):
        self.alive = False


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ow = OrderbookWidget()
    ow.show()
    exit(app.exec_())
