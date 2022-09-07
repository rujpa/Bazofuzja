import pandas as pd 

from src.plugins.core import FileConnection
from src.plugins.core import TableData

class Xml(FileConnection.FileConnection):
    
    def getFileAsDataFrame(self):
        
        try:
            table = pd.read_xml(self.filepath, encoding = 'unicode_escape')
        
        except Exception as ex:
            self.logger.createLog("getFileAsDataFrame", "Failed to import file " + str(self.filename) + " as dataframe: " + str(ex), True)
            
            return None
        
        else:
            self.logger.createLog("getFileAsDataFrame", "Imported file " + str(self.filename) + " as dataframe", True)
            result = TableData.TableData(self.filename, table)
            
            return result
        
    
    def exportDataFrameToFile(self, data):
        try:
            data.getDataFrame().to_xml(self.setMultipleFilenames(data))
            
        except Exception as ex:
            self.logger.createLog("exportDataFrameToFile", "Failed to export dataframe to a file " + str(self.filename) + ": " + str(ex), True)
            
        else:
            self.logger.createLog("exportDataFrameToFile", "Exported dataframe to a file " + str(self.filename), True)
