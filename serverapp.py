from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QMessageBox,QVBoxLayout,QLabel,QHBoxLayout,QInputDialog,QListWidget
from PyQt5.QtGui import QFont
import sys
import subprocess
import os
from client import message
import shutil
class ServerWin(QWidget):

    '''Главное меню'''

    def __init__(self):
        super().__init__()
        if 'share' not in os.listdir('C:\\'): os.mkdir('C:\\share')
        self.initUI()
        
        

    def initUI(self):
        
        self.setWindowTitle('Мастер конфигурации шаблонов')
        self.setGeometry(600, 300, 500, 500)
        self.font = QFont("Times", 14, 500,False)
        self.font2 = QFont("Times", 10, 500,False)
        self.helloLabel = QLabel('Список шаблонов:', self)
        self.helloLabel.setFont(self.font2)

        self.listTemp = QListWidget()
        dirTemp = os.listdir("C:\\share\\")
        self.listTemp.addItems(dirTemp)

        self.checkButton = QPushButton('Проверить соединение с клиентом', self)
        self.addTempButton = QPushButton('Добавить шаблон', self)
        self.delButton = QPushButton('Удалить шаблон', self)
        self.updateButton = QPushButton('Обновить инсталяторы в шаблоне', self)
        self.addInstButton = QPushButton('Добавить пакет', self)
        self.delInstButton = QPushButton('Удалить пакет', self)


        self.progLabel = QLabel('Список пакетов в шаблоне:', self)
        self.progLabel.setFont(self.font2)

        self.listProg = QListWidget()
        
        self.checkButton.clicked.connect(self.onClick)
        self.addTempButton.clicked.connect(self.addTemp)
        self.delButton.clicked.connect(self.delTemp)
        self.updateButton.clicked.connect(self.updateTemps)
        self.listTemp.itemClicked.connect(self.showProg)
        self.addInstButton.clicked.connect(self.addInst)
        self.delInstButton.clicked.connect(self.delInst)
        self.vL = QVBoxLayout()
        
        self.vL.addWidget(self.helloLabel)
        self.vL.addWidget(self.listTemp,Qt.AlignCenter)
        self.vL.addWidget(self.progLabel)
        self.vL.addWidget(self.listProg,Qt.AlignCenter)
        self.vL.addWidget(self.checkButton)
        
        self.hL = QHBoxLayout()
        self.hL.addWidget(self.addTempButton,Qt.AlignCenter)
        self.hL.addWidget(self.delButton,Qt.AlignCenter)
        self.vL.addLayout(self.hL)
        self.hl2 = QHBoxLayout()
        self.hl2.addWidget(self.addInstButton,Qt.AlignCenter)
        self.hl2.addWidget(self.delInstButton,Qt.AlignCenter)
        self.vL.addLayout(self.hl2)
        self.vL.addWidget(self.updateButton)
        self.setLayout(self.vL)
    def showProg(self):
        try:
            if self.listTemp.selectedItems():
                dirName = self.listTemp.selectedItems()[0].text()
                progNames = os.listdir("C:\\share\\"+dirName)
                #print(progNames)
                word=''
                progListLOCAL = []
                for nupkg in progNames:
                        #print(nupkg)
                        for let in nupkg:
                            if let != '.': 
                                word+=let
                            else:
                                if nupkg.find('extension') > -1:
                                    word+='.extension'
                            
                                progListLOCAL.append(word)
                                word = '' 
                                break
                self.listProg.clear()
                self.listProg.addItems(progListLOCAL)
        except:
            message('Это не шаблон.')
                        
                        
                    
    def onClick(self):
        
        self.client, ok = QInputDialog.getText(self,'Введите ip клиента','ip клиента')        
        try: 
            if self.client != "" and ok:
                self.connect = subprocess.run(['ping', str(self.client)], capture_output=True, text=True,encoding='cp866')
                #print(self.connect.stdout)
                temp = str(self.connect).find('время') > -1
                if temp:
                    message('Соединение установлено!')

                else:
                    message('Соединение не установлено!')
                    
                    
        except:
            message('Такого клиента не существует!')

        #self.checkButton.adjustSize()
    def addTemp(self): 
        self.dirTemp, ok = QInputDialog.getText(self,'Введите название шаблона','название шаблона')
        #message(os.path.join('C:\\','share',self.dirTemp))
        if self.dirTemp != '' and ok and self.dirTemp not in os.listdir(os.path.join('C:\\','share')):
            
            os.mkdir(os.path.join('C:\\','share',self.dirTemp))
            self.listTemp.clear()
            dirTemp = os.listdir("C:\\share\\")
            self.listTemp.addItems(dirTemp)
            message(f'Шаблон {self.dirTemp} добавлен.')
            
        elif self.dirTemp in os.listdir(os.path.join('C:\\','share')):
            message('Такой шаблон уже существует!')
        else:
            message('Повторите ваш запрос')
        self.prog, ok = QInputDialog.getText(self,'Введите название пакета','название пакета')
        while self.prog != '' and ok:
            command = f'''Invoke-WebRequest -Uri "https://chocolatey.org/api/v2/package/{self.prog}/" -OutFile "C:\\share\\{self.dirTemp}\\{self.prog}.nupkg"'''
            try:
                ps_command = f'''Start-Process powershell -Verb RunAs -WindowStyle Hidden -ArgumentList ' -Command {command}' -PassThru -Wait;'''    
                self.cons = subprocess.run(["powershell", "-Command",ps_command], check=True, capture_output=True)
                message(f'{self.cons.stdout}')
            except:message(f'Не удалось добавить данный пакет.')
            self.prog, ok = QInputDialog.getText(self,'Введите пакета','название пакета')
    def delTemp(self):
        if self.listTemp.selectedItems():
            dirName = self.listTemp.selectedItems()[0].text()
            if dirName in os.listdir(os.path.join('C:\\','share')):
                shutil.rmtree(os.path.join('C:\\','share',dirName))
                self.listTemp.clear()
                dirTemp = os.listdir("C:\\share\\")
                self.listTemp.addItems(dirTemp)
                self.listProg.clear()
                message(f'Шаблон {dirName} был удалён.')
    def addInst(self):
        
        if self.listTemp.selectedItems():
            self.dirTemp = self.listTemp.selectedItems()[0].text()
            command = f'''Invoke-WebRequest -Uri "https://chocolatey.org/api/v2/package/{self.prog}/" -OutFile "C:\\share\\{self.dirTemp}\\{self.prog}.nupkg"'''
            message(self.dirTemp)
            try:
                ps_command = f'''Start-Process powershell -Verb RunAs -WindowStyle Hidden -ArgumentList ' -Command {command}' -PassThru -Wait;'''    
                self.cons = subprocess.run(["powershell", "-Command",ps_command], check=True, capture_output=True)
                message(f'{self.prog} успешно добавлен!')
            except:message(f'Не удалось добавить данный пакет.')
            self.listProg.clear()
            self.listProg.addItems(os.listdir(f'C:\\share\\{self.dirTemp}'))
    def delInst(self):
        if self.listTemp.selectedItems():
            if self.listProg.selectedItems():
                tempName = self.listProg.selectedItems()[0].text()
                instName = self.listProg.selectedItems()[0].text()
                if instName in os.listdir(os.path.join('C:\\','share',tempName)):
                    shutil.rmtree(os.path.join('C:\\','share',tempName,instName))
                    self.listProg.clear()
                    dirTemp = os.listdir(f"C:\\share\\{tempName}")
                    self.listProg.addItems(dirTemp)
                    message(f'Пакет {instName} был удалён.')        
    def updateTemps(self):
        progListLOCAL = []
        try:
            if self.listTemp.selectedItems():
                dirName = self.listTemp.selectedItems()[0].text()
                progNames = os.listdir(f"C:\\share\\{dirName}")
                message(f"{dirName} {progNames}")
                #print(progNames)
                word=''        
                for nupkg in progNames:
                        #print(nupkg)
                        for let in nupkg:
                            if let != '.': 
                                word+=let
                            else:
                                if nupkg.find('extension') > -1:
                                    word+='.extension'
                            
                                progListLOCAL.append(word)
                                word = '' 
                                break               
        except: message(f'Это не шаблон. {progListLOCAL}')
        
        for prog in progListLOCAL:
            command = f'''Invoke-WebRequest -Uri "https://chocolatey.org/api/v2/package/{prog}/" -OutFile "C:\\share\\{dirName}\\{prog}.nupkg"'''
            try:
                ps_command = f'''Start-Process powershell -Verb RunAs -WindowStyle Hidden -ArgumentList ' -Command {command}' -PassThru -Wait;'''    
                self.cons = subprocess.run(["powershell", "-Command",ps_command], check=True)
                message(f'Обновление {prog} завершено!')
            except:message('Ошибка.')
        message('Обновление завершено!')
if __name__ == '__main__':

    app = QApplication(sys.argv)
    welc = ServerWin()
    welc.show()
    sys.exit(app.exec_())