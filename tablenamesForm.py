
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QDialogButtonBox, QInputDialog
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton

from PyQt5.QtCore import Qt
import Ui_tablenamesWindow

class tablenamesForm(): #Okno do zmian nazw tabel
    def __init__(self):
        self.extraWin = QMainWindow()
        self.extraUi = Ui_tablenamesWindow.Ui_tablenameWindow()
        self.extraUi.setupUi(self.extraWin)
        self.extraWin.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.extraUi.acceptNamesBtn.clicked.connect(self.saveModifNames)
        self.extraUi.discardNamesBtn.clicked.connect(self.discardAll)

        self.modifListT = []

    def show(self):
        self.extraWin.show()
    
    def loadData(self,listT):   #wczytanie listy tabel, dodanie do nowej listy i ustawienie edytowalności
        temp = 0
        for i in listT:
            self.extraUi.nameList.addItem(i)
            self.extraUi.nameList.item(temp).setFlags(self.extraUi.nameList.item(temp).flags() |  QtCore.Qt.ItemIsEditable)
            temp += 1

    def saveModifNames(self):
    
        for i in range(self.extraUi.nameList.count()):
            self.modifListT.append(self.extraUi.nameList.item(i).text())
        self.extraWin.close()

    def discardAll(self):
        self.extraUi.nameList.clear()
        self.modifListT = []
        self.extraWin.close()
    
    def getNewNames(self):      #wywołanie funkcji zwraca liste nowych nazw
        return self.modifListT
    