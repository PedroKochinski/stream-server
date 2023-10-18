import socket
import Message
localIp = "127.0.0.1"
class Client:
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((localIp, self.port))
        self.message = Message.Message(sock=self.sock)
        
    def __str__(self):
        return str(self.__dict__)
    
    def sendMessage(self, message, address, port):
        self.message.sendMessage(message, address, self.port)
        
    def receiveMessage(self):
        self.message.receiveMessage(self.port)
        
    def close(self):
        self.sock.close()

def main():
    #create a client object
    client = Client(20001)

    #send a message to the server
    print("sending message...")
    client.sendMessage(["Hello, world!"], localIp, 20001)

if __name__ == "__main__":
    main()