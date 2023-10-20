import socket
import ast

"""
message codes:
1 - request to connect
2 - request to disconnect
3 - request to receive data
"""


class Message:
    def __init__(self, msg="", sock=None):
        self._msg = ""
        self._id = 0
        self._code = 0
        self._sock = sock #socket object

    def __str__(self):
        return str(self.__dict__)
    
    def setMsg(self, msg):
        self._msg = msg
    
    def getMsg(self):
        return self._msg
    
    def setId(self, id):
        self._id = id
    
    def getId(self):
        return self._id
    
    def setCode(self, code):
        self._code = code
    
    def getCode(self):
        return self._code

    def sendMessage(self, message, address, port):
        try:
            # Send the message
            str_message = str(message)
            self._sock.sendto(str_message.encode(), (address, port))
        except socket.error as e:
            print("Error while sending message:", e)

    def receiveMessage(self, port):
        try:
            # Receive messages continuously
            while True:
                data, (recvAddr, recvPort) = self._sock.recvfrom(2048)  # buffer size is 2048 bytes
                res = ast.literal_eval(data.decode())
                return res, recvAddr, recvPort

        except socket.error as e:
            print("Error while receiving message:", e)

    
