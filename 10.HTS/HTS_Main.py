import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from pybithumb import Bithumb

form_class = uic.loadUiType("resource/main.ui")[0]


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
                self.b = Bithumb(apiKey, secKey)
                self.balance = self.b.get_balance(self.ticker)
                if self.balance == None:
                    self.textEdit.append("KEY가 올바르지 않습니다.")
                    return
            self.startButton.setText("매매중지")
            self.textEdit.append("------ START ------")
            self.textEdit.append(f"보유 현금 : {self.balance[2]} 원")
        else:
            self.textEdit.append("------- END -------")
            self.startButton.setText("매매시작")

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
