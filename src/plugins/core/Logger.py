from datetime import datetime

class Logger:
    def __init__(self, filename, uiOutput = None):
        self.uiOutput = uiOutput
        self.filename = filename
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        self.logFile = open(filename, "w")
        self.logFile.write('[ ' + str(filename) + ' log file starting from ' + str(now) + ' ]\n')
        
    
    def createLog(self, objectName, logString, ifPrint = False):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        
        output = "[" + dt_string + "]" + str(objectName) + ": " + str(logString) 
        
        self.logFile.write(output + '\n')
        
        if ifPrint:
            print(output)
        
            if self.uiOutput is not None:
                self.uiOutput.append(output)
    
    
    def closeFile(self):
        self.logFile.close()