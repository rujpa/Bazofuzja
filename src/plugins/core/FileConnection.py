import pandas as pd

from src.plugins.core import Logger

class FileConnection():
    ifLoginNeeded = False
    def __init__(self, filepath, uiOutput=""):
        self.filepath = filepath
        self.ui = uiOutput
        
        tokens = filepath.replace('\\', '/').split('/')
        self.filename = str(tokens[-1])

        self.logger = Logger.Logger(self.getName() + "_" + self.filename + "_log.txt", uiOutput)
        self.logger.createLog(self.getName() + "__init__", "Preparing to open file " + self.filename, True)

        self.conn = "ok"

    def getUi(self):
        return self.ui

    def getName(self):
        return str(type(self).__name__)
        
    def getFilePath(self):
        return self.filepath
    
    def getIfLoginNeeded(self):
        return self.ifLoginNeeded
        
    def setMultipleFilenames(self,data):
        filepath2 = self.filepath.split(".")
        l = len(filepath2)
        filepath2[l-1] ="_"+ data.getTableName() +"."+filepath2[l-1]
        filepath2[l-2] = filepath2[l-2] + filepath2[l-1]
        filepath2.pop(l-1)
        
        return ".".join(filepath2)
    
    # to implement in subclasses
    
    
    def getFileAsDataFrame(self):
        pass
    
    def exportDataFrameToFile(self):
        pass
    
    
    
    # TODO:
    #   -wizard tworzący relacje automatycznie/półautomatycznie
    #       pomocna - normalizacja danych?