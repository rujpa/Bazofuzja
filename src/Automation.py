import os
import pickle
import importlib
from src.plugins.core import DatabaseConnection
from src.plugins.core import FileConnection
import src.plugins
import base64


class Automation:
    def __init__(self, Win):
        self.Win = Win
        self.src_data = {}
        self.dst_data = {}      
        self.operation = {}
        self.arg = {}
        
        self.Win.LoadPlugins()
        
    
    def setDatabases(self):
        DbIn = self.Win.getDbIn()
        DbOut = self.Win.getDbOut()
        
        self.src_data.update({"ifLoginNeeded":DbIn.getIfLoginNeeded()})
        self.src_data.update({"isFlatFile":self.Win.isFlatFile(DbIn)})
        self.src_data.update({"tech": self.Win.getTechIn()})
        self.dst_data.update({"ifLoginNeeded":DbOut.getIfLoginNeeded()})
        self.dst_data.update({"isFlatFile":self.Win.isFlatFile(DbOut)})
        self.dst_data.update({"tech": self.Win.getTechOut()})
        
        self.setLoginData(self.src_data,DbIn)
        self.setLoginData(self.dst_data,DbOut)
        
    def setLoginData(self,data,Db):
        if(data["ifLoginNeeded"] == True):
            data.update({"databaseAddress":Db.getHost()})
            data.update({"databaseUser":Db.getUser()})
            data.update({"password":Db.getPassword()})
            data.update({"databaseName":Db.getDatabase()})
            #self.encryption(data)
            
        else:
            data.update({"filepath":Db.getFilePath()})
            #data.update({"ui":Db.getUi()})
        
    def addOperation(self,newAcction,listOfArg):
        #print(newAcction)
        self.operation.update({len(self.operation):newAcction})
        self.arg.update({len(self.arg):listOfArg})
        

        
    def save(self):
        self.setDatabases()
        self.filename = self.src_data["tech"] + "-"+self.dst_data["tech"]
        self.filepath = os.environ["HOMEPATH"]+"//"+self.filename + ".bin"
        
        transfer_record = {"src": self.src_data, "dst": self.dst_data, "actions": self.operation, "arguments":self.arg}
        
        binary = pickle.dumps(transfer_record)
        binary = base64.b64encode(binary)
        
        out = open(self.filepath, "wb+")
        out.write(binary)
        out.close()
    
    def read(self,filepath):
        source = open(filepath, "rb")
        read_binary = source.read()
        source.close()
        
        read_binary = base64.b64decode(read_binary)
        read_binary = pickle.loads(read_binary)
        
        self.src_data = read_binary["src"]
        self.dst_data = read_binary["dst"]
        self.operation = read_binary["actions"]
        self.arg = read_binary["arguments"]  
       
        
        DbIn = self.createDatabase(self.src_data)
        DbOut = self.createDatabase(self.dst_data)
        
        DbIn.setIfLoginNeeded(self.src_data["ifLoginNeeded"])
        DbOut.setIfLoginNeeded(self.dst_data["ifLoginNeeded"])
        
        self.Win.setDbIn(DbIn)
        self.Win.setDbOut(DbOut)
        self.Win.setTechIn(self.src_data["tech"])
        self.Win.setTechOut(self.dst_data["tech"])
        
        for i in range(0,len(self.operation)):
            fun = getattr(self.Win, self.operation[i])
            l = len(self.arg[i])
            listOfArg = self.arg[i]
            if(l == 1):
                fun(listOfArg[0])
            elif(l==2):
                fun(listOfArg[0],listOfArg[1])
        
        
    def createDatabase(self,data):
    
        if(data["isFlatFile"] == False and data["ifLoginNeeded"] ):
                Db = self.Win.mod[data["tech"]](data["databaseAddress"],data["databaseUser"],data["password"],data["databaseName"])
        else:
            Db = self.Win.mod[data["tech"]](data["filepath"])

        return Db
        
