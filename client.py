import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QMessageBox,QVBoxLayout,QLabel,QHBoxLayout
from PyQt5.QtGui import QFont
import sys
'''app = QApplication([])
mainwin = QWidget()
lV = QVBoxLayout()
b = QPushButton('Проверить соединение с сервером')
lV.addWidget(b)
mainwin.setLayout(lV)
def check_con():
    connect = requests.get('http://192.168.1.170')
    if str(connect).find('200') > -1:
        mes = QMessageBox()
        mes.setText('Соединение установлено!')
        mes.show()
        mes.exec_()
    else:
        mes = QMessageBox()
        mes.setText('Соединение не установлено!')
        mes.show()
        mes.exec_()
b.clicked.connect(check_con)
mainwin.show()
app.exec_()'''




class WelcomeWin(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        
        self.setWindowTitle('Мастер установки приложений')
        self.setGeometry(1000, 500, 50, 200)
        self.font = QFont("Times", 14, 500,False)
        self.helloLabel = QLabel('Привет! Первым делом проверь соединение с сервером, нажав на кнопку ниже!', self)
        self.helloLabel.setFont(self.font)

        self.button = QPushButton('Проверить соединение', self)
      
        self.button.clicked.connect(self.onClick)

        self.vL = QVBoxLayout()
        self.vL.addWidget(self.helloLabel,Qt.AlignCenter)
        self.vL.addWidget(self.button,Qt.AlignCenter)
        
        self.setLayout(self.vL)
    def onClick(self):
        connect = requests.get('http://192.168.1.170')
        temp = str(connect).find('200') > -1
        if temp:
            mes = QMessageBox()
            mes.setText('Соединение установлено!')
            mes.show()
            mes.exec_()
        else:
            mes = QMessageBox()
            mes.setText('Соединение не установлено!')
            mes.show()
            mes.exec_()
            self.button.setText('Проверить соединение ещё раз!')
            self.button.adjustSize()
        if temp: self.nextWin()
    def nextWin(self):
        self.hide()
        self.chooseWin = ChooseWin()
        self.chooseWin.show()
class ChooseWin(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        
        self.setWindowTitle('Выбор шаблона')
        self.setGeometry(1000,500, 500, 200)
        self.font = QFont("Times", 14, 500,False)
        
        self.helloLabel = QLabel('Пожалуйста, выберите шаблон, чтобы начать установку.', self)
        self.helloLabel.setFont(self.font)

        self.buttonL = QPushButton('Ученик', self)
        self.buttonT = QPushButton('Учитель', self)
        self.buttonM = QPushButton('Менеджер', self)
        self.buttonD = QPushButton('Директор', self)
        self.buttonL.clicked.connect(self.onClickL)
        self.buttonT.clicked.connect(self.onClickT)
        self.buttonM.clicked.connect(self.onClickM)
        self.buttonD.clicked.connect(self.onClickD)
        self.vL = QVBoxLayout()
        self.hL1 = QHBoxLayout()
        self.hL2 = QHBoxLayout()
        self.vL.addWidget(self.helloLabel,5,Qt.AlignCenter)
        self.hL1.addWidget(self.buttonT,Qt.AlignCenter)
        self.hL1.addWidget(self.buttonL,Qt.AlignCenter)
        self.hL2.addWidget(self.buttonM,Qt.AlignCenter)
        self.hL2.addWidget(self.buttonD,Qt.AlignCenter)
        self.vL.addLayout(self.hL1)
        self.vL.addLayout(self.hL2)
        self.vL.setSpacing(5)
        self.setLayout(self.vL)
    def onClickL(self): pass
    def onClickT(self): pass
    def onClickM(self): pass
    def onClickD(self): pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    welc = WelcomeWin()
    welc.show()
    sys.exit(app.exec_())