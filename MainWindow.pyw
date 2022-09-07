#pyuic5 -x projectUI.ui -o Ui_MainWindow.py

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QDialogButtonBox, QInputDialog
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton

from PyQt5.QtCore import Qt
import os

from src import Ui_MainWindow
from src import Window

import tablenamesForm
import Ui_tablePreview
import Ui_addRelation
import pandas as pd


class addRelationForm():
    def __init__(self):
        self.extraWin = QMainWindow()
        self.extraUi = Ui_addRelation.Ui_addRelationWin()
        self.extraUi.setupUi(self.extraWin)
        self.extraUi.addRelationBtn.clicked.connect(self.add)
    def add(self):
        if self.extraUi.selTab.text() != "" and self.extraUi.selTabK.text() != ""and self.extraUi.conTab.text() != "" and self.extraUi.conTab.text() != "":
            l = []
            l.append(self.extraUi.selTab.text())
            l.append(self.extraUi.selTabK.text())
            l.append(self.extraUi.conTab.text())
            l.append(self.extraUi.conTabK.text())
            MainWindow.setRow(main_win,l)
            self.extraWin.close()

    def show(self):
        self.extraWin.show()

    def clear(self):
        l = []
        self.extraUi.selTab.setText("")
        self.extraUi.selTabK.setText("")
        self.extraUi.conTab.setText("")
        self.extraUi.conTabK.setText("")


class tablePreviewForm():
    def __init__(self):
        self.extraWin = QMainWindow()
        self.extraUi = Ui_tablePreview.Ui_tablePreview()
        self.extraUi.setupUi(self.extraWin)
        self.extraUi.tableSelected.currentTextChanged.connect(self.loadTable)
        self.extraUi.tablePreviewWidget.horizontalHeader().setStretchLastSection(True)

    def show(self):
        self.extraWin.show()
    def clear(self):
        self.extraUi.tableSelected.clear()

    def getTableNames(self):
        self.extraUi.tableSelected.addItems(MainWindow.getSelectedTables(main_win))
     
    def loadTable(self):
        listOfColumns = []
        dat = main_win.Win.getData(self.extraUi.tableSelected.currentText())
        data = dat[0]
        for name in data.getDataFrame().columns:
            listOfColumns.append(name)
        self.extraUi.tablePreviewWidget.setColumnCount(len(listOfColumns))
        self.extraUi.tablePreviewWidget.setHorizontalHeaderLabels(listOfColumns)
        self.extraUi.tablePreviewWidget.setRowCount(0)
        rowsNumber = len(data.getDataFrame().index)

        for i in range(rowsNumber):
            self.extraUi.tablePreviewWidget.insertRow(i)
            for j in range(len(listOfColumns)):
                s = str(data.getDataFrame().iat[i,j])
                self.extraUi.tablePreviewWidget.setItem(i,j,QTableWidgetItem(s))
                


    
