from src.plugins.core import DatabaseConnection 
import sqlalchemy

class PostgreSQL(DatabaseConnection.DatabaseConnection):    
    
    def connect(self):
        if self.host and self.user:
            
            try:
                self.engine = sqlalchemy.create_engine('postgresql+psycopg2://' + self.user + ':' + self.password + '@' + self.host + '/' + self.database)
                self.connection = self.engine.connect()
                
            except Exception as ex:
                self.logger.createLog("connect", "Connection error: " + str(ex), True)
                self.conn = "" 
            
            else:
                self.logger.createLog("connect", "Database connected", True)
                self.conn = "ok"   
    
    
    def getTableList(self):
        result = list()
        
        for line in self.executeQuery("SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"):
            result.append(str(line[1]))
            
        return result

    
    def getPrimaryKeys(self):
        relation = self.executeQuery("SELECT TABLE_NAME, CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_TYPE = 'PRIMARY KEY';")
        result = relation.fetchall()
        
        return result
    
    
    def getForeignKeys(self):
        relation = self.executeQuery("SELECT tc.constraint_name, tc.table_name, kcu.column_name, ccu.table_name AS references_table, ccu.column_name AS references_field FROM information_schema.table_constraints tc LEFT JOIN information_schema.key_column_usage kcu ON tc.constraint_catalog = kcu.constraint_catalog AND tc.constraint_schema = kcu.constraint_schema AND tc.constraint_name = kcu.constraint_name LEFT JOIN information_schema.referential_constraints rc ON tc.constraint_catalog = rc.constraint_catalog AND tc.constraint_schema = rc.constraint_schema AND tc.constraint_name = rc.constraint_name LEFT JOIN information_schema.constraint_column_usage ccu ON rc.unique_constraint_catalog = ccu.constraint_catalog AND rc.unique_constraint_schema = ccu.constraint_schema AND rc.unique_constraint_name = ccu.constraint_name WHERE lower(tc.constraint_type) in ('foreign key')")
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