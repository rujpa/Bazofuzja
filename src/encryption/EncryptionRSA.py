from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
from os.path  import exists
import src.encryption

class EncryptionRSA ():

    def __init__(self):
        self.myPath = os.path.dirname(src.encryption.__file__)    

        if(exists(self.myPath + "\\priv_key.pem")):
            pass
        else:
            if(exists(self.myPath +"\\passwords.bin")):
                os.remove(self.myPath + "\\passwords.bin")
            if(exists(self.myPath + "\\logins.txt")):
                os.remove(self.myPath + "\\logins.txt")
            self.generate()
            self.exportPrivKey()

        self.setPrivKey()
        
    password = ""
    decrypted = ""
    privKey = u''
    
    def generate(self):
        self.keyPair = RSA.generate(1024)
        return self.keyPair

    def setPrivKey(self):
        file = open(self.myPath + "\\priv_key.pem", "rb")
        self.privKey = RSA.importKey(file.read())
        file.close()


    def encrypt(self):
        pubKeyPEM = self.privKey.publickey()
        encryptor = PKCS1_OAEP.new(pubKeyPEM)

        self.decrypted = self.decrypted + "\n" + self.password

        binFile = bytes(self.decrypted, 'ascii')
        encrypted = encryptor.encrypt(binFile)       
        
        file = open(self.myPath + "\\passwords.bin", "wb")
        file.write(encrypted)
        file.close()

    def encryptPassword(self, password):
        binPassword = bytes(password, 'ascii')
        pubKeyPEM = self.privKey.publickey()
        encryptor = PKCS1_OAEP.new(pubKeyPEM)
        encrypted = encryptor.encrypt(binPassword)
        encryptedSt = str(encrypted)              
        return encryptedSt

    def decrypt(self):
        decryptor = PKCS1_OAEP.new(self.privKey)

        file = open(self.myPath + "\\passwords.bin", "rb")
        content = file.read()
        self.decrypted = decryptor.decrypt(content).decode()

        if(self.decrypted[0] == "\n"):
            self.decrypted = self.decrypted[1:]

    def decryptPassword(self, password):
        decryptor = PKCS1_OAEP.new(self.privKey)
        binPassword = bytes(password, 'ascii')
        decrypted = decryptor.decrypt(binPassword).decode()
        return decrypted

    def exportPrivKey(self):
        file = open(self.myPath + "\\priv_key.pem", "wb")
        self.privKeyPEM = self.keyPair.exportKey()
        file.write(self.privKeyPEM)
        file.close()

    def addPassword(self, password):      
        self.password = password
        if(exists(self.myPath + "\\passwords.bin")):
            self.decrypt()
        self.encrypt()

    def readPasswords(self):
        self.decrypt()
        return self.decrypted