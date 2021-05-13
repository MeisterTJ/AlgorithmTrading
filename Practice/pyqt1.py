import sys
from PyQt5.QtWidgets import * # PyQt5 디렉토리에 있는 QtWidgets.py 파일로부터 모든 것을 import 하라

app = QApplication(sys.argv)    # QApplication 클래스의 인스턴스가 필요
label = QLabel("Hello")
label.show()

btn = QPushButton("Hello")      # 위의 label과 겹쳐서 뜨는데, 결국 2개를 꺼야 한다.
btn.show()
app.exec()                      # PyQt에서 이벤트 루프는 QApplication 클래스의 exec() 메서드를 호출함으로써 생성할 수 있다.

