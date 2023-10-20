import Message
import cv2
import socket
import zlib
import struct


serverPort = 4501
serverIP = "127.0.0.1"
class Server:
    def __init__(self, port):
        self._port = port
        self._ip = socket.gethostbyname(socket.gethostname())
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((serverIP, self._port))
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
        
        if recvAddr not in self._addressList and msgCode == 1:
            self._addressList.append(recvAddr)
            self._portList.append(recvPort)
            print("Address list:", self._addressList)
            print("Port list:", self._portList)
        else:
            print("Address already in list.")
        
        
        self._message.sendMessage(msgDict, recvAddr, recvPort)

    def sendMessageToAll(self, message):
        for i in range(len(self._addressList)):
            # Divide os dados em pacotes menores
            self._message.sendMessage(message, self._addressList[i], self._portList[i])

    def close(self):
        self._sock.close()
    
def main():
    BUFFER_SIZE = 65507  # Tamanho máximo do pacote UDP

    # Create a server object
    server = Server(serverPort)

    # Start video capture
    cap = cv2.VideoCapture('video.mp4')

    print(f"UDP Streaming Server in {server.getIp()}:{server.getPort()}")
    print("listening....")
    server.receiveMessage()

    cv2.namedWindow('Server Video', cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Show the frame on the server side
        cv2.imshow('Server Video', frame)
        cv2.waitKey(30)  # Display the frame and wait for a short time (1 ms) to refresh the window

        # Compact and serialize the frame
        frame_bytes = zlib.compress(frame.tobytes())

        # Divide the data into smaller packets and send the frame over UDP
        for i in range(0, len(frame_bytes), BUFFER_SIZE):
            print("sending message...")
            server.sendMessageToAll(frame_bytes[i:i + BUFFER_SIZE])

if __name__ == "__main__":
    main()
    
