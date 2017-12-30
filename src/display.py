import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QGroupBox, QPushButton, QLabel, QHBoxLayout,  QVBoxLayout, QGridLayout, QFormLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPainter, QPen, QBrush, QScreen, QPixmap, QGuiApplication
from PyQt5.QtCore import *

import bp_network
import bp_mnist_loader

class Canvas(QWidget):
    def __init__(self, parent=None):
        super(Canvas,self).__init__(parent)
        self.map = [[0 for i in range(240)] for j in range(240)]
        self.mouse_down = False

        self.gb = QGroupBox(self)
        self.gb.setGeometry(0,0,240,240) #一定要有个东西把它撑起来！！不然看不到
        #self.setStyleSheet('background-color:#fff')

        self.setMouseTracking(False)
        self.pos_list = []

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        brush = QBrush(Qt.white)
        painter.setBrush(brush)
        painter.drawRect(0, 0, 240, 240)
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

    def mousePressEvent(self, event):
        self.mouse_down = True

    def mouseMoveEvent(self, event):
        pos = (event.pos().x(), event.pos().y())
        if self.mouse_down == True:
            for i in range(pos[0]-5, pos[0]+5):
                for j in range(pos[1]-5, pos[1]+5):
                    self.map[j][i] = 1
        self.pos_list.append(pos)

        self.update()

    def mouseReleaseEvent(self, event):
        self.mouse_down = False
        pos_break = (-1, -1)
        self.pos_list.append(pos_break)

        self.update()

    def map_zip(self):
        zip_map = [[0 for i in range(24)] for j in range(24)]
        for i in range(240):
            for j in range(240):
                zip_map[int(i/10)][int(j/10)] += self.map[i][j]
        return zip_map

    def map_clear(self):
        for i in self.map:
            for j in i:
                j = 0

class DisplayWindow(QWidget):
    def __init__(self, parent=None):
        super(DisplayWindow,self).__init__(parent)
        self.resize(580,270)

        self.bp = bp_network.Network()

        self.train_number = -1
        self.result_number = -1

        self.mainLayout = QHBoxLayout(self)
        self.canvasLayout = QGridLayout()
        self.menuLayout = QGridLayout()
        
        
        # 添加自定义部件（MyWidget）
        self.canvas = Canvas(self)
        self.canvas.resize(240,240)
        #self.canvas.setStyleSheet('background-color:#fff')
        self.canvasLayout.addWidget(self.canvas, 0, 0)
        
        self.menuLayout.setSpacing(10)
        # 添加编辑框（QLineEdit）
        self.button_number = []
        for i in range(10) :
            button = QPushButton(str(i), self)
            self.button_number.append(button)
            self.button_number[i].resize(self.button_number[i].sizeHint())
            #self.button_number[i].clicked.connect(self.choose_num)
            if i > 0:
                self.menuLayout.addWidget(self.button_number[i], (9-i)/3, (i+2)%3)
            else:
                self.menuLayout.addWidget(self.button_number[i], (9-i)/3, i%3)

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

        self.button_train = QPushButton("Train", self)
        self.button_train.clicked.connect(self.train)
        self.menuLayout.addWidget(self.button_train, 3, 1, 1, 1)

        self.train_number_label = QLabel(self)
        self.train_number_label.setText("-1")
        self.train_number_label.setAlignment(Qt.AlignCenter)
        self.train_number_label.setStyleSheet('background-color:#fff')
        self.menuLayout.addWidget(self.train_number_label, 3, 2, 1, 1)

        self.button_flash = QPushButton("Flash", self)
        self.button_flash.clicked.connect(self.map_flash)
        self.menuLayout.addWidget(self.button_flash, 4, 0, 1, 1)

        self.button_iden = QPushButton("Identify", self)
        self.button_iden.clicked.connect(self.iden)
        self.menuLayout.addWidget(self.button_iden, 4, 1, 1, 1)

        self.result_number_label = QLabel(self)
        '''self.result_number_label.setFixedWidth(300)
        self.result_number_label.setFixedHeight(300)'''
        self.result_number_label.setText("-1")
        self.result_number_label.setAlignment(Qt.AlignCenter)
        self.result_number_label.setStyleSheet('background-color:#fff')

        self.menuLayout.addWidget(self.result_number_label, 4, 2, 1, 1)

        self.mainLayout.addLayout(self.canvasLayout, 9)
        self.mainLayout.addLayout(self.menuLayout, 1)

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

    def train(self):
        if self.train_number >= 0:
            #self.bp.start_training(self.catch_screen())
            #self.catch_screen()
            self.BP_train(self.catch_screen(), self.train_number)

            self.train_number = -1
            self.train_number_label.setText(str(self.train_number))
            
        
    def iden(self):
        #self.result_number = self.bp.start_testing(self.catch_screen())
        #self.catch_screen()
        self.result_number = self.BP_iden(self.catch_screen())

        self.result_number_label.setText(str(self.result_number))
        self.result_number = -1

    def catch_screen(self):
        screen_map = self.canvas.map_zip()
        return screen_map
        '''for row in train_map:
            print(row)'''
        
    def map_flash(self):
        self.canvas = Canvas(self)
        self.canvas.resize(240, 240)
        self.canvasLayout.addWidget(self.canvas, 0, 0)

    def BP_train(self, train_map, train_number):
        #传入train_map，二维列表，及对应的数字train_number，请进行训练

    def BP_iden(self, iden_map):
        #请进行识别
        ans = -1
        return ans

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    w = DisplayWindow()
    w.show()
    app.exec_()