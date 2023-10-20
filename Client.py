import cv2
import socket
import zlib
import numpy as np
import Message

serverIP = "127.0.0.1"
serverPort = 4501
class Client:
    def __init__(self, port):
        self._serverPort = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._message = Message.Message(sock=self._sock)
        
    def __str__(self):
        return str(self.___dict__)
    
    def getServerPort(self):
        return self._serverPort
    
    def getIp(self):
        return self._ip
    
    def getSocket(self):
        return self._sock
    
    def getMessage(self):
        return self._message
    
    def setServerPort(self, serverPort):
        self._serverPort = serverPort
    
    def setIp(self, ip):
        self._ip = ip

    def setSocket(self, sock):
        self._sock = sock

    def setMessage(self, message):
        self._message = message
    
    def sendMessage(self, message, address, port):
        self._message.sendMessage(message, address, port)
        
    def receiveMessage(self):
        frame_buffer = b""
        while True:
            frame_data, _, _ = self._message.receiveByteMessage(self._serverPort)
            frame_data = zlib.decompress(frame_data)
            frame_buffer += frame_data
            print("receiving")
            if len(frame_data) < 65507:
                if len(frame_buffer) > 0:
                    frame = np.frombuffer(frame_buffer, dtype=np.uint8)
                    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                    print(frame)
                    if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
                        cv2.imshow('Streaming de Vídeo', frame)

                    frame_buffer = b""  # Clear the buffer

            if cv2.waitKey(10) & 0xFF == 27:  # Press Esc to exit
                break
    
    def close(self):
        self._sock.close()

def main():
    #create a client object
    client = Client(serverPort)

    msgDict = {
        "message": "Request to connect",
        "code": 1,
        "id": 1
    }

    # Configurar uma janela OpenCV para exibir o vídeo
    cv2.namedWindow('Client Video', cv2.WINDOW_NORMAL)

    #send a message to the server
    print("sending message...")
    client.sendMessage(msgDict, serverIP, serverPort)
    print("waiting for response...")
    client.receiveMessage()



if __name__ == "__main__":
    main()