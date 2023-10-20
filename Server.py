import Message
import socket

localIP = "127.0.0.1"
localPort = 20001

class Server:
    def __init__(self, ip, port):
        self._port = localPort
        self._ip = socket.gethostbyname(socket.gethostname())
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((localIP, self._port))
        self._message = Message.Message(sock=self._sock)
        self._addressList = []
        self._portList = []
    
    def __str__(self):
        return str(self.___dict__)
    
    def getPort(self):
        return self._port
    
    def getIp(self):
        return self._ip
    
    def getSocket(self):
        return self._sock
    
    def getMessage(self):
        return self._message
    
    def setPort(self, port):
        self._port = port
    
    def setIp(self, ip):
        self._ip = ip

    def setSocket(self, sock):
        self._sock = sock

    def setMessage(self, message):
        self._message = message

    def sendMessage(self, message, address, port):
        self._message.sendMessage(message, address, port)
        
    def receiveMessage(self):
        while True:
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
                "message": "Accepting connection",
                "code": 2,
                "id": 1
            }
            
            if recvAddr not in self._addressList:
                self._addressList.append(recvAddr)
                self._portList.append(recvPort)
                print("Address list:", self._addressList)
                print("Port list:", self._portList)
            else:
                print("Address already in list.")
            
            while True:
               self._message.sendMessage(msgDict, recvAddr, recvPort)

    def close(self):
        self._sock.close()
    
def main():
    #create a server object
    server = Server(localIP, localPort)
    print("listening....")
    server.receiveMessage()

if __name__ == "__main__":
    main()
    
