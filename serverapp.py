import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QMessageBox,QVBoxLayout,QLabel,QHBoxLayout,QInputDialog,QListWidget
from PyQt5.QtGui import QFont
import sys
import subprocess
import os


class ServerWin(QWidget):

    '''Главное меню'''

    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle('Мастер конфигурации шаблонов')
        self.setGeometry(800, 500, 500, 500)
        self.font = QFont("Times", 14, 500,False)
        self.font2 = QFont("Times", 10, 500,False)
        self.helloLabel = QLabel('Список шаблонов:', self)
        self.helloLabel.setFont(self.font2)

        self.listTemp = QListWidget()
        dirTemp = os.listdir("C:\\share\\")
        self.listTemp.addItems(dirTemp)

        self.checkButton = QPushButton('Проверить соединение', self)
        self.addTempButton = QPushButton('Добавить шаблон', self)
        
        self.checkButton.clicked.connect(self.onClick)
        self.addTempButton.clicked.connect(self.addTemp)

        self.vL = QVBoxLayout()
        
        self.vL.addWidget(self.helloLabel)
        self.vL.addWidget(self.listTemp,Qt.AlignCenter)
        
        self.hL = QHBoxLayout()
        
        self.hL.addWidget(self.checkButton,Qt.AlignCenter)
        self.hL.addWidget(self.addTempButton,Qt.AlignCenter)
        
        self.vL.addLayout(self.hL)
        self.setLayout(self.vL)
        
    def onClick(self):
        
        self.client, ok = QInputDialog.getText(self,'Введите ip клиента','ip клиента')
        
        try: 

            if self.client != "" and ok:

                self.connect = subprocess.run(['ping', str(self.client)], capture_output=True, text=True,encoding='cp866')
                #print(self.connect.stdout)
                temp = str(self.connect).find('время') > -1

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
                    
        except:

            mes = QMessageBox()
            mes.setText('Такого клиента не существует!')
            mes.show()
            mes.exec_()

        self.checkButton.adjustSize()
    def addTemp(): 
        dir = os.getcwd()
        print(dir)
if __name__ == '__main__':

    app = QApplication(sys.argv)
    welc = ServerWin()
    welc.show()
    sys.exit(app.exec_())