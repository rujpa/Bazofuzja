# potrzebne importy
from src.modules.core import DatabaseConnection 
import sqlalchemy

# nazwa klasy musi być identyczna co do nazwy pliku
class conTemplate(DatabaseConnection.DatabaseConnection):    
    
    # # #
    # W zależności od typu bazy konieczne może być zaimplementowanie nowego konstruktora który (wedle potrzeb)
    # # #
    
    # Otwarcie połączenia
    def connect(self): 
        if self.host and self.user:
            
            try:
                self.engine = sqlalchemy.create_engine('') # String połączenia SQLAlchemy (przykładowo: 'databasetype+driver://user:password@host/database')
                self.connection = self.engine.connect()
            
            # Generowanie logów, handler wyjątków    
            except:
                self.logger.createLog("connect", "Connection error", True)
                self.conn = ""
            
            else:
                self.logger.createLog("connect", "Database connected", True)
                self.conn = "ok"   
    
    
    # Zwróć listę tabel  
    def getTableList(self):
        result = list()
        
        for line in self.executeQuery(''): # Query zwracające listę nazw dostępnych tabel
            result.append(str(line)) # Dane które należy umieścić w liście mogą mieć inną formę, w zależności od użytego query
            
        return result
    
    
    # # #
    # Dalsza część kodu do implementacji w przypadku, w którym połączenie ma obsługiwać również przenoszenie kluczy głównych i obcych
    # # #
    
    # Zwróć listę kluczy głównych tabel w bazie w postaci:
    # tableName, columnName
    def getPrimaryKeys(self):
        relation = self.executeQuery('') # Query zwracające klucze główne w postaci: 
        result = relation.fetchall()
        
        return result
    
    # Zwróć listę kluczy obcych znajdujących się w bazie w postaci:
    # constraintName  tableName  columnName  referencedTableName  referencedColumnName
    def getForeignKeys(self):
        relation = self.executeQuery('') # Query zwracające klucze główne w postaci: constraintName  tableName  columnName  referencedTableName  referencedColumnName
        result = relation.fetchall()
        
        return result
    
    
    # Dodaj pojedynczy klucz główny 
    def addPrimaryKey(self, tableName, columnName):
        try:
            self.executeQuery('') # query ALTER TABLE dodające PRIMARY KEY CONSTRAINT używając podanych danych
            
        # Generowanie logów, handler wyjątków
        except Exception as ex:
            self.logger.createLog("addPrimaryKey", "Primary key "  + str(tableName) + "." + str(columnName) + " insert error: " + str(ex), True)
            
        else:
            self.logger.createLog("addPrimaryKey", "Primary key "  + str(tableName) + "." + str(columnName) + " inserted ", True)
    
    
    # Dodaj pojedynczy klucz obcy
    def addForeignKey(self, constraintName, tableName, columnName, referencedTableName, referencedColumnName):
        try:
            self.executeQuery('') # Query ALTER TABLE dodające FOREIGN KEY CONSTRAINT używając podanych danych
            
        # Generowanie logów, handler wyjątków
        except Exception as ex:
            self.logger.createLog("addForeignKey", "Relation insert error: " + str(ex), True)
            
        else:
            self.logger.createLog("addForeignKey", "Relation inserted ", True)
