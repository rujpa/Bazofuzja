from src.plugins.core import DatabaseConnection 
import sqlalchemy

class MySql(DatabaseConnection.DatabaseConnection):    
    
    def connect(self):
        if self.host and self.user:
            
            try:
                self.engine = sqlalchemy.create_engine('mysql+pymysql://' + self.user + ':' + self.password + '@' + self.host + '/' + self.database)
                self.connection = self.engine.connect()
                
            except Exception as ex:
                self.logger.createLog("connect", "Connection error: " + str(ex), True)
                self.conn = ""
            
            else:
                self.logger.createLog("connect", "Database connected", True)
                self.conn = "ok"   
    
    
    def getTableList(self):
        result = list()
        
        for line in self.executeQuery("SHOW TABLES;"):
            result.append(str(line[0]))
            
        return result

    
    def getPrimaryKeys(self):
        relation = self.executeQuery("SELECT TABLE_NAME, COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE CONSTRAINT_NAME = 'PRIMARY' AND table_schema = '" + self.database + "';")
        result = relation.fetchall()
        
        return result
    
    
    def getForeignKeys(self):
        relation = self.executeQuery("SELECT CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE CONSTRAINT_NAME <>'PRIMARY' AND REFERENCED_TABLE_NAME is not null;")
        result = relation.fetchall()
        
        return result
    
    
    def addPrimaryKey(self, tableName, columnName):
        try:
            self.executeQuery("ALTER TABLE " + tableName + " ADD PRIMARY KEY(" + columnName + ");")
            
        except Exception as ex:
            self.logger.createLog("addPrimaryKey", "Primary key "  + str(tableName) + "." + str(columnName) + " insert error: " + str(ex), True)
            
        else:
            self.logger.createLog("addPrimaryKey", "Primary key "  + str(tableName) + "." + str(columnName) + " inserted ", True)
    
    
    def addForeignKey(self, constraintName, tableName, columnName, referencedTableName, referencedColumnName):
        try:
            self.executeQuery("ALTER TABLE " + tableName + " ADD CONSTRAINT " + constraintName + " FOREIGN KEY(" + columnName + ") REFERENCES " + referencedTableName + "(" + referencedColumnName + ");")
            
        except Exception as ex:
            self.logger.createLog("addForeignKey", "Relation insert error: " + str(ex), True)
            
        else:
            self.logger.createLog("addForeignKey", "Relation inserted ", True)
