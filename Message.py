import socket
import ast
import pickle

"""
message codes:
1 - request to connect
2 - request to disconnect
3 - request to receive data
"""


class Message:
    def __init__(self, sock=None):
        self._sock = sock #socket object

    def __str__(self):
        return str(self.__dict__)

    def sendMessage(self, message, address, port):
        try:
            # Send the message
            self._sock.sendto(pickle.dumps(message), (address, port))
        except socket.error as e:
            print("Error while sending message:", e)

    def receiveMessage(self, port):
        try:
            while True:
                data, (recvAddr, recvPort) = self._sock.recvfrom(35000)  # buffer size is 2048 bytes
                res = pickle.loads(data)
                print(len(res["message"]))
                return res, recvAddr, recvPort
        except socket.timeout:
            print("Timed Out")

        except socket.error as e:
            print("Error while receiving message:", e)

    
