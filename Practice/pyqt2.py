import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):    # QMainWindow를 상속받은 윈도우
    def __init__(self):
        super().__init__()      # QMainWindow의 초기화가 필요하다.
        self.setGeometry(100, 200, 300, 400)    # 100, 200위치에 300, 400 크기의 창 생성

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()

