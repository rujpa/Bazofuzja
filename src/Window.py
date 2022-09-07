import sys
import os
from src import Ui_MainWindow
from src.plugins.core import DatabaseConnection
from src.plugins.core import FileConnection
import importlib
import src.plugins
from src.plugins.core import TableData
import pandas as pd
from src import Automation
class Window:

    def __init__(self):
        self.techIn = ""    #string z typem wejściowej bazy danych
        self.techOut = ""    #string z typem wyjściowej bazy danych
        self.fileOut = ""   
        self.mod = {}      #słownik {nazwa_klasy : klasa}
        self.DbIn = None     #obiekt zawierający wejściową baze danych
        self.DbOut = None     #obiekt zawierający wyjściową baze danych
        self.Aut = Automation.Automation(self)
        
        filepath = os.environ["HOMEPATH"]+"//operation.bin"
        
        
        self.LoadPlugins()
        
    def clearAll(self):
        self.DbIn = None    
        self.DbOut = None
        self.techIn = ""   
        self.techOut = ""    
        self.fileOut = ""

    def LoadPlugins(self):
    
        self.mod.clear()
        pathToFiles = os.path.dirname(src.plugins.__file__)
        files = os.listdir(pathToFiles)
       
       
        for x in files:
            x = x.split('.')
            if(len(x)== 2 and x[1] == "py" and x[0] and x[0] != "__init__"):
                mod = importlib.import_module("." + x[0],'src.plugins')
                self.mod[x[0]] = getattr(mod,x[0])
    
    def DatabaseList(self):
        myList = list(self.mod.keys())
        myList.sort()
        return myList
        
        
    def login(self,ui,dbNameStr):
        Db = self.mod[dbNameStr](ui.databaseAddress.text(), ui.databaseUser.text(), ui.databasePassword.text(), ui.databaseName.text(),ui.promptBar)
        if (Db.conn == "ok"):
            return Db
        else:
            return None
        
    def isLoginFormNeeded(self, tech):
    # true - wymaga logowania, false - wymaga pliku
        return self.mod[tech].ifLoginNeeded
        
    def isFlatFile(self,db):
        if isinstance(db,FileConnection.FileConnection):
            return True
        return False
        
    def isDatabase(self,db):
        if isinstance(db,DatabaseConnection.DatabaseConnection):
            return True
        return False

    def returnName(self,Db):
        return str(type(Db).__name__)
            
    def setDbIn(self,DbIn):
        self.DbIn = DbIn
    
    def setDbOut(self,DbOut):
        self.DbOut = DbOut
        
    def setTechIn(self,techIn):
        self.techIn = techIn
        
    def setTechOut(self,techOut):
        self.techOut = techOut
    
    def getDbIn(self):
        return self.DbIn
            
    def getDbOut(self):
        return self.DbOut
        
    def getTechIn(self):
        return self.techIn
    
    def getTechOut(self):
        return self.techOut

    #def getFileName(self, db):
    def getData(self,table):
        tableList = []
        for x in self.chunkList:
            if(x.getTableName() == table):
                tableList.append(x)
        return tableList
        
    def autoSave(self):
        self.Aut.save()
        
    def autoRead(self,filepath):
        self.Aut.read(filepath)
        
        
    def loadLogin(self,ui,Db):
        #Db to DbIn lub DbOut
        if Db is not None:
            ui.databaseAddress.setText(Db.getHost())
            ui.databaseUser.setText(Db.getUser())
            ui.databasePassword.setText(Db.getPassword())
            ui.databaseName.setText(Db.getDatabase())
            
    def loadTableList(self,tab):
        tab.clear()
        for x in self.DbIn.getTableList():
            tab.addItem(str(x))
            
    def fileIn(self,dbNameStr,fileName,ui):
        Db = self.mod[dbNameStr](fileName,ui.promptBar)
        
        if (Db.conn == "ok"):
            return Db
        else:
            return None
    
                
    def getTable(self,TableList=[],newTableList=[]):
        self.chunkList = []
        self.chunkNum = []
        
        self.Aut.addOperation("getTable",[TableList,newTableList])
        
        for i in range(0,len(TableList)):    
            if self.isDatabase(self.DbIn):
                self.DbIn.chunking(TableList[i])
                if self.DbIn.Chunksize != 0:
                    chunk = pd.read_sql("SELECT * FROM " + TableList[i], self.DbIn.connection, chunksize=self.DbIn.Chunksize)

                    for chunk_dataframe in chunk:
                            
                        table = TableData.TableData(TableList[i], chunk_dataframe)
                        table.setTableName(newTableList[i])
                        self.chunkList.append(table)
                        self.chunkNum.append(i)
                        
        if self.isFlatFile(self.DbIn):
            table = self.DbIn.getFileAsDataFrame()
            self.chunkList.append(table)
            self.chunkNum.append(0)
 
                

        
    def exportTable(self,ifExists = "append"):

        self.Aut.addOperation("exportTable",[ifExists])
        
        x = -1
        
        for i in range(len(self.chunkList)):
            table = self.chunkList[i]
            if x != i:
                IfFirst = True
                x = i
            
            if self.isDatabase(self.DbOut):
                self.DbOut.exportTableToDatabase(table, ifExists) if IfFirst else self.DbOut.exportTableToDatabase(table, "append")
                
            elif self.isFlatFile(self.DbOut):
                self.DbOut.exportDataFrameToFile(table)  
                
        
    
    
