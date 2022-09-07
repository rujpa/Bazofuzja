import pandas as pd

from src.plugins.core import FileConnection
from src.plugins.core import TableData

class Csv(FileConnection.FileConnection):
    
    def getFileAsDataFrame(self, separator = ','):
        
        try:
            table = pd.read_csv(self.filepath, sep = separator, encoding = 'unicode_escape')
        
        except Exception as ex:
            self.logger.createLog("getFileAsDataFrame", "Failed to import file " + str(self.filename) + " as dataframe: " + str(ex), True)
            
            return None
        
        else:
            self.logger.createLog("getFileAsDataFrame", "Imported file " + str(self.filename) + " as dataframe", True)
            result = TableData.TableData(self.filename, table)
            
            return result
        
    def exportDataFrameToFile(self, data, separator = ','):
        try:
            
            data.getDataFrame().to_csv(self.setMultipleFilenames(data), sep = separator)
            
        except Exception as ex:
            self.logger.createLog("exportDataFrameToFile", "Failed to export dataframe to a file " + str(self.filename) + ": " + str(ex), True)
            
        else:
            self.logger.createLog("exportDataFrameToFile", "Exported dataframe to a file " + str(self.filename), True)
