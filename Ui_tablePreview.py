# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'podglad.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_tablePreview(object):
    def setupUi(self, tablePreview):
        tablePreview.setObjectName("tablePreview")
        tablePreview.resize(785, 536)
        tablePreview.setMinimumSize(QtCore.QSize(657, 415))
        self.centralwidget = QtWidgets.QWidget(tablePreview)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_4)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.frame_4)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tableSelected = QtWidgets.QComboBox(self.frame_3)
        self.tableSelected.setMaximumSize(QtCore.QSize(150, 16777215))
        self.tableSelected.setObjectName("tableSelected")
        self.horizontalLayout_3.addWidget(self.tableSelected)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tablePreviewWidget = QtWidgets.QTableWidget(self.frame_2)
        self.tablePreviewWidget.setObjectName("tablePreviewWidget")
        self.tablePreviewWidget.setColumnCount(0)
        self.tablePreviewWidget.setRowCount(0)
        self.horizontalLayout_4.addWidget(self.tablePreviewWidget)
        self.verticalLayout.addWidget(self.frame_2)
        self.horizontalLayout.addWidget(self.frame)
        tablePreview.setCentralWidget(self.centralwidget)

        self.retranslateUi(tablePreview)
        QtCore.QMetaObject.connectSlotsByName(tablePreview)

    def retranslateUi(self, tablePreview):
        _translate = QtCore.QCoreApplication.translate
        tablePreview.setWindowTitle(_translate("tablePreview", "Bazofuzja - podgl??d"))
        self.label.setText(_translate("tablePreview", "Podgl??d tabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    tablePreview = QtWidgets.QMainWindow()
    ui = Ui_tablePreview()
    ui.setupUi(tablePreview)
    tablePreview.show()
    sys.exit(app.exec_())