class MainWindow:
    def __init__(self):
        self.Win = Window.Window()
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow.Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.main_win.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.ui.stackedWidget.setCurrentWidget(self.ui.welcomeScreen)
        self.ui.menuBox.setCurrentIndex(0)
        self.listFK = []
        self.mode = 0
        self.changeMode()
        

        #przyciski:
        self.ui.exitBtn.clicked.connect(self.exit)
        self.ui.sourceInputBtn.clicked.connect(self.showSourceInput)
        self.ui.systemInputBtn.clicked.connect(self.showSystemInput)
        self.ui.selectionInputBtn.clicked.connect(self.showSelection)
        self.ui.systemOutputBtn.clicked.connect(self.showSystemOutput)
        self.ui.saveOutputBtn.clicked.connect(self.showSaveOutput) 
        self.ui.summaryBtn.clicked.connect(self.showSummary)
        self.ui.showRelationBtn.clicked.connect(self.showRelations)
        self.ui.editDataBtn.clicked.connect(self.showEditPage)

        self.ui.changeNameBtn.clicked.connect(self.showTablenames)

        self.ui.loadFileInputBtn.clicked.connect(self.loadFileInput)
        self.ui.loginBtn.clicked.connect(self.loginDatabase)
        self.ui.submitTablesBtn.clicked.connect(self.submitTables)
        self.ui.saveFileOutputBtn.clicked.connect(self.saveFileOutput)
        self.ui.submitAllBtn.clicked.connect(self.submitAll)

        self.ui.showModulesBtn.clicked.connect(self.showModulesDir)

        self.ui.deleteNullsBtn.clicked.connect(self.deleteNullsFun)
        self.ui.deleteDupliBtn.clicked.connect(self.deleteDupliFun)
        self.ui.deleteByIDBtn.clicked.connect(self.deleteByIDFun)

        self.ui.deleteRelationBtn.clicked.connect(self.deleteRelation)
        self.ui.addRelationBtn.clicked.connect(self.addRelation)

        self.ui.hideBtn.clicked.connect(self.hideWindow)
        self.ui.minBtn.clicked.connect(self.maxWindow)

        self.ui.tableShow2Btn.clicked.connect(self.showPreview)
        self.ui.tableShowBtn.clicked.connect(self.showPreview)

        self.ui.changeModeBtn.clicked.connect(self.changeMode) 

        self.ui.moveNextBtn.clicked.connect(self.showSystemOutput)

        self.ui.readAutoBtn.clicked.connect(self.readAuto)


        #dodanie do listy jakie mamy moduły baz danych
            
        for i in self.Win.DatabaseList():
            self.ui.dataSystemsTableI.addItem(i)
            self.ui.dataSystemsTableO.addItem(i)
            
        #trigger dla klikniętych list
        self.ui.dataSystemsTableI.itemClicked.connect(self.setSystemInput)
        self.ui.dataSystemsTableO.itemClicked.connect(self.setSystemOutput)
        
        #wyłącza przyciski na init
        self.ui.sourceInputBtn.setEnabled(False)
        self.ui.selectionInputBtn.setEnabled(False)
        self.ui.systemOutputBtn.setEnabled(False)
        self.ui.saveOutputBtn.setEnabled(False)
        self.ui.summaryBtn.setEnabled(False)
        self.ui.editDataBtn.setEnabled(False)
        self.ui.showRelationBtn.setEnabled(False)

        self.dialogTablename = tablenamesForm.tablenamesForm() #stworzenie obiektu
        self.dialogTablePreview = tablePreviewForm()
        self.dialogAddRelation = addRelationForm()

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setWindowTitle("Uwaga")

        self.msg2 = QMessageBox()
        self.msg2.setIcon(QMessageBox.Information)
        self.msg2.setWindowTitle("Uwaga")
        self.msg2.setText("Czy chcesz przejść do opcji zaawansowanych")
        nobtn = QPushButton('Nie')
        self.msg2.addButton(nobtn, QMessageBox.NoRole)

        self.ui.primaryWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.relationList.horizontalHeader().setStretchLastSection(True)
        self.ui.dataToTabelWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.first10Widget.horizontalHeader().setStretchLastSection(True)
        self.listP = []
    


    
#-----------------------------------------------------------#
    def show(self):
        self.main_win.show()

    def exit(self):
        self.Win.closeAll(main_win)
        self.main_win.close()
#-------------------- Czyszczenie --------------#
    def clearAll(self):
        self.ui.sourceInputBtn.setEnabled(False)
        self.ui.selectionInputBtn.setEnabled(False)
        self.ui.systemOutputBtn.setEnabled(False)
        self.ui.saveOutputBtn.setEnabled(False)
        self.ui.summaryBtn.setEnabled(False)
        self.ui.editDataBtn.setEnabled(False)
        self.ui.showRelationBtn.setEnabled(False)
        self.listP = []
        self.listFk = []
        self.cleanLoginInfo()
        self.ui.saveEditFlatCheck.setChecked(False)
        self.ui.saveRelationCheckbox.setChecked(False)
        self.ui.primaryWidget.setRowCount(0)
        self.ui.relationList.setRowCount(0)
        self.ui.dataToTabelWidget.setRowCount(0)
        self.ui.first10Widget.setRowCount(0)

    def cleanLoginInfo(self):   
        self.ui.databasePassword.setText("")
        self.ui.databaseAddress.setText("")
        self.ui.databaseName.setText("")
        self.ui.databaseUser.setText("")
