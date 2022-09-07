from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton
import Ui_tablePreview

class tablePreviewForm():
    def __init__(self, tablenames, data):
        self.extraWin = QMainWindow()
        self.extraUi = Ui_tablePreview.Ui_tablePreview()
        self.extraUi.setupUi(self.extraWin)
        self.extraUi.tableSelected.currentTextChanged.connect(self.loadTable)

    def show(self):
        self.extraWin.show()
    def clear(self):
        self.extraUi.tableSelected.clear()

    def getTableNames(self):
        self.extraUi.tableSelected.addItems(MainWindow.getSelectedTables(main_win))
     
    def loadTable(self):
        listOfColumns = []
        data = main_win.Win.getData(self.extraUi.tableSelected.currentText())
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