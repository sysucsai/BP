import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QGroupBox, QPushButton, QLabel, QHBoxLayout,  QVBoxLayout, QGridLayout, QFormLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import *

class Canvas(QWidget):
    def __init__(self, parent=None):
        super(Canvas,self).__init__(parent)

        self.gb = QGroupBox(self)
        self.gb.setGeometry(0,0,600,600) #一定要有个东西把它撑起来！！不然看不到
        #self.setStyleSheet('background-color:#fff')

        self.setMouseTracking(False)
        self.pos_list = []

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.black, 10, Qt.SolidLine)
        painter.setPen(pen)

        if len(self.pos_list) > 1:
            point_start = self.pos_list[0]
            for pos in self.pos_list:
                point_end = pos
                if point_end == (-1, -1):
                    point_start = (-1, -1)
                    continue
                if point_start == (-1, -1):
                    point_start = point_end
                    continue
                painter.drawLine(point_start[0], point_start[1], point_end[0], point_end[1])
                point_start = point_end

        painter.end()

    def mouseMoveEvent(self, event):
        pos = (event.pos().x(), event.pos().y())
        self.pos_list.append(pos)

        self.update()

    def mouseReleaseEvent(self, event):
        pos_break = (-1, -1)
        self.pos_list.append(pos_break)

        self.update()


class DisplayWindow(QWidget):
    def __init__(self, parent=None):
        super(DisplayWindow,self).__init__(parent)
        self.resize(940,630)

        mainLayout = QHBoxLayout(self)
        canvasLayout = QHBoxLayout()
        menuLayout = QGridLayout()
        
        
        # 添加自定义部件（MyWidget）
        self.canvas = Canvas(self)
        self.canvas.resize(600, 600)
        canvasLayout.addWidget(self.canvas)
        
        menuLayout.setSpacing(10)
        # 添加编辑框（QLineEdit）
        self.button_number = []
        for i in range(10) :
            button = QPushButton(str(i), self)
            self.button_number.append(button)
            self.button_number[i].resize(self.button_number[i].sizeHint())
            menuLayout.addWidget(self.button_number[i], i/3, i%3)

        self.button_train = QPushButton("train", self)
        menuLayout.addWidget(self.button_train, 3, 1, 1, 2)

        self.button_iden = QPushButton("Identify", self)
        menuLayout.addWidget(self.button_iden, 4, 0, 1, 2)

        self.result = QLabel(self)
        '''self.result.setFixedWidth(300)
        self.result.setFixedHeight(300)'''
        self.result.setText("9")
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setStyleSheet('background-color:#FFF')

        menuLayout.addWidget(self.result, 4, 2, 1, 1)

        mainLayout.addLayout(canvasLayout, 9)
        mainLayout.addLayout(menuLayout, 1)

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    w = DisplayWindow()
    w.show()
    app.exec_()