#-------------------------Przyciski na pasku górnym----------------------------#
    def hideWindow(self):
        self.main_win.showMinimized()

    def maxWindow(self):
        self.main_win.showMaximized()

    def changeMode(self):
        if self.mode == 0:
            self.ui.label.setPixmap(QtGui.QPixmap("resources_png/logo_white.png"))
            colorfile = open("graphic/light.qss","r")
            self.mode = 1
        else:
            self.ui.label.setPixmap(QtGui.QPixmap("resources_png/logo_black.png"))
            colorfile = open("graphic/dark.qss","r")
            self.mode = 0
        stylesheet = str(colorfile.read())
        self.main_win.setStyleSheet(stylesheet)

    def showModulesDir(self):
        os.system('start .\src\plugins')


    #------------------ Obsługa relacji -----------------#

    def saveRelations(self): 
        if self.ui.primaryWidget.rowCount() >0:
            for i in range(self.ui.primaryWidget.rowCount()):
                self.Win.addPrimaryKey(self.ui.primaryWidget.item(i,0).text(),self.ui.primaryWidget.item(i,1).text())

        if self.ui.relationList.rowCount() >0:
            for i in range(self.ui.relationList.rowCount()):
                fkName = "FK_"
                number = 1
                result = []
                fkName += self.ui.relationList.item(i,0).text()
                fkName += "_"
                self.listFK.sort()
                for j in self.listFK:
                    if j == (fkName +str(number)):
                        number += 1

                result.append(fkName +str(number))
                self.listFK.append(fkName +str(number))
                result.append(self.ui.relationList.item(i,0).text())
                result.append(self.ui.relationList.item(i,1).text())
                result.append(self.ui.relationList.item(i,2).text())
                result.append(self.ui.relationList.item(i,3).text())
                self.Win.addForeignKey(result[0],result[1],result[2],result[3],result[4])
      

    
    #POSTAWIĆ BARIERKI

    def fillRelationTable(self):
        if self.Win.isFlatFile(self.Win.DbIn) == False:
            LPrimary = self.Win.getPrimaryKeys()
            LForeign = self.Win.getForeignKeys()
            self.ui.primaryWidget.setRowCount(0)
            row = 0
            if len(self.getSelectedTables()) >0:
                for i in LPrimary:
                    if i[0] in self.getSelectedTables():
                        self.ui.primaryWidget.insertRow(row)
                        self.ui.primaryWidget.setItem(row,0, QTableWidgetItem(str(i[0])))
                        self.ui.primaryWidget.setItem(row,1, QTableWidgetItem(i[1]))
                        row += 1

                self.ui.relationList.setRowCount(0)
                row = 0
                for i in LForeign:
                    if i[1] in self.getSelectedTables():
                        self.ui.relationList.insertRow(row)
                        self.ui.relationList.setItem(row,0, QTableWidgetItem(str(i[1])))
                        self.ui.relationList.setItem(row,1, QTableWidgetItem(i[2]))
                        self.ui.relationList.setItem(row,2, QTableWidgetItem(i[3]))
                        self.ui.relationList.setItem(row,3, QTableWidgetItem(i[4]))
                        row += 1
                    self.listFK.append(i[0])
            
        else:
            self.ui.primaryWidget.setRowCount(0)
            row = 0
            #self.splitFlatFileData()
            if self.listP != "":
                for i in self.listP:
                    print(i)
                    self.ui.primaryWidget.insertRow(row)
                    self.ui.primaryWidget.setItem(row,0, QTableWidgetItem(str(i[0])))
                    self.ui.primaryWidget.setItem(row,1, QTableWidgetItem(i[1]))
       
        

    def addRelation(self):
        if self.ui.relationBox.currentIndex() == 1:
            self.dialogAddRelation.show()
        else:
            row = self.ui.primaryWidget.rowCount()
            self.ui.primaryWidget.insertRow(row)

    def setRow(self, l):
        row = self.ui.relationList.rowCount()
        self.ui.relationList.insertRow(row)
        self.ui.relationList.setItem(row,0, QTableWidgetItem(str(l[0])))
        self.ui.relationList.setItem(row,1, QTableWidgetItem(l[1]))
        self.ui.relationList.setItem(row,2, QTableWidgetItem(l[2]))
        self.ui.relationList.setItem(row,3, QTableWidgetItem(l[3]))
        self.dialogAddRelation.clear()

    def deleteRelation(self):
        if self.ui.relationBox.currentIndex() == 1:
            self.ui.relationList.removeRow(self.ui.relationList.currentRow())
        else:
            self.ui.primaryWidget.removeRow(self.ui.primaryWidget.currentRow())
        

    #------------pokazywanie/zmiana stron---------------#
    def showTablenames(self):   #otworzenie nowego okna
        self.dialogTablename.show()
        self.dialogTablename.loadData(self.getSelectedTables())

    def showPreview(self):
        self.dialogTablePreview.clear()
        self.dialogTablePreview.getTableNames()
        self.dialogTablePreview.loadTable()
        self.dialogTablePreview.show()

    def showEditPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.dataEditScreen)
        listT = self.dialogTablename.getNewNames()
        if listT == []:
            listT = self.getSelectedTables()
        self.ui.tableListEdits.addItems(listT)

    def showRelations(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.relationMenuScreen)
        self.fillRelationTable()
        
    def showSystemInput(self):  #pokazuje liste modułów baz danych IN
        self.ui.stackedWidget.setCurrentWidget(self.ui.systemInputScreen)

    def showSystemOutput(self):
        self.ui.systemOutputBtn.setEnabled(True) #pokazuje liste modułów baz danych OUT
        self.ui.stackedWidget.setCurrentWidget(self.ui.systemOutputScreen)
        self.ui.menuBox.setCurrentIndex(1)
    
    def showSelection(self):    #wybór tabel
        if self.Win.isFlatFile(self.Win.DbIn):
            self.ui.stackedWidget.setCurrentWidget(self.ui.tablesFlatScreen)
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.selectionScreen)
        self.ui.selectionInputBtn.setEnabled(True)
        

    def showSummary(self):  #podsumowanie
        self.ui.summaryBtn.setEnabled(True)
        self.ui.stackedWidget.setCurrentWidget(self.ui.reportScreen)
        self.ui.editDataBtn.setEnabled(True)
        self.putDataSum()
        self.ui.showRelationBtn.setEnabled(True)
        self.ui.menuBox.setCurrentIndex(3)
      

    def showSaveOutput(self):   #wybiera metode logowanie/plik dla OUT
        if self.Win.isFlatFile(self.Win.DbIn) == False:
            listT = self.dialogTablename.getNewNames()
            if listT == []:
                listT = self.getSelectedTables()

            self.Win.getTable(self.getSelectedTables(),listT)
        if self.Win.isFlatFile(self.Win.DbIn): #jeśli to plik to rozdziel dane
            if self.ui.saveEditFlatCheck.isChecked():
                self.splitFlatFileData()

        self.cleanLoginInfo()
        self.ui.saveOutputBtn.setEnabled(True)
        if self.Win.isLoginFormNeeded(self.Win.techOut):
            self.ui.labelForLogin.setText("wyjściowych")
            self.ui.stackedWidget.setCurrentWidget(self.ui.loginScreen)
            if self.ui.rememberMeCheckbox.isChecked() == True:
                self.Win.loadLogin(self.ui,self.Win.DbIn)
    
            else:
                self.Win.loadLogin(self.ui,self.Win.DbOut)

            self.ui.rememberMeCheckbox.setDisabled(True) #do sprawdzenie jak będzie działać logowaniez remember
            
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.saveOutputScreen)

    def showSourceInput(self):  #wybiera metode logowanie/plik dla IN
        self.cleanLoginInfo()
        self.ui.sourceInputBtn.setEnabled(True)
        
        if self.Win.isLoginFormNeeded(self.Win.techIn):
            self.ui.labelForLogin.setText("wejściowych") 
            self.ui.stackedWidget.setCurrentWidget(self.ui.loginScreen)
            self.ui.rememberMeCheckbox.setDisabled(False)

            self.Win.loadLogin(self.ui,self.Win.DbIn)

        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.fileInputScreen)

    #------------zapisanie bazy I/O---------------#
    def setSystemInput(self, item):
        self.Win.techIn = item.text()
        self.showSourceInput()

    def setSystemOutput(self, item):
        self.Win.techOut = item.text()
        self.showSaveOutput()

    #------------Funkcje pomocnicze--------------------#
    def getSelectedTables(self):
        result = []
        for x in self.ui.tableWidget.selectedItems():
            result.append(x.text())
        return result

    #------funkcje dla przycisków edycji-------------#

    def deleteNullsFun(self):
        tablename =  self.ui.tableListEdits.currentText()
        self.Win.deleteNullsFun(tablename)

        self.msg.setText("Usunięto puste rekordy")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec()
        self.ui.sumExtra.append("Usunięto puste rekordy")


    def deleteDupliFun(self):
        tablename =  self.ui.tableListEdits.currentText()
        self.Win.deleteDupliFun(tablename)

        self.msg.setText("Usunięto duplikaty rekordów")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec()
        self.ui.sumExtra.append("Usunięto duplikaty rekordów")
        #miejsce na usuwanie duplikatow

    def deleteByIDFun(self):
        tablename =  self.ui.tableListEdits.currentText()
        self.Win.deleteInterpolar(tablename)

        self.msg.setText("Zastosowano iterpolacje pustych rekordów")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec()
        self.ui.sumExtra.append("Zastosowano iterpolacje pustych rekordów")

    #------------ dane źródłowe -------------------#

    def loadFileInput(self):    #metoda dla wejścia z pliku
     
        fileInputName = QFileDialog.getOpenFileName(self.main_win, caption="Wybierz plik", directory= os.path.expanduser("~/Desktop"), filter= "Wszystkie pliki (*.*);;Pliki baz danych (*.db);;Pliki arkuszy MS Excel (*.xls);;Pliki csv (*.csv);;Pliki znacznikowe xml (*.xml);;Pliki JSON (*.json)") 
        if fileInputName[0] == "":
            QMessageBox.about(self.main_win, "Błąd pliku wejściowego", "Niepoprawny plik wejściowy")
        else:
            QtCore.QFile(fileInputName[0])
            self.Win.DbIn = self.Win.fileIn(self.Win.techIn,fileInputName[0], self.ui)
            if self.Win.DbIn is not None:
                if self.Win.isDatabase(self.Win.DbIn):
                    self.Win.loadTableList(self.ui.tableWidget)
                    
                else:
                    self.Win.getTable()
                    self.loadFlatPreview()
                self.showSelection()


