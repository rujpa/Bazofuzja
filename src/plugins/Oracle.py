###
# TODO:
#   1. Przeprowadzenie testow połączenia z bazą oracle
#   2. Sprawdzenie poprawnosci query użytego w metodzie getTableList()
###

from src.plugins.core import DatabaseConnection
import sqlalchemy

class Oracle(DatabaseConnection.DatabaseConnection):    
    
    def connect():
        if self.host and self.user:
            
            try:
                self.engine = sqlalchemy.create_engine('oracle+cx_oracle://' + self.user + ':' + self.password + '@' + self.host + '/' + self.database)
                self.connection = self.engine.connect()
                
            except Exception as ex:
                self.logger.createLog("connect", "Connection error: " + str(ex), True)
                self.conn = ""
            
            else:
                self.logger.createLog("connect", "Database connected", True)
                self.conn = "ok"   
    
    
    def getTableList():
        result = list()
        
        for line in self.executeQuery("SELECT table_name FROM all_tables"):
            result.append(str(line[0])) # sprawdzić, czy poprawnie zwraca listę tabel!
            
        return result
