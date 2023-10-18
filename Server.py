import Message
import socket

localIP = "127.0.0.1"
localPort = 20001

class Server:
    def __init__(self, port):
        self.port = localPort
        self.ip = socket.gethostbyname(socket.gethostname())
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((localIP, self.port))
        self.message = Message.Message(sock=self.sock)
        
    def __str__(self):
        return str(self.__dict__)
    
    def sendMessage(self, message, address, port):
        self.message.sendMessage(message, address, port)
        
    def receiveMessage(self):
        self.message.receiveMessage(self.port)
        
    def close(self):
        self.sock.close()
    
def main():
    #create a server object
    server = Server(2001)
    print("listening....")
    server.receiveMessage()

if __name__ == "__main__":
    main()
    