#----------------- zapis danych ---------------#
    def saveFileOutput(self):   #metoda dla wyjścia do pliku
        resultTemporary = False

        fileOutputName = QFileDialog.getSaveFileName(self.main_win, caption="Zapisz plik",  directory= os.path.expanduser("~/Desktop"), filter= "Wszystkie pliki (*.*);;Pliki baz danych (*.db);;Pliki arkuszy MS Excel (*.xls);;Pliki csv (*.csv);;Pliki znacznikowe xml (*.xml);;Pliki JSON (*.json)")
        
        if fileOutputName[0] == "" :
            QMessageBox.about(self.main_win, "Błąd pliku wyjściowego", "Niepoprawny plik wyjściowy")
        else:
            QtCore.QFile(fileOutputName[0])
            self.Win.DbOut = self.Win.fileIn(self.Win.techOut,fileOutputName[0],self.ui)
            if self.Win.DbOut is not None:
                resultTemporary = True  #if saving to file is successful

        if resultTemporary:
            yesbtn = QPushButton('Tak')
            self.msg2.addButton(yesbtn, QMessageBox.YesRole)
            self.msg2.exec()
            if  self.msg2.clickedButton() == yesbtn:
                self.showEditPage()
                self.ui.summaryBtn.setEnabled(True)
                self.ui.editDataBtn.setEnabled(True)
                self.ui.showRelationBtn.setEnabled(True)
                self.ui.menuBox.setCurrentIndex(2)
            else:
                self.showSummary()
            self.msg2.removeButton(yesbtn)

