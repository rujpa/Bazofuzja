import sys
import pandas as pd

from src.plugins.core import Logger
from src.plugins.core import TableData

from ast import Pass
from tkinter.messagebox import NO
from sqlalchemy import text
import psutil

class DatabaseConnection:
    
    ifLoginNeeded = True
    def __init__(self, host, user, password, database = "",  uiOutput = None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.engine = None
        self.connection = None
        self.Chunksize = None
        
        self.logger = Logger.Logger(self.getName() + "_" + self.user + "_log.txt", uiOutput)
        
        self.connection = None
        self.connect()
    
    def setIfLoginNeeded(self,newIfLogin):
        self.ifLoginNeeded = newIfLogin
        
    def getHost(self):
        return self.host
        
    def getUser(self):
        return self.user
        
    def getPassword(self):
        return self.password
        
    def getDatabase(self):
        return self.database
        
    def getIfLoginNeeded(self):
        return self.ifLoginNeeded
        
    def setDatabase(self, database, ifReload = False):
        self.database = database
        
        self.logger.createLog("setDatabase", "Selecting new database", True)
        
        if ifReload:
            self.close()
            self.connect()     
            
    def getFilePath(self):
        return self.filename

    def close(self):
        self.connection.close()
        self.logger.createLog("close", "Database disconnected", True)
        self.logger.closeFile()
        
        
    def commit(self):
        self.connection.commit()
        
    
    def getName(self):
        return str(type(self).__name__)
        
        
    def executeQuery(self, query):

        try:
            result = self.connection.execute(text(query))
        
        except Exception as ex:
            self.logger.createLog("executeQuery", "Query execution failed", True)
            raise ex
            return None

        else:
            self.logger.createLog("executeQuery", "Query executed successfully", True)
            return result
    

    def getTableAsDataFrame(self, tableName):
        query = "SELECT * FROM " + str(tableName) + ";"
        df = pd.read_sql(query, self.connection)
        
        result = TableData.TableData(tableName, df)
        
        self.logger.createLog("getTableAsDataFrame", "Imported table " + tableName + " as dataframe", True)
        return result
    
    
    def exportTableToDatabase(self, table, ifExists = "append"): #ifExists może mieć formę ["append", "replace"] w zależności od wybranej opcji
        try:
            if isinstance(table, TableData.TableData):
                frame = table.getDataFrame()
                frame.to_sql(table.getTableName(), con = self.connection, index = False, if_exists = ifExists)    
        
        except Exception as ex:
            self.logger.createLog("exportTableToDatabase", "Table Export Failed: " + str(ex), True)

        else:
            self.logger.createLog("exportTableToDatabase", "Exported table " + table.getTableName() + " to database" , True)
        
        
    def chunking(self,table):
       # print("chunking")
       # print(table)
       # print("koniec")
        
        chunkQuery = "SELECT * FROM " + table + " LIMIT 1;"
        df = pd.read_sql(chunkQuery, self.connection)
        one = df.memory_usage(deep=True).sum()
                    
        chunkQuery = "SELECT * FROM " + table + " LIMIT 2;"
        df = pd.read_sql(chunkQuery, self.connection)
        two = df.memory_usage(deep=True).sum()

        row = two - one
        metadata = one - row

        mem = psutil.virtual_memory()[1]
        memLimit = (mem * 0.5) - metadata
        self.Chunksize = int(memLimit/row)
        
        
    #to implement in subclasses
                
    def connect(self):
        pass
    
    def getTableList(self):
        pass

    def getPrimaryKeys(self):
        pass
    
    
    def getForeignKeys(self):
        pass
    
    def addPrimaryKey(self, tableName, columnName):
        pass
    
    
    def addForeignKey(self, constraintName, tableName, columnName, referencedTableName, referencedColumnName):
       pass