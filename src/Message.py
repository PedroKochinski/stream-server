import pickle

"""
message codes:
1 - request to connect / accept connection
2 - data message
3 - end of transmission
4 - client disconnected from server
5 - server refused connection (max capacity)
6 - server refused connection (already has the address in address list)
"""


class Message:
    def __init__(self, sock=None):
        self.sock = sock #socket object

    def __str__(self):
        return str(self._dict__)

    def sendMessage(self, message, address, port):
        self.sock.sendto(pickle.dumps(message), (address, port))
        

    def receiveMessage(self, port):
        while True:
            data, (recvAddr, recvPort) = self.sock.recvfrom(65535)  # buffer size is 65535 bytes, max UDP segment size
            res = pickle.loads(data)
            print(len(res["message"]))
            return res, recvAddr, recvPort
        

    
