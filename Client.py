import socket
import numpy as np
import Message

serverIP = "10.254.224.66"
serverPort = 4501

class Client:
    def __init__(self, port):
        self._serverPort = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(0.1)
        self._message = Message.Message(sock=self._sock)
        
    def __str__(self):
        return str(self.___dict__)
    
    def sendMessage(self, message, address, port):
        self._message.sendMessage(message, address, port)
        
    def receiveMessage(self):
            
            with open('writeFile.txt', 'wb') as f:
                while True:
                    try:
                        print("receiving")
                        data, _, _ = self._message.receiveMessage(self._serverPort)
                        msg = data["message"]
                        print(len(msg))
                        f.write(msg)
                    except Exception:
                        print("Error receiving message")
            f.close()
    
    def close(self):
        self._sock.close()

def main():

    client = Client(serverPort)

    msgDict = {
        "message": "Request to connect",
        "code": 1,
        "id": 1
    }

    #send a message to the server
    print("sending message...")
    client.sendMessage(msgDict, serverIP, serverPort)
    print("waiting for response...")
    client.receiveMessage()

if __name__ == "__main__":
    main()