# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addrel.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addRelationWin(object):
    def setupUi(self, addRelationWin):
        addRelationWin.setObjectName("addRelationWin")
        addRelationWin.resize(674, 205)
        self.centralwidget = QtWidgets.QWidget(addRelationWin)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.selTab = QtWidgets.QLineEdit(self.frame_3)
        self.selTab.setObjectName("selTab")
        self.horizontalLayout_2.addWidget(self.selTab)
        self.selTabK = QtWidgets.QLineEdit(self.frame_3)
        self.selTabK.setObjectName("selTabK")
        self.horizontalLayout_2.addWidget(self.selTabK)
        self.conTab = QtWidgets.QLineEdit(self.frame_3)
        self.conTab.setObjectName("conTab")
        self.horizontalLayout_2.addWidget(self.conTab)
        self.conTabK = QtWidgets.QLineEdit(self.frame_3)
        self.conTabK.setObjectName("conTabK")
        self.horizontalLayout_2.addWidget(self.conTabK)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.addRelationBtn = QtWidgets.QPushButton(self.frame_4)
        self.addRelationBtn.setGeometry(QtCore.QRect(250, 20, 75, 23))
        self.addRelationBtn.setObjectName("addRelationBtn")
        self.verticalLayout.addWidget(self.frame_4)
        self.horizontalLayout.addWidget(self.frame)
        addRelationWin.setCentralWidget(self.centralwidget)

        self.retranslateUi(addRelationWin)
        QtCore.QMetaObject.connectSlotsByName(addRelationWin)

    def retranslateUi(self, addRelationWin):
        _translate = QtCore.QCoreApplication.translate
        addRelationWin.setWindowTitle(_translate("addRelationWin", "Dodaj relacje"))
        self.label.setText(_translate("addRelationWin", "Wybrana tabela"))
        self.label_2.setText(_translate("addRelationWin", "Klucz wybranej tabeli"))
        self.label_3.setText(_translate("addRelationWin", "Połączona tabela"))
        self.label_4.setText(_translate("addRelationWin", "Klucz połączonej tabeli"))
        self.addRelationBtn.setText(_translate("addRelationWin", "Dodaj"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    addRelationWin = QtWidgets.QMainWindow()
    ui = Ui_addRelationWin()
    ui.setupUi(addRelationWin)
    addRelationWin.show()
    sys.exit(app.exec_())
