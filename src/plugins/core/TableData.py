import pandas as pd

class TableData:
    
    def __init__(self, tableName, tableDataFrame):
        if isinstance(tableDataFrame, pd.DataFrame):
            self.tableName = tableName
            self.tableDataFrame = tableDataFrame
        
        
    def getDataFrame(self):
        return self.tableDataFrame
    
    
    def getTableName(self):
        return self.tableName
    
    
    def setTableName(self, name):
        self.tableName = name
    
    
    def removeNullRows(self):
        self.tableDataFrame = self.tableDataFrame.dropna(axis=0, how="any", thresh=None, subset=None, inplace=False)
        

    def removeNullColumns(self):
        self.tableDataFrame = self.tableDataFrame.dropna(axis=1, how="any", thresh=None, subset=None, inplace=False)
    
    
    def removeByIndex(self, i): # 'i' can be either single label or a list
        self.tableDataFrame = self.tableDataFrame.drop(index = i)
        
        
    def removeColumn(self, i): # 'i' can be either single label or a list
        self.tableDataFrame = self.tableDataFrame.drop(index = i, axis = 1)
        

    def removeDuplicates(self):
        self.tableDataFrame = self.tableDataFrame.drop_duplicates()
        
        
    def interpolateNullRecords(self):
        self.tableDataFrame = self.tableDataFrame.interpolate(method = 'linear', axis = 0)
