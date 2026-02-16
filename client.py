import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QMessageBox,QVBoxLayout,QLabel,QHBoxLayout,QInputDialog,QListWidget
from PyQt5.QtGui import QFont
import sys
import subprocess
import os
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
    '''Окно приветствия'''
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
        self.server, ok = QInputDialog.getText(self,'Введите ip сервера','ip сервера')
        self.server = '192.168.1.170'
        try: 
            if self.server != "" and ok:
                self.connect = requests.get('http://'+self.server)
                temp = str(self.connect).find('200') > -1
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
                    
                if temp: self.nextWin()
                
        except:
            mes = QMessageBox()
            mes.setText('Такого сервера не существует!')
            mes.show()
            mes.exec_()
        self.button.setText('Проверить соединение ещё раз!')
        self.button.adjustSize()
    def nextWin(self):
        self.hide()
        self.chooseWin = ChooseWin()
        self.chooseWin.show()


class ChooseWin(QWidget):
    '''Окно выбора шаблона'''
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        
        self.setWindowTitle('Выбор шаблона')
        self.setGeometry(1000,700, 500, 200)
        self.font = QFont("Times", 14, 500,False)
        
        self.helloLabel = QLabel('Пожалуйста, выберите шаблон.', self)
        self.helloLabel.setFont(self.font)
        self.checkLabel = QLabel('Проверьте наличие установщика.', self)
        self.checkLabel.setFont(self.font)
        self.buttonChoco = QPushButton('Развернуть установщик')

        self.buttonL = QPushButton('Ученик', self)
        self.buttonT = QPushButton('Учитель', self)
        self.buttonM = QPushButton('Менеджер', self)
        self.buttonA = QPushButton('Администратор', self)

        self.listTemp = QListWidget()
        dirTemp = os.listdir("\\\\192.168.1.170\\share\\")
        self.listTemp.addItems(dirTemp)

        self.buttonChoco.clicked.connect(self.onClickChoco)
        self.buttonL.clicked.connect(self.onClickL)
        self.buttonT.clicked.connect(self.onClickT)
        self.buttonM.clicked.connect(self.onClickM)
        self.buttonA.clicked.connect(self.onClickA)
        self.listTemp.itemClicked.connect(self.tempChoose)

        self.vL = QVBoxLayout()
        self.hL1 = QHBoxLayout()
        self.hL2 = QHBoxLayout()

        self.vL.addWidget(self.helloLabel,5,Qt.AlignCenter)
        self.vL.addWidget(self.checkLabel,5,Qt.AlignCenter)
        
        self.vL.addWidget(self.buttonChoco,5,Qt.AlignCenter)

        self.hL1.addWidget(self.buttonT,Qt.AlignCenter)
        self.hL1.addWidget(self.buttonL,Qt.AlignCenter)

        self.hL2.addWidget(self.buttonM,Qt.AlignCenter)
        self.hL2.addWidget(self.buttonA,Qt.AlignCenter)

        self.vL.addLayout(self.hL1)
        self.vL.addLayout(self.hL2)
        self.vL.setSpacing(5)
        self.vL.addWidget(self.listTemp)
        self.setLayout(self.vL)

    def tempChoose(self): 
        
        if self.listTemp.selectedItems():
            self.tempName = self.listTemp.selectedItems()[0].text()
            req = '\\\\'+welc.server+'\\share\\'+self.tempName
            command = f"choco source add -n=Learner -s='"+req+"' --priority=1;"
            dirTemp = os.listdir(req)
            for i in dirTemp:
                print(i)



    def onClickChoco(self):
        try: 

            #legacy
            #self.cons = subprocess.run(["powershell.exe","Start-Process", "PowerShell", "-Verb", "RunAs;","Set-ExecutionPolicy", "Bypass", "-Scope", "Process", "-Force;", "[System.Net.ServicePointManager]::SecurityProtocol", "=", "[System.Net.ServicePointManager]::SecurityProtocol", "-bor", "3072;", "iex", "((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"])

            #PS-script
            command = "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
            ps_command = f'Start-Process powershell -Verb RunAs -WindowStyle Hidden -ArgumentList "-NoExit -Command {command}"'
            self.cons = subprocess.run(["powershell", "-Command", ps_command], check=True)

            if self.cons.stdout == None:
                mes = QMessageBox()
                mes.setText('Всё готово к установке!')
                mes.show()
                mes.exec_()

        except:
            mes = QMessageBox()
            mes.setText('Ошибка!')
            mes.show()
            mes.exec_()
        
    def onClickL(self):

        #PS-script
        command = f"choco source add -n=Learner -s='\\\\192.168.1.170\\share\\Learner' --priority=1;choco install googlechrome;choco install winrar; choco install visualstudiocode;choco install python3;choco install git.install;choco install visualstudio2019buildtools;exit"
        ps_command = f'Start-Process powershell -Verb RunAs -ArgumentList "-NoExit -Command {command}"'    
        self.cons = subprocess.run(["powershell", "-Command",ps_command], check=True)
        
        self.close()

        #legacy
        '''command = "choco install googlechrome"
        ps_command = f'Start-Process powershell -Verb RunAs -ArgumentList "-NoExit -Command {command}"'
        self.cons = subprocess.run(["powershell", "-Command", ps_command], check=True)'''

    def onClickT(self): 

        command = f"choco source add -n=Learner -s='\\\\192.168.1.170\\share\\learner' --priority=1; choco install googlechrome;choco install winrar;choco install visualstudiocode;choco install zoom;choco install python3;choco install git.install;exit"
        ps_command = f'Start-Process powershell -Verb RunAs -ArgumentList "-NoExit -Command {command}"'    
        self.cons = subprocess.run(["powershell", "-Command",ps_command], check=True)

        self.close()

    def onClickM(self): 

        command = f"choco source add -n=Learner -s='\\\\192.168.1.170\\share\\learner' --priority=1; choco install pdf24;choco install zoom;choco install winrar;choco install thunderbird;choco install wps-office-free;exit"
        ps_command = f'Start-Process powershell -Verb RunAs -ArgumentList "-NoExit -Command {command}"'    
        self.cons = subprocess.run(["powershell", "-Command",ps_command], check=True)

        self.close()

    def onClickA(self): 

        command = f"choco source add -n=Learner -s='\\\\192.168.1.170\\share\\learner' --priority=1; choco install pdf24;choco install winrar;choco install thunderbird;choco install wps-office-free;choco install telegram;exit"
        ps_command = f'Start-Process powershell -Verb RunAs -ArgumentList "-NoExit -Command {command}"'    
        self.cons = subprocess.run(["powershell", "-Command",ps_command], check=True)

        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    welc = WelcomeWin()
    welc.show()
    sys.exit(app.exec_())