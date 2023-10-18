import socket
import ast

class Message:
    def __init__(self, msg="", sock=None):
        self.msg = ""
        self.sock = sock #socket object

    def __str__(self):
        return str(self.__dict__)
    
    def sendMessage(self, message, address, port):
        try:
            # Send the message
            str_message = str(message)
            self.sock.sendto(str_message.encode(), (address, port))
        except socket.error as e:
            print("Error while sending message:", e)

    def receiveMessage(self, port):
        try:
            # Receive messages continuously
            while True:
                data, addr = self.sock.recvfrom(2048)  # buffer size is 2048 bytes
                res = ast.literal_eval(data.decode())
                print(res)
                return res
        except socket.error as e:
            print("Error while receiving message:", e)

    
