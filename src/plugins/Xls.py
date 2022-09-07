import pandas as pd 

from src.plugins.core import FileConnection
from src.plugins.core import TableData

class Xls(FileConnection.FileConnection):
    
    def getFileAsDataFrame(self, sheetName = 0):
        
        try:
            table = pd.read_excel(self.filepath, sheet_name = sheetName)
        
        except Exception as ex:
            self.logger.createLog("getFileAsDataFrame", "Failed to import file " + str(self.filename) + " as dataframe: " + str(ex), True)
            
            return None
        
        else:
            self.logger.createLog("getFileAsDataFrame", "Imported file " + str(self.filename) + " as dataframe", True)
            result = TableData.TableData(self.filename, table)
            
            return result
    
      
    def exportDataFrameToFile(self, data, sheetname = "__default__"):
        try:
            if sheetname == "__default__":
                sheetname = data.getTableName()
                
            data.getDataFrame().to_excel(self.setMultipleFilenames(data), sheet_name = sheetname)
            
        except Exception as ex:
            self.logger.createLog("exportDataFrameToFile", "Failed to export dataframe to a file " + str(self.filename) + ": " + str(ex), True)
            
        else:
            self.logger.createLog("exportDataFrameToFile", "Exported dataframe to a file " + str(self.filename), True)
