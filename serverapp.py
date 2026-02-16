import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QMessageBox,QVBoxLayout,QLabel,QHBoxLayout,QInputDialog,QListWidget
from PyQt5.QtGui import QFont
import sys
import subprocess
import os
import cpuinfo
import GPUtil

class ServerWin(QWidget):

    '''Главное меню'''

    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle('Мастер конфигурации шаблонов')
        self.setGeometry(1000, 500, 50, 200)
        self.font = QFont("Times", 14, 500,False)
        self.font2 = QFont("Times", 10, 500,False)
        self.helloLabel = QLabel('Список шаблонов:', self)
        self.helloLabel.setFont(self.font)

        self.listTemp = QListWidget()
        dirTemp = os.listdir("C:\\share\\")
        self.listTemp.addItems(dirTemp)

        self.button = QPushButton('Проверить соединение', self)
      
        self.button.clicked.connect(self.onClick)

        self.vL = QVBoxLayout()
        self.vL.addWidget(self.listTemp)
        self.vL.addWidget(self.helloLabel,Qt.AlignCenter)
        self.vL.addWidget(self.button,Qt.AlignCenter)
        
        self.setLayout(self.vL)
    def onClick(self):
        pass
if __name__ == '__main__':

    app = QApplication(sys.argv)
    welc = ServerWin()
    welc.show()
    sys.exit(app.exec_())