import sys
from src.plugins.core import DatabaseConnection
import sqlalchemy
from src.plugins.core import Logger

class Sqlite(DatabaseConnection.DatabaseConnection):
    
    ifLoginNeeded = False
    
    def __init__(self, filename, uiOutput = ""):
        self.filename = filename
        self.logger = Logger.Logger(filename + "_log.txt")
        self.engine = None
        self.connection = None
        self.Chunksize = None
        
        self.connect()           
    
    
    def connect(self):
        if self.filename:
            try:
                engine = sqlalchemy.create_engine('sqlite:///' + self.filename)
                self.connection = engine.connect()
            
            except Exception as ex:
                self.logger.createLog("connect", "Connection error : " + str(ex), True)
                self.conn = ""    
            
            else:
                self.logger.createLog("connect", "Database connected", True)
                self.conn = "ok"
    
    
    def getTableList(self):
        result = list()
        
        for line in self.executeQuery("SELECT name FROM sqlite_master WHERE type='table';"):
            result.append(str(line[0]))

        return result
