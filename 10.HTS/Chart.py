# 실시간 현재가 차트
# chart.ui 파일을 읽어오고 현재가를 출력한다.

import sys
import time
import pybithumb
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtChart import QLineSeries, QChart, QValueAxis, QDateTimeAxis
from PyQt5.QtGui import QPainter  # Antialiasing을 제거하는데 사용하는 모듈을 Import
from PyQt5.QtCore import Qt, QDateTime, QThread, pyqtSignal


class PriceWorker(QThread):
    # 메인 쓰레드에 데이터를 전달하기 위한 dataSent 시그널을 정의한다.
    dataSent = pyqtSignal(float)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker

        # QThread를 안전하게 종료하기 위해 인스턴스 변수를 사용한다. alive의 초기값은 True이다.
        self.alive = True

    def run(self):
        # 반복해서 현재가를 조회하고 시그널을 메인 쓰레드에 알립니다.
        # alive가 False가 되면 반복문을 탈출해서 쓰레드가 종료된다.
        while self.alive:
            data = pybithumb.get_current_price(self.ticker)
            time.sleep(1)
            self.dataSent.emit(data)

    def close(self):
        self.alive = False


# 메인 GUI에 추가할 목적이므로 QWidget 클래스를 상속하는 ChartWidget 클래스를 정의한다.
class ChartWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC"):
        super().__init__(parent)
        # chart.ui 파일을 읽어와서 디자인을 적용한다.
        uic.loadUi("resource/chart.ui", self)
        self.ticker = ticker
        self.viewLimit = 120  # 라인 차트로 그릴 데이터의 수를 미리 정의한다.

        self.priceData = QLineSeries()
        self.priceChart = QChart()
        self.priceChart.addSeries(self.priceData)
        self.priceChart.legend().hide()  # 차트의 범례를 숨긴다.

        axisX = QDateTimeAxis()  # PyChart에서 날짜 축을 관리하는 QDateTimeAxis 객체를 생성한다.
        axisX.setFormat("hh:mm:ss")  # 시:분:초 형태로 차트에 표시한다.
        axisX.setTickCount(4)  # 차트에 표시할 날짜의 개수를 4로 지정한다.
        dt = QDateTime.currentDateTime()  # 현재 시간 정보를 QDateTime 객체로 얻어온다.

        # X축에 출력될 값의 범위를 현재 시간부터 viewLimit(120)초 이후까지 설정한다.
        # addSecs 메서드는 지정된 초 이후의 시간을 QDateTime으로 반환한다.
        axisX.setRange(dt, dt.addSecs(self.viewLimit))

        axisY = QValueAxis()  # 정수를 저장하는 축을 생성하고 축의 레이블을 차트에 표시하지 않는다.
        axisY.setVisible(False)

        self.priceChart.addAxis(axisX, Qt.AlignBottom)
        self.priceChart.addAxis(axisY, Qt.AlignRight)
        self.priceData.attachAxis(axisX)
        self.priceData.attachAxis(axisY)

        # 차트 객체 안에 여백을 최소화해서 차트를 크게 그린다.
        self.priceChart.layout().setContentsMargins(0, 0, 0, 0)

        self.priceView.setChart(self.priceChart)
        self.priceView.setRenderHints(QPainter.Antialiasing)  # 차트에 anti-aliasing을 적용한다.

        # PriceWorker 객체 생성 및 dataSent 이벤트를 연결할 슬롯을 지정한다.
        self.pw = PriceWorker(ticker)
        self.pw.dataSent.connect(self.appendData)
        self.pw.start()

    # 차트에 그릴 데이터를 입력받는다.
    def appendData(self, currPrice):
        # 정해진 데이터 개수만큼 저장되어 있다면 오래된 0번 인덱스의 데이터를 삭제한다.
        # 삭제 로직이 없다면 저장되는 데이터의 개수가 무한히 증가할 것이다.
        if len(self.priceData) == self.viewLimit:
            self.priceData.remove(0)
        dt = QDateTime.currentDateTime()

        # append 메서드는 millisecond(ms)를 입력받기 때문에 MSecsSinceEpoch() 메서드로 QDateTime 객체를 millisecond로 변환한다.
        self.priceData.append(dt.toMSecsSinceEpoch(), currPrice)

        # 차트의 축 정보를 업데이트 한다. 실시간으로 추가되는 데이터의 위치를 지정한다.
        self.__updateAxis()

    def __updateAxis(self):
        # QLineSerires 객체에 저장된 데이터를 리스트로 얻어온다.
        # pvs에 저장된 리스트 안에는 QPointF 객체로 위치 정보가 저장되어 있다.
        pvs = self.priceData.pointsVector()

        # 가장 오래된 0번 인덱스의 객체를 하나 선택해서 x 좌표에 저장된 값을 가져온다.
        # ms로 변환해서 들어간 좌표 데이터를 fromMSecsSinceEpoch 메서드를 사용해서 QDateTime 객체로 변환한다.
        dtStart = QDateTime.fromMSecsSinceEpoch(int(pvs[0].x()))

        # 데이터가 꽉 차 있다면 최근 시간 정보가 들어 있는 마지막 객체를 선택한다.
        if len(self.priceData) == self.viewLimit:
            dtLast = QDateTime.fromMSecsSinceEpoch(int(pvs[-1].x()))
        # 데이터가 꽉 차 있지 않다면 시작 위치를 기준으로 viewLimit 초 이후까지 출력한다.
        # 항상 viewLimit 개의 데이터를 출력하는데 사용된다.
        else:
            dtLast = dtStart.addSecs(self.viewLimit)

        # 앞서 얻어온 위치 정보를 보여줄 수 있도록 X 축의 범위를 설정한다.
        ax = self.priceChart.axisX()
        ax.setRange(dtStart, dtLast)

        # QPointF 객체에서 y 좌표를 가져와서 최소값, 최대값으로 Y축에 표시될 범위를 지정한다.
        ay = self.priceChart.axisY()
        dataY = [v.y() for v in pvs]
        ay.setRange(min(dataY), max(dataY))

    # QWidget에 정의된 메서드로 UI의 종료 버튼을 누르면 실행된다.
    # 자식 클래스에서 closeEvent를 재정의해서 종료되기 전 쓰레드를 종료한다.
    def closeEvent(self, event):
        self.pw.close()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    # 이벤트 루프 사이에서 위젯을 생성한다.
    app = QApplication(sys.argv)
    cw = ChartWidget()
    cw.show()
    exit(app.exec_())