#---------------------- Logowanie ----------------#

    def loginDatabase(self):    #obsługa logowania
        resultTemporary = False
        if (self.ui.databaseName.text() == "test"):
            self.ui.databaseAddress.setText("192.168.56.101")
            self.ui.databaseUser.setText("pracownik")
            self.ui.databasePassword.setText("pass")
            self.ui.databaseName.setText("CentrumSportowe")

        if(self.ui.databaseName.text() == "mysql"):
                self.ui.databaseAddress.setText("remotemysql.com")
                self.ui.databaseUser.setText("9IDsP75Tm5")
                self.ui.databasePassword.setText("tcvZHWSUHX")
                self.ui.databaseName.setText("9IDsP75Tm5")

        if self.ui.labelForLogin.text() == "wyjściowych":
            if self.ui.databaseName.text() != "": #todo znajdz lepszy sposób
                self.Win.DbOut = self.Win.login(self.ui,self.Win.techOut)
                self.Win.loadLogin(self.ui,self.Win.DbOut)
                
                if(self.Win.DbOut is not None):
                    resultTemporary = True #if login is successful
                  
            if resultTemporary:
      
                yesbtn = QPushButton('Tak')
                self.msg2.addButton(yesbtn, QMessageBox.YesRole)
                self.msg2.exec()
                if  self.msg2.clickedButton() == yesbtn:
                    self.showEditPage()
                    self.ui.summaryBtn.setEnabled(True)
                    self.ui.editDataBtn.setEnabled(True)
                    self.ui.showRelationBtn.setEnabled(True)
                    self.ui.menuBox.setCurrentIndex(2)
                else:
                    self.showSummary()
                self.msg2.removeButton(yesbtn)
               
        else:
            #dane do logowanie na szybko, potrzebne dla funkcji tekstowych logowania

            if self.ui.databaseName.text() != "" and self.ui.databaseUser.text() != "" and self.ui.databaseAddress.text() != "" and self.ui.databasePassword.text() != "" :
                self.Win.DbIn = self.Win.login(self.ui,self.Win.techIn)
                self.Win.loadLogin(self.ui,self.Win.DbIn)
            if(self.Win.DbIn is not None):
                resultTemporary = True 
                self.Win.loadTableList(self.ui.tableWidget)
        
            if resultTemporary:
                self.showSelection()
