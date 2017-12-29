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

        self.train_number = -1
        self.result_number = -1

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
            #self.button_number[i].clicked.connect(self.choose_num)
            if i > 0:
                menuLayout.addWidget(self.button_number[i], (9-i)/3, (i+2)%3)
            else:
                menuLayout.addWidget(self.button_number[i], (9-i)/3, i%3)

        self.button_number[0].clicked.connect(self.choose_num_0)
        self.button_number[1].clicked.connect(self.choose_num_1)
        self.button_number[2].clicked.connect(self.choose_num_2)
        self.button_number[3].clicked.connect(self.choose_num_3)
        self.button_number[4].clicked.connect(self.choose_num_4)
        self.button_number[5].clicked.connect(self.choose_num_5)
        self.button_number[6].clicked.connect(self.choose_num_6)
        self.button_number[7].clicked.connect(self.choose_num_7)
        self.button_number[8].clicked.connect(self.choose_num_8)
        self.button_number[9].clicked.connect(self.choose_num_9)

        self.button_train = QPushButton("train", self)
        self.button_train.clicked.connect(self.BP_train)
        menuLayout.addWidget(self.button_train, 3, 1, 1, 1)

        self.train_number_label = QLabel(self)
        self.train_number_label.setText("-1")
        self.train_number_label.setAlignment(Qt.AlignCenter)
        self.train_number_label.setStyleSheet('background-color:#fff')
        menuLayout.addWidget(self.train_number_label, 3, 2, 1, 1)

        self.button_iden = QPushButton("Identify", self)
        self.button_iden.clicked.connect(self.BP_iden)
        menuLayout.addWidget(self.button_iden, 4, 0, 1, 2)

        self.result_number_label = QLabel(self)
        '''self.result_number_label.setFixedWidth(300)
        self.result_number_label.setFixedHeight(300)'''
        self.result_number_label.setText("-1")
        self.result_number_label.setAlignment(Qt.AlignCenter)
        self.result_number_label.setStyleSheet('background-color:#fff')

        menuLayout.addWidget(self.result_number_label, 4, 2, 1, 1)

        mainLayout.addLayout(canvasLayout, 9)
        mainLayout.addLayout(menuLayout, 1)

    def choose_num_0(self):
        self.train_number = 0
        self.train_number_label.setText(str(self.train_number))

    def choose_num_1(self):
        self.train_number = 1
        self.train_number_label.setText(str(self.train_number))

    def choose_num_2(self):
        self.train_number = 2
        self.train_number_label.setText(str(self.train_number))

    def choose_num_3(self):
        self.train_number = 3
        self.train_number_label.setText(str(self.train_number))

    def choose_num_4(self):
        self.train_number = 4
        self.train_number_label.setText(str(self.train_number))

    def choose_num_5(self):
        self.train_number = 5
        self.train_number_label.setText(str(self.train_number))

    def choose_num_6(self):
        self.train_number = 6
        self.train_number_label.setText(str(self.train_number))

    def choose_num_7(self):
        self.train_number = 7
        self.train_number_label.setText(str(self.train_number))

    def choose_num_8(self):
        self.train_number = 8
        self.train_number_label.setText(str(self.train_number))
    
    def choose_num_9(self):
        self.train_number = 9
        self.train_number_label.setText(str(self.train_number))

    def BP_train(self):
        if self.train_number >= 0:
            #pass
            self.train_number = -1
            self.train_number_label.setText(str(self.train_number))
        
    def BP_iden(self):
        self.result_number = -1
        self.result_number_label.setText(str(self.result_number))

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    w = DisplayWindow()
    w.show()
    app.exec_()