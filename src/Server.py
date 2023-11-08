import Message
import socket
import threading
import time
import logging
import sys

# create logger
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a Server class to handle audio transmission
class Server:
    def __init__(self, port):
        self.rate = 1  # Set the time interval for audio transmission
        self.port = port
        self.ip = socket.gethostbyname(socket.gethostname()) # Get the IP address of the host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.sock.settimeout(5)
        self.message = Message.Message(sock=self.sock)  # Initialize the Message instance for communication
        self.addressList = []  # List to store client addresses
        self.portList = []  # List to store client ports
        self.msgId = 0  # Message ID
        self.state = 0  # State 0: Active, 1: Finished
        self.maxClientSize = 3 # Maximum clients connected at the same time

    def sendMessage(self, message, address, port):
        # Send a message to a specific address and port
        self.message.sendMessage(message, address, port)

    def receiveMessage(self):
        tmp = self.message.receiveMessage(self.port)  # Receive a message
        if(tmp != None):
            recvMsg, recvAddr, recvPort = tmp  # Extract received message, address, and port
            
            msg, code = recvMsg["message"], recvMsg["code"]  # Extract message and code from the received message

            # Log messages
            logging.info("Message received from address: %s", recvAddr)
            logging.info("Port: %s", recvPort)
            logging.info("Message: %s", msg)
            logging.info("Code: %s", code)

            msgDict = {}

            if code == 1: # Request to connect
                if recvAddr not in self.addressList:
                    if len(self.addressList) < self.maxClientSize:
                        msgDict = {
                            "message": b"Accepting connection",
                            "code": 2, # Accept connection code
                            "id": self.msgId
                        }
                        # If the address is not in the list
                        self.addressList.append(recvAddr)  # Add the sender's address to the list
                        self.portList.append(recvPort)  # Add the sender's port to the list
                        
                        # Log messages
                        logging.info("Address list: %s", self.addressList)
                        logging.info("Port list: %s", self.portList)
                        
                    else:
                        msgDict = {
                            "message": b"Rejecting connection, server at full capacity",
                            "code": 3, # Reject connection code
                            "id": self.msgId
                        }
                        
                        # Log message
                        logging.info("Rejecting connection from %s, server at full capacity", recvAddr)
                else:
                    # Log message
                    logging.info("Address already in the list.")

                # Log message
                logging.info("Sending a response with ID = %s", self.msgId)
                
                self.message.sendMessage(msgDict, recvAddr, recvPort)  # Send an acknowledgment message to the sender
                
            elif code == 4: # Request to disconnect
                if recvAddr in self.addressList:
                    # If the address is in the list remove it from the list
                    self.addressList.remove(recvAddr)  # Remove the sender's address from the list
                    self.portList.remove(recvPort)  # Remove the sender's port from the list
                    
                    # Log messages
                    logging.info("Address list: %s", self.addressList)
                    logging.info("Port list: %s", self.portList)
                    
                else:
                    # Log message
                    logging.info("Address is not in the list.")

                
    def sendMessageToAll(self, message, code):
        self.msgId += 1  # Increment the message ID
        
        # Log message
        logging.info("Sending to all clients a message with ID = %s", self.msgId)
        
        for i in range(len(self.addressList)):
            msgDict = {
                "message": message,
                "code": code,
                "id": self.msgId
            }
            self.message.sendMessage(msgDict, self.addressList[i], self.portList[i])  # Send the message to all clients

    def close(self):
        self.sock.close()  # Close the server socket

    def receiveMsgThread(self):
        while True:
            try:
                self.receiveMessage()  # Receive and handle incoming messages
                if self.state == 1:
                    logging.info("Finished")  # Server has finished its job
                    break
            except socket.timeout:
                pass

            except socket.error as e:
                # Log error message
                logging.error("Error while receiving message: %s", e)
            
            finally:            
                if self.state == 1:
                    logging.info("Finished")  # Server has finished its job
                    break

    def sendMsgThread(self):
            print("Waiting for clients to connect...")
            
            while True:

                if len(self.addressList) > 0:
                    streamFileName = input("Enter the name of the file to be streamed: ")
                    self.rate = float(input("Enter the rate of transmission (in seconds): "))
                    try:
                        with open(streamFileName, "rb") as audioFile:
                            print("Sending audio data...")
                            while True:
                                audioData = audioFile.read(30000) # Read 30000 bytes of audio data
                                # Log message
                                logging.info("Audio data length: %s", len(audioData))
                                time.sleep(self.rate) # Sleep for the specified rate
                                if len(audioData) <= 0: # If there is no more audio data, break the loop
                                    break
                                self.sendMessageToAll(audioData, 6)  # Send audio data to all clients
                        audioFile.close() # Close the audio file
                        logging.info("No more transmission")
                        self.state = 1  # Update server state to indicate it has finished
                        break
                    except FileNotFoundError:
                        # Log error message
                        logging.exception("File not found")
                        print("File not found. Try again? (y/n)")
                        choice = input()
                        if choice == "y":
                            continue
                        else:
                            self.state = 1
                            break

                    except socket.error as e:
                        # Log error message
                        logging.exception("Scoket Exception: Error while sending message - %s", e)


    def startThreads(self):
        # Create and start the receive audio thread and the send audio thread
        receiveMsgThread = threading.Thread(target=self.receiveMsgThread)
        sendMsgThread = threading.Thread(target=self.sendMsgThread)

        receiveMsgThread.start()
        sendMsgThread.start()
        
        receiveMsgThread.join()
        sendMsgThread.join()

def main():
    if len(sys.argv) == 2:
        serverPort = int(sys.argv[1])
        server = Server(serverPort)

        logging.info("UDP Streaming Server in %s:%s", server.ip, server.port)

        server.startThreads()  # Start the server's main threads for receiving and sending audio

        server.sendMessageToAll("End of transmission", 4)  # Send a message indicating the end of transmission
        logging.info("Total messages sent: %s", server.msgId)  # Log the total number of messages sent
        print("Closing server...")
        server.close()  # Close the server
    else:
        print("Usage: python3 Server.py <port>")

if __name__ == "__main__":
    main()