#=-----------obsługa automatyzacji----------#
    def readAuto(self):
        file = QFileDialog.getOpenFileName(self.main_win, caption="Wybierz plik", directory= os.path.expanduser("~/Desktop"), filter= "Wszystkie pliki (*.*);;Pliki binarne (*.bin)")
        if file[0] != "":
            self.Win.autoRead(file[0])
            #data =  self.Win.autoInfo()
            self.showSummary()

#-----------zapisy-------------#
    def submitTables(self): #zatwierdza tabele

        resultTemporary = False
        self.ui.tableListEdits.clear()
        resultTemporary = True  #if submmit table is successful

        if resultTemporary:
            self.showSystemOutput()

    def submitAll(self):    #wykonuje i zamyka aplikację
        
           
        if self.Win.DbOut is not None:

            if self.ui.appendRadio.isChecked():
                self.Win.exportTable("append")
            else: 
                self.Win.exportTable("replace")

            if (self.ui.saveRelationCheckbox.isChecked() or self.ui.dataTableRadio.isChecked()) and self.Win.isFlatFile(self.Win.DbOut) == False:
                self.saveRelations()

        if self.ui.saveToBatchCheck.isChecked():
            self.Win.autoSave()
            #wykonaj funkcję zapisu
       
        self.Win.clearAll()
        self.clearAll()
        self.msg.setText("Wykonano operację!\nWyczyszczono pamięć aplikacji")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec()
        self.ui.stackedWidget.setCurrentWidget(self.ui.welcomeScreen)
    
    ''' 
    Niegotowe funkcje 
    ||
    V
    '''