#-------------------Relacje /Paulina
    def getFilePath(self,db):
        return db.getFilePath()

    def getPrimaryKeys(self):
        return self.DbIn.getPrimaryKeys()
        
    def getForeignKeys(self):
        return self.DbIn.getForeignKeys()

    def addPrimaryKey(self, tableName, columnName):
        self.DbOut.addPrimaryKey(tableName, columnName)

    def addForeignKey(self, constraintName, tableName, columnName, referencedTableName, referencedColumnName):
       self.DbOut.addForeignKey(constraintName, tableName, columnName, referencedTableName, referencedColumnName)
       
#-----------------------------------------------------------------     

    def deleteInterpolar(self, tablename = ""):
        self.Aut.addOperation("deleteInterpolar",[tablename])
        if(tablename == "" and len(self.chunkList)==1):
            self.chunkList[0].interpolateNullRecords()
        else:
            data = self.getData(tablename)
            for x in data:
                x.interpolateNullRecords()
                
    def deleteNullsFun(self, tablename = ""):
        self.Aut.addOperation("deleteNullsFun",[tablename])
        
        if(tablename == "" and len(self.chunkList)==1):
            self.chunkList[0].removeNullRows()
        else:
            data = self.getData(tablename)
            for x in data:
                x.removeNullRows()

    def deleteDupliFun(self,tablename = ""):
        self.Aut.addOperation("deleteDupliFun",[tablename])
        
        if(tablename == "" and len(self.chunkList)==1):
            self.chunkList[0].removeDuplicates()
        else:
            data = self.getData(tablename)
            for x in data:
                x.removeDuplicates()   
       
    def createTable(self,tempL, listOfTables): #funkcja do Window
        self.Aut.addOperation("createTable",[tempL, listOfTables])
        data = self.DbIn.getFileAsDataFrame()
        self.chunkList.clear()
        self.chunkNum.clear()
        x = 0
        
        for i in tempL:
            df = pd.DataFrame({})
            for j in listOfTables:
                if i == j[0]:
                    df.insert(loc = 0, column = j[1], value = data.getDataFrame()[j[1]].tolist())
            table = TableData.TableData(i, df)
            self.chunkList.append(table)
            self.chunkNum.append(x)
            x = x + 1
            self.exportTable("replace")
                    
#-------------------Relacje /Paulina    
    def closeAll(self,main_win):
        try:
            if(self.mod[techIn].conn == "ok"):
                self.mod[techIn].close()
            if(self.mod[techOut].conn == "ok"):
                self.mod[techOut].close()
        except:
            pass
        
    