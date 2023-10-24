import Message
import socket
import time
import struct


serverPort = 4501
serverIP = "10.254.224.66"
class Server:
    def __init__(self, port):
        self._port = port
        self._ip = socket.gethostbyname(socket.gethostname())
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(0.1)
        self._sock.bind((serverIP, self._port))
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
                "code": 2,
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
        
        except Exception:
            print("Error receiving message")
            
    def sendMessageToAll(self, message):
        for i in range(len(self._addressList)):
            msgDict = {
                "message": message,
                "code": 2,
                "id": 1
            }
            
            self._message.sendMessage(msgDict, self._addressList[i], self._portList[i])

    def close(self):
        self._sock.close()
    
def main():
    BUFFER_SIZE = 65507  # Tamanho máximo do pacote UDP

    # Create a server object
    server = Server(serverPort)

    print(f"UDP Streaming Server in {server.getIp()}:{server.getPort()}")
    
    print("listening....")

    while True:
        server.receiveMessage()
        if(len(server.getAddressList())):
            break
    
    with open('shrekScript.txt', "rb") as f:
        while True:
            contents = f.read(2048)
            if len(contents)<=0:
                break
            server.receiveMessage()
            print("sending")
            server.sendMessageToAll(contents)
    

        
if __name__ == "__main__":
    main()
    
