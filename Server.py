import Message
import socket
from pydub import AudioSegment
from random import randint

serverPort = 4501


class Server:
    def __init__(self, port):
        rate = input("Intervalo de tempo (em segundos): ")
        self._port = port
        self._ip = socket.gethostbyname(socket.gethostname())
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(float(rate))
        self._sock.bind((self._ip, self._port))
        self._message = Message.Message(sock=self._sock)
        self._addressList = []
        self._portList = []
        self.msgId = 0
    
    def __str__(self):
        return str(self.___dict__)
    
    def getPort(self):
        return self._port
    
    def getIp(self):
        return self._ip
    
    def sendMessage(self, message, address, port):
        self._message.sendMessage(message, address, port)
        
    def getAddressList(self):
        return self._addressList

    def receiveMessage(self):
        try:
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
                "message": b"Accepting connection",
                "code": 1,
                "id": self.msgId
            }
            
            if recvAddr not in self._addressList and msgCode == 1:
                self._addressList.append(recvAddr)
                self._portList.append(recvPort)
                print("Address list:", self._addressList)
                print("Port list:", self._portList)
            else:
                print("Address already in list.")
            self._message.sendMessage(msgDict, recvAddr, recvPort)
        
        except TypeError:
            print("Type Error")
            
    def sendMessageToAll(self, message, code=2):
        for i in range(len(self._addressList)):
            msgDict = {
                "message": message,
                "code": code,
                "id": self.msgId
            }
            print("sending with ID =", self.msgId)
            self._message.sendMessage(msgDict, self._addressList[i], self._portList[i])

    def close(self):
        self._sock.close()
    
def main():
    # Create a server object
    server = Server(serverPort)

    print(f"UDP Streaming Server in {server.getIp()}:{server.getPort()}")
    
    print("listening....")

    while True:
        server.receiveMessage() # fica escutando ate algum host conectar
        if(len(server.getAddressList())):
            break
    from pydub import AudioSegment
    with open('brasil.mp3', "rb") as audio_file:
        while True:
            audio_data = audio_file.read(34000)  # Lê 1024 bytes do arquivo MP3
            print(len(audio_data))
            if len(audio_data) <= 0:  # Verifica se acabou o arquivo
                break
            server.msgId += 1
            server.receiveMessage()  # Escuta até dar timeout
            number = randint(0, 100)
            # if number >= 20:
            server.sendMessageToAll(audio_data, 2)  # Envia o conteúdo para todos os hosts da lista

    audio_file.close()
    server.sendMessageToAll("End of transmission", 3, server.msgId+1) # indica para todos os hosts da lista que a transmissao acabou
    print("Total messages sent: ", server.msgId+1)
    server.close()
        
if __name__ == "__main__":
    main()
    