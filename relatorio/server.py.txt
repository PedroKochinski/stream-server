import Message
import socket
import time
import struct
from random import randint

serverPort = 4501


class Server:
    def __init__(self, port):
        rate = input("Intervalo de tempo (em segundos): ")
        self._port = port
        self._ip = socket.gethostbyname(socket.gethostname())
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(float(rate))
        self._sock.bind((self._ip, self._port))
        self._message = Message.Message(sock=self._sock)
        self._addressList = []
        self._portList = []
    
    def __str__(self):
        return str(self.___dict__)
    
    def getPort(self):
        return self._port
    
    def getIp(self):
        return self._ip
    
    def sendMessage(self, message, address, port):
        self._message.sendMessage(message, address, port)
        
    def getAddressList(self):
        return self._addressList

    def receiveMessage(self):
        try:
            recvMsg, recvAddr, recvPort = self._message.receiveMessage(self._port)
            
            msg = recvMsg['message']
            msgCode = recvMsg['code']

            print()
            print("Message received from address:", recvAddr)
            print("Port:", recvPort)
            print("Message:", msg)
            print("Code:", msgCode)

            print()

            msgDict = {
                "message": b"Accepting connection",
                "code": 1,
                "id": 1
            }
            
            if recvAddr not in self._addressList and msgCode == 1:
                self._addressList.append(recvAddr)
                self._portList.append(recvPort)
                print("Address list:", self._addressList)
                print("Port list:", self._portList)
            else:
                print("Address already in list.")
            self._message.sendMessage(msgDict, recvAddr, recvPort)
        
        except TypeError:
            print("Type Error")
            
    def sendMessageToAll(self, message, code=2, msgId=1):
        for i in range(len(self._addressList)):
            msgDict = {
                "message": message,
                "code": code,
                "id": msgId
            }
            
            self._message.sendMessage(msgDict, self._addressList[i], self._portList[i])

    def close(self):
        self._sock.close()
    
def main():
    # Create a server object
    server = Server(serverPort)

    print(f"UDP Streaming Server in {server.getIp()}:{server.getPort()}")
    
    print("listening....")

    while True:
        server.receiveMessage() # fica escutando ate algum host conectar
        if(len(server.getAddressList())):
            break
    i = 0
    with open('shrekScript.txt', "rb") as f:
        while True:
            contents = f.read(2048) # le 2048 bytes do arquivo
            if len(contents)<=0: # verifica se acabou o arquivo
                break
            i+=1
            server.receiveMessage() # escuta até dar timeout
            print("sending with ID = ", i)
            number = randint(0, 100)
            if(number >= 20):
                server.sendMessageToAll(contents, 2, i) # envia o conteudo para todos os hosts da lista
    server.sendMessageToAll("End of transmission", 3, i+1) # indica para todos os hosts da lista que a transmissao acabou
    print("Total messages sent: ", i+1)
    server.close()
        
if __name__ == "__main__":
    main()
    