import socket
from Message import Message
from pydub import AudioSegment
from pydub.playback import play
import io
import threading
from queue import Queue

# Input the server's IP address and set the server port
serverIP = input("Enter the server's IP: ")
serverPort = 4501

class Client:
    def __init__(self, port):
        # Initialize the client with necessary attributes
        self.serverPort = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(10)
        self.message = Message(sock=self.sock)
        self.expectedMsgId = 0 # Expected message ID
        self.receivedMsgQte = 0  # Count of received messages
        self.lostMsgCounter = 0  # Count of lost messages
        self.audio_buffer = Queue()
        self.buffer_threshold = 5
        self.state = 0  # State 0: Active, 1: Finished

    def sendMessage(self, message, address, port):
        # Send a message to the specified address and port
        self.message.sendMessage(message, address, port)

    def playBuffer(self):
        # Play audio from the buffer while the client is active or the buffer is not empty
        while self.state == 0 or not self.audio_buffer.empty():
            if not self.audio_buffer.empty():
                full_audio = AudioSegment.empty() # Create an empty audio segment
                while not self.audio_buffer.empty():
                    full_audio += self.audio_buffer.get() # Get all segments from the buffer and concatenate them
                play(full_audio) # Play the full audio segment

    def receiveAudioThread(self):
        try:
            data, _, _ = self.message.receiveMessage(self.serverPort)
            audioSegments = []

            while True:
                code, id, msg = data["code"], data["id"], data["message"]

                if code == 1:
                    # Connection established
                    self.expectedMsgId = id + 1
                    print("Connected")
                elif code == 3:
                    # End of transmission
                    print("End of transmission")
                    self.receivedMsgQte += 1
                    self.state = 1
                elif code == 2:
                    if id == self.expectedMsgId:
                        # Received in order
                        self.receivedMsgQte += 1
                        self.expectedMsgId += 1
                    elif id < self.expectedMsgId:
                        # Received out of order (late)
                        print("Received out of order (late) with ID =", id)
                        self.lostMsgCounter += 1
                    else:
                        # Lost or out of order
                        print("Lost or out of order with ID =", id, " Expected =", self.expectedMsgId)
                        self.lostMsgCounter += id - self.expectedMsgId
                        self.lostMsgCounter += 1
                        self.expectedMsgId = id + 1

                    msg = data["message"]
                    try:
                        audioSegment = AudioSegment.from_mp3(io.BytesIO(msg))
                        audioSegments.append(audioSegment)
                    except IndexError:
                        print("Error: No audio data found in the message.")

                    if len(audioSegments) >= self.buffer_threshold:
                        for segment in audioSegments:
                            self.audio_buffer.put(segment)
                        audioSegments = []
                    elif len(audioSegments) == 0:
                        # Pre-buffer a few segments when the buffer is empty
                        data, _, _ = self.message.receiveMessage(self.serverPort)
                        continue

                data, _, _ = self.message.receiveMessage(self.serverPort)

        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            self.state = 1
            self.close()
            exit(1)
        except TypeError:
            print("Type error")

        
        

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
        msgDict = {
            "message": "Request to disconnect",
            "code": 4,
            "id": 1
        }
        self.sendMessage(msgDict, serverIP, serverPort)
        self.sock.close()

def main():
    client = Client(serverPort)

    msgDict = {
        "message": "Request to connect",
        "code": 1,
        "id": 1
    }

    print("Sending message...")
    client.sendMessage(msgDict, serverIP, serverPort)
    client.startThreads()
    print("Received", client.receivedMsgQte, "messages")
    print("Lost", client.lostMsgCounter, "messages")
    print("Out of order", client.lostMsgCounter, "messages")
    print("Finished")
    client.close()

if __name__ == "__main__":
    main()
