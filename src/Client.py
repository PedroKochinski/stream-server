import socket
from Message import Message
from pydub import AudioSegment
from pydub.playback import play
import io
import threading
from queue import Queue
import logging
import sys

# Configurar o logger
logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

serverPort = 0
serverIP = ""

class Client:
    def __init__(self, port):
        # Initialize the client with necessary attributes
        self.serverPort = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(10)
        self.message = Message(sock=self.sock)
        self.sendMsgId = 1  # Message ID
        self.expectedMsgId = 0 # Expected message ID
        self.receivedMsgQte = 0  # Count of received messages
        self.outOfOrderMsgCounter = 0  # Count of out of order messages
        self.lostMsgCounter = 0  # Count of lost messages
        self.audioBuffer = Queue()
        self.bufferThreshold = 5
        self.state = 0  # State 0: Active, 1: Finished

    def sendMessage(self, message, code, id):
        self.sendMsgId += 1

        # Create a message dictionary
        msgDict = {
            "message": message,
            "code": code,
            "id": id
        }

        # Send a message to the specified address and port
        self.message.sendMessage(msgDict, serverIP, serverPort)

    def playBuffer(self):
        # Play audio from the buffer while the client is active or the buffer is not empty
        while self.state == 0 or not self.audioBuffer.empty():
            if not self.audioBuffer.empty():
                full_audio = AudioSegment.empty() # Create an empty audio segment
                while not self.audioBuffer.empty():
                    full_audio += self.audioBuffer.get() # Get all segments from the buffer and concatenate them
                play(full_audio) # Play the full audio segment

    def receiveAudioThread(self):
        audioSegments = []
        data = {}
        while True:
            if self.state == 1:
                # If the client is finished, break the loop
                break
            
            try:
                # Receive a message
                tmp = self.message.receiveMessage(self.serverPort)
                if (tmp != None):
                    data, _, _ = tmp

            except socket.timeout:
                # Log timeout
                logging.warning("Connection timed out")
                pass

            except socket.error as e:
                # Log socket error message
                logging.exception("Scoket Exception: Error while receiving message - %s", e)
            
            if data != {}:
                code, id, msg = data["code"], data["id"], data["message"]
                
                # Log received message ID
                logging.info("Received MSG %s", id)

                # Connection established
                if code == 2:
                    self.expectedMsgId = id + 1
                    logging.info("Connected")
                # Connection refused, server is at full capacity right now, should I try again?
                elif code == 3:
                    self.state = 1
                    logging.error("Error while connecting. Server is at full capacity, try again later")
                    break
                # End of transmission
                elif code == 4:
                    logging.info("End of transmission")
                    self.receivedMsgQte += 1
                    self.state = 1
                # Data message
                elif code == 6:
                    # Received in order
                    if id == self.expectedMsgId:
                        self.receivedMsgQte += 1
                        self.expectedMsgId += 1
                    # Received out of order (late)
                    elif id < self.expectedMsgId:
                        logging.warning("Received out of order (late) with ID = %s", id)
                        self.outOfOrderMsgCounter += 1
                        self.receivedMsgQte += 1
                    # Lost or out of order  
                    else:
                        logging.warning("Lost or out of order with ID = %s. Expected = %s", id, self.expectedMsgId)
                        self.lostMsgCounter += id - self.expectedMsgId
                        self.outOfOrderMsgCounter += 1
                        self.lostMsgCounter += 1
                        self.expectedMsgId = id + 1

                    msg = data["message"]

                    try:
                        # Convert the message to an audio segment and put it in the buffer
                        audioSegment = AudioSegment.from_mp3(io.BytesIO(msg))
                        audioSegments.append(audioSegment)
                    except IndexError:
                        logging.exception("Exception: No audio data found in the message.")

                    # If the buffer is full, put all segments in the buffer 
                    if len(audioSegments) >= self.bufferThreshold:
                        for segment in audioSegments:
                            self.audioBuffer.put(segment)
                        audioSegments = []
                

    def playAudioThread(self):
        # Start playing audio from the buffer
        self.playBuffer()

    def startThreads(self):
        # Create and start receive audio and play audio threads
        receiveAudioThread = threading.Thread(target=self.receiveAudioThread)
        playAudioThread = threading.Thread(target=self.playAudioThread)
        receiveAudioThread.start()
        playAudioThread.start()
        receiveAudioThread.join()
        playAudioThread.join()

    def close(self):
        # Close the client socket
        
        self.sendMessage("Request to disconnect", 4, 1)
        self.sock.close()

def main():
    global serverPort, serverIP
    if len(sys.argv) == 3:
        serverPort = int(sys.argv[1])
        serverIP = sys.argv[2]

        client = Client(serverPort)

        print("Sending message...")
        client.sendMessage("Request to connect", 1, client.sendMsgId)
        client.startThreads()
        
        total_messages = client.expectedMsgId  # Total messages expected (including out-of-order)
        received_percentage = (client.receivedMsgQte / total_messages) * 100
        lost_percentage = (client.lostMsgCounter / total_messages) * 100
        out_of_order_percentage = (client.outOfOrderMsgCounter / total_messages) * 100

        print("Received:", client.receivedMsgQte, "messages")
        print("Lost:", client.lostMsgCounter, "messages")
        print("Out of order:", client.outOfOrderMsgCounter, "messages")
        print("Total Messages:", total_messages)
        print("Percentage of Received Messages: {:.2f}%".format(received_percentage))
        print("Percentage of Lost Messages: {:.2f}%".format(lost_percentage))
        print("Percentage of Out of Order Messages: {:.2f}%".format(out_of_order_percentage))
        print("Finished")

        logging.info("=========================================================")
        logging.info("Total messages received: %s", client.receivedMsgQte)
        logging.info("Total messages lost: %s", client.lostMsgCounter)
        logging.info("Total messages out of order: %s", client.outOfOrderMsgCounter)
        logging.info("Percentage of Received Messages: {:.2f}%".format(received_percentage))
        logging.info("Percentage of Lost Messages: {:.2f}%".format(lost_percentage))
        logging.info("Percentage of Out of Order Messages: {:.2f}%".format(out_of_order_percentage))
        logging.info("=========================================================")


        client.close()
    else:
        print("Usage: python3 Client.py <port> <serverIP>")

if __name__ == "__main__":
    main()
