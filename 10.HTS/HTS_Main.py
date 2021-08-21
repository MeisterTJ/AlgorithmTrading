import sys
import pybithumb
import datetime
import time
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from volatility import *

form_class = uic.loadUiType("resource/main.ui")[0]


# 변동성 돌파 전략을 실행하는 쓰레드
class VolatilityWorker(QThread):
    tradingSent = pyqtSignal(str, str, str)

    def __init__(self, ticker, bithumb):
        super().__init__()
        self.ticker = ticker
        self.bithumb = bithumb
        self.alive = True

    def run(self):
        # 현재 시간
        now = datetime.datetime.now()
        # 현재 일 (00시) 로부터 하루 뒤
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        # 전날의 5일 이동 평균
        ma5 = get_yesterday_ma5(self.ticker)
        target_price = get_target_price(self.ticker)
        wait_flag = False

        while self.alive:
            try:
                now = datetime.datetime.now()

                # 정확한 00시 00초를 잡아낼 수는 없으니 10초 안쪽 범위에 있는지 체크한다.
                if mid < now < mid + datetime.delta(seconds=10):
                    target_price = get_target_price(self.ticker)
                    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                    ma5 = get_yesterday_ma5(self.ticker)

                    # 자정에는 코인을 전부 판다.
                    desc = sell_crypto_currency(self.bithumb, self.ticker)

                    # 시장가 매도를 수행한 뒤에 주문의 체결 여부를 다시 한번 조회한다.
                    result = self.bithumb.get_order_completed(desc)

                    # 매도 체결되지 않았다면 result에 None이 들어가기 때문에 KeyError를 일으켜서
                    # except 구문으로 이동해서 다시 매도를 시도한다.
                    timestamp = result['data']['order_date']
                    dt = datetime.datetime.fromtimestamp(int(int(timestamp) / 1000000))
                    tstring = dt.strftime("%Y/%m/%d %H:%M:%S")
                    self.tradingSent.emit(tstring, "매도", result['data']['order_qty'])
                    wait_flag = False

                if wait_flag == False:
                    # 변동성 돌파의 조건을 만족하면 매수를 시도한다.
                    # 매수 또한 매도와 동일하게 주문의 정상 처리 여부를 확인한 뒤 매수를 확정 짓는다.
                    current_price = pybithumb.get_current_price(self.ticker)
                    if (current_price > target_price) and (current_price > ma5):
                        desc = buy_crypto_currency(self.bithumb, self.ticker)
                        result = self.bithumb.get_order_completed(desc)
                        timestamp = result['data']['order_date']
                        dt = datetime.datetime.fromtimestamp(int(int(timestamp) / 1000000))
                        tstring = dt.strftime("%Y/%m/%d %H:%M:%S")
                        self.tradingSent.emit(tstring, "매수", result['data']['order_qty'])
                        wait_flag = True
            except:
                pass
            time.sleep(1)

    def close(self):
        self.alive = False


class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ticker = "BTC"
        self.startButton.clicked.connect(self.clickBtn)
        self.setWindowTitle("Home Trading System")

        with open("..\privatekey.txt") as f:
            lines = f.readlines()
            api_Key = lines[0].strip()
            sec_Key = lines[1].strip()
            self.apiKey.setText(api_Key)
            self.secKey.setText(sec_Key)

    def clickBtn(self):
        if self.startButton.text() == "매매시작":
            apiKey = self.apiKey.text()
            secKey = self.secKey.text()
            if len(apiKey) != 32 or len(secKey) != 32:
                self.textEdit.append("Key가 올바르지 않습니다.")
                return
            else:
                self.bithumb = pybithumb.Bithumb(apiKey, secKey)
                self.balance = self.bithumb.get_balance(self.ticker)
                if self.balance == None:
                    self.textEdit.append("KEY가 올바르지 않습니다.")
                    return
            self.startButton.setText("매매중지")
            self.textEdit.append("------ START ------")
            self.textEdit.append(f"보유 현금 : {self.balance[2]} 원")

            # 변동성 돌파 전략을 실행하는 쓰레드 실행
            self.vw = VolatilityWorker(self.ticker, self.bithumb)
            self.vw.tradingSent.connect(self.receiveTradingSignal)
            self.vw.start()

        else:
            self.vw.close()
            self.textEdit.append("------- END -------")
            self.startButton.setText("매매시작")

    def receiveTradingSignal(self, time, type, amount):
        self.textEdit.append(f"[{time}] {type} : {amount}")

    def closeEvent(self, event):
        # 각 위젯들에게 closeEvent를 날려주어야 한다.
        # 하위 위젯들의 closeEvent는 자동으로 불리지 않는 듯 하다.
        self.chartWidget.closeEvent(event)
        self.overviewWidget.closeEvent(event)
        self.orderbookWidget.closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())
