import argparse
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
from MainWindow import MainWindow
from os.path import exists


parser = argparse.ArgumentParser()
parser.add_argument('filepath', metavar = 'filepath', type = str, help = 'Filepath to .sav file containing previously saved bazofuzja configuration')

args = parser.parse_args()

if not os.path.isfile(str(args.filepath)):
    print("Specified file does not exist")
    sys.exit()

if str(args.filepath).split('.')[-1] != 'bin':
    print("Specified file does not have the needed extension [.bin]")
    sys.exit()
    
print('Opening ' + str(args.filepath))

app = QApplication(sys.argv)
main_win = MainWindow()

myPath = os.path.dirname(os.path.abspath(__file__)) + "\\" + args.filepath
print(myPath)
main_win.Win.Aut.read(myPath)