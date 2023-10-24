import socket
import Message

serverIP = "10.254.224.52"
serverPort = 4501
name = input("Enter the file name: ")

class Client:
    def __init__(self, port):
        self._serverPort = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(2)
        self._message = Message.Message(sock=self._sock)
        self._expectedMsgId = 1
        self._receivedMsgQte = 0
        self._lostMsgQte = 0
        self._outOfOrderMsgQte = 0
        
    def sendMessage(self, message, address, port):
        self._message.sendMessage(message, address, port)
        
    def receiveMessage(self):
        data, _, _ = self._message.receiveMessage(self._serverPort)
        
        with open(name + '.txt', 'wb') as f:
            while True:
                if data["code"] == 3:  # verifica se a transmissão acabou
                    print("End of transmission")
                    break
                
                elif data["code"] == 2:  # verifica se são dados
                    if data["id"] == self._expectedMsgId:
                        # Recebeu na ordem
                        print("Received in order")
                        self._receivedMsgQte += 1
                        self._expectedMsgId += 1
                    elif data["id"] < self._expectedMsgId:
                        # Chegou atrasado
                        print("Received out of order (late)")
                        self._lostMsgQte += 1
                    else:
                        # Perdeu ou chegou fora de ordem
                        print("Lost or out of order")
                        self._lostMsgQte += data["id"] - self._expectedMsgId
                        self._outOfOrderMsgQte += 1
                        self._expectedMsgId = data["id"] + 1
                    
                    msg = data["message"]
                    f.write(msg)

                data, _, _ = self._message.receiveMessage(self._serverPort)
                
        f.close()
    
    def close(self):
        self._sock.close()

def main():

    client = Client(serverPort)

    msgDict = {
        "message": "Request to connect",
        "code": 1,
        "id": 1
    }

    print("Sending message...")
    client.sendMessage(msgDict, serverIP, serverPort)  # pede para conectar ao servidor
    
    client.receiveMessage()  # recebe os dados do servidor
    print("Received Messages: ", client._receivedMsgQte)
    print("Lost Messages: ", client._lostMsgQte)
    print("Out of Order Messages: ", client._outOfOrderMsgQte)
    client.close()

if __name__ == "__main__":
    main()