#---------------------Raport---------------------------#
    def createStr(self):
        l = []
        l.append(self.ui.databaseUser.text())
        l.append("@")
        l.append(self.ui.databaseAddress.text())
        l.append("/")
        l.append(self.ui.databaseName.text())
        return ''.join(l)
        
    def putDataSum(self):
        self.ui.sumSystemIn.setText(self.Win.getTechIn())
        if self.Win.isLoginFormNeeded(self.Win.getTechIn()):
            self.Win.loadLogin(self.ui,self.Win.DbIn)
            self.ui.sumSource.setText(str(self.createStr()))
        else:
            self.ui.sumSaved.setText(self.Win.getFilePath(self.Win.DbIn))

        self.ui.sumSystemOut.setText(self.Win.getTechOut())
        if self.Win.isLoginFormNeeded(self.Win.getTechOut()):
            self.Win.loadLogin(self.ui,self.Win.DbOut)
            self.ui.sumSaved.setText(str(self.createStr()))
        else:
           self.ui.sumSaved.setText( self.Win.getFilePath(self.Win.DbOut))
            
        
        self.collectOperations()

#---------------- Obsługa strony edycji plików płaskich -------------#
    def loadFlatPreview(self):
        data = self.Win.DbIn.getFileAsDataFrame()
        #print(data.getDataFrame())
        listOfColumns = []
        for name in data.getDataFrame().columns:
            listOfColumns.append(name)
        self.ui.first10Widget.setColumnCount(len(listOfColumns))
        self.ui.first10Widget.setHorizontalHeaderLabels(listOfColumns)
        self.ui.first10Widget.setRowCount(0)

        rowsNumber = len(data.getDataFrame().index)
        if rowsNumber >= 10: rowsNumber = 10

        for i in range(rowsNumber):
            self.ui.first10Widget.insertRow(i)
            for j in range(len(listOfColumns)):
                s = str(data.getDataFrame().iat[i,j])
                self.ui.first10Widget.setItem(i,j,QTableWidgetItem(s))
        self.createNewRows(len(listOfColumns))

    def createNewRows(self,number):
       
        self.ui.dataToTabelWidget.setRowCount(number)
        for i in range(number):
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)       
            self.ui.dataToTabelWidget.setItem(i,2,chkBoxItem)

    def splitFlatFileData(self):
        howMany = 0
        tempL = []
        listOfTables = []
        #primaryL = []
       
        for i in range(self.ui.dataToTabelWidget.rowCount()):
            if self.ui.dataToTabelWidget.item(i,0) is not None:
                howMany += 1
                tempC = self.ui.dataToTabelWidget.item(i,1).text()
                if self.ui.dataToTabelWidget.item(i,2).checkState() == 2: #zmienić na checked
                    print("ratuj")
                    self.listP.append((self.ui.dataToTabelWidget.item(i,0).text(),tempC))
                if self.ui.dataToTabelWidget.item(i,0).text() not in tempL:
                   tempL.append(self.ui.dataToTabelWidget.item(i,0).text()) 
                listOfTables.append((self.ui.dataToTabelWidget.item(i,0).text(),tempC))

        print(tempL) # stworzenie tabel

        print(listOfTables) #przpisanie kolumn do tabel

        

        self.Win.createTable(tempL,listOfTables)
        ''' def createTable(self,tempL, listOfTables): #funkcja do Window
                data = self.DbIn.getFileAsDataFrame()
                for i in tempL:
                    df = pd.DataFrame({})
                    for j in listOfTables:
                        if i == j[0]:
                            df.insert(loc = 0, column = j[1], value = data.getDataFrame()[j[1]].tolist())
                    table = TableData.TableData(i, df)
                    print(table.getDataFrame())'''

        #Stworzyć bramki!!
    #------------ Zapis operacji ------------#

    def collectOperations(self):

        temp = ""
        if self.getSelectedTables() != self.dialogTablename.getNewNames():
            
            selectTemp = self.getSelectedTables()
            newTemp = self.dialogTablename.getNewNames()
            if len(selectTemp) > 0 and len(newTemp) >0:
                self.ui.sumExtra.append("Zmieniono nazwy tabel:")
                for i in range(len(selectTemp)):
                    if selectTemp[i] != newTemp[i]:
                        self.ui.sumExtra.append(selectTemp[i] + " = " + newTemp[i])
       
            
        '''
        stara nazwa tabel, nowa nazwa tabel ok
        relacje: klucze głowne, obce
        usuwanie null, dupli, kryterium ok
        usuwanie kolumn
        rozdzielenie kolumn do tabel (płaskie do niepłaskie)
        
        '''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
