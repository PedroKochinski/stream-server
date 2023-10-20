import socket
import Message

localIp = "127.0.0.1"

class Client:
    def __init__(self, port):
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.connect((localIp, self._port))
        self._message = Message.Message(sock=self._sock)
        
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
            recvMsg, _ , _ = self._message.receiveMessage(self._port)
            print(recvMsg)
    
    def close(self):
        self._sock.close()

def main():
    #create a client object
    client = Client(20001)

    #create a message
    msg = client.getMessage()

    msgDict = {
        "message": "Request to connect",
        "code": 1,
        "id": 1
    }
    #send a message to the server
    print("sending message...")
    client.sendMessage(msgDict, localIp, 20001)
    print("waiting for response...")
    client.receiveMessage()

if __name__ == "__main__":
    main()