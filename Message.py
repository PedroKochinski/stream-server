import socket
import pickle

"""
message codes:
1 - request to connect / accept connection
2 - data message
3 - end of transmission
"""


class Message:
    def __init__(self, sock=None):
        self.sock = sock #socket object

    def __str__(self):
        return str(self._dict__)

    def sendMessage(self, message, address, port):
        try:
            # Send the message
            self.sock.sendto(pickle.dumps(message), (address, port))
        except socket.error as e:
            print("Error while sending message:", e)

    def receiveMessage(self, port):
        try:
            while True:
                data, (recvAddr, recvPort) = self.sock.recvfrom(65535)  # buffer size is 65535 bytes, max UDP segment size
                res = pickle.loads(data)
                print(len(res["message"]))
                return res, recvAddr, recvPort
        except socket.timeout:
            print("Timed Out")

        except socket.error as e:
            print("Error while receiving message:", e)

    
