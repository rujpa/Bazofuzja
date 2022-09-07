import src.encryption
from src.encryption import EncryptionRSA as EncryptionRSA
import os
from os.path  import exists

class PasswordManager():

    def __init__(self):
        self.path = os.path.dirname(src.encryption.__file__) + "\\logins.txt"

        if(exists(self.path)):
            pass
        else:
            file = open(self.path, "w")
            file.close()
    
    allLogs = ""
    login = ""
    lineNumber = 0


    def readLogins(self):
        file = open(self.path, "r")
        self.allLogs = file.read()
        file.close()

    def addLogin(self, login, databaseName, databaseAddress):
        line = login + ' ' + databaseName + ' ' + databaseAddress
        self.readLogins()
        stop = 0
        if(self.allLogs != ""):
            logList = self.allLogs.splitlines()
            file = open(self.path, "a")
            for i in logList:
                if(i == line):
                    stop = 1
                    break                                            
            if(stop == 0):   
                file.write("\n" + line)
                file.close()
        else:
            file = open(self.path, "a")
            file.write(line)
            file.close()
        
        
    def readFittingPassword(self, login, databaseName, databaseAddress):
        cipher = EncryptionRSA.EncryptionRSA()
        line = login + ' ' + databaseName + ' ' + databaseAddress    
        
        self.readLogins()
        logList = self.allLogs.splitlines()
        for i in logList:
            if(i == line):               
                passwords = cipher.readPasswords()
                passwordList = passwords.splitlines()
                properPassword = passwordList[self.lineNumber]
                return properPassword    
            else:
                self.lineNumber+=1        
