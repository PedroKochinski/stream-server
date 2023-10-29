import Message
import socket
import threading
import time
from random import randint

serverPort = 4501

# Create a Server class to handle audio transmission
class Server:
    def __init__(self, port):
        self.bitRate = float(input("Time interval (in seconds): "))
        self.port = port
        self.ip = socket.gethostbyname(socket.gethostname())
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.sock.settimeout(5)
        self.message = Message.Message(sock=self.sock)
        self.addressList = []
        self.portList = []
        self.msgId = 0
        self.state = 0

    def sendMessage(self, message, address, port):
        # Send a message to a specific address and port
        self.message.sendMessage(message, address, port)

    def receiveMessage(self):
        try:
            recvMsg, recvAddr, recvPort = self.message.receiveMessage(self.port)

            msg, code = recvMsg["message"], recvMsg["code"]

            print("Message received from address:", recvAddr)
            print("Port:", recvPort)
            print("Message:", msg)
            print("Code:", code)

            msgDict = {
                "message": b"Accepting connection",
                "code": 1,
                "id": self.msgId
            }

            if recvAddr not in self.addressList and code == 1:
                self.addressList.append(recvAddr)
                self.portList.append(recvPort)
                print("Address list:", self.addressList)
                print("Port list:", self.portList)
            else:
                print("Address already in the list.")
            self.message.sendMessage(msgDict, recvAddr, recvPort)

        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            self.state = 1
            self.sendMessageToAll("End of transmission", 3)
            print("Total messages sent: ", self.msgId)
            self.close()
            exit(1)

        except TypeError:
            print("Type Error")

    def sendMessageToAll(self, message, code):
        self.msgId += 1
        for i in range(len(self.addressList)):
            msgDict = {
                "message": message,
                "code": code,
                "id": self.msgId
            }
            print("Sending with ID =", self.msgId)
            self.message.sendMessage(msgDict, self.addressList[i], self.portList[i])

    def close(self):
        self.sock.close()

    def receiveMsgThread(self):
        while True:
            self.receiveMessage()
            if self.state == 1:
                print("Finished")
                break

    def sendMsgThread(self):
        while True:
            if len(self.addressList) > 0:
                with open('1minuto.mp3', "rb") as audioFile:
                    while True:
                        audioData = audioFile.read(30000)
                        print(len(audioData))
                        time.sleep(self.bitRate)
                        if len(audioData) <= 0:
                            break
                        # number = randint(0, 100) 
                        self.sendMessageToAll(audioData, 2)

                audioFile.close()
                print("No more transmission")
                self.state = 1
                break

    def startThreads(self):
        # Create and start the receive audio thread
        receiveMsgThread = threading.Thread(target=self.receiveMsgThread)
        sendMsgThread = threading.Thread(target=self.sendMsgThread)
        receiveMsgThread.start()
        sendMsgThread.start()
        receiveMsgThread.join()
        sendMsgThread.join()

def main():
    server = Server(serverPort)

    print(f"UDP Streaming Server in {server.ip}:{server.port}")
    
    server.startThreads()
    
    server.sendMessageToAll("End of transmission", 3)
    print("Total messages sent: ", server.msgId)
    server.close()

if __name__ == "__main__":
    main()
