import socket
import Message
from pydub import AudioSegment
from pydub.playback import play
import io
import threading
from queue import Queue

serverIP = input("Digite o IP do servidor: ")
serverPort = 4501

class Client:
    def __init__(self, port):
        self._serverPort = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(5)
        self._message = Message.Message(sock=self._sock)
        self._expectedMsgId = 1
        self._receivedMsgQte = 0
        self._lostMsgQte = 0
        self._outOfOrderMsgQte = 0
        self.audio_buffer = Queue()  # Use a Queue for a non-blocking buffer
        self.buffer_threshold = 5  # Adjust the buffer threshold as needed
        self.state = 0

    def sendMessage(self, message, address, port):
        self._message.sendMessage(message, address, port)

    def play_buffer(self):
        while self.state == 0 or not self.audio_buffer.empty():
            if not self.audio_buffer.empty():
                full_audio = AudioSegment.empty()
                while not self.audio_buffer.empty():
                    full_audio += self.audio_buffer.get()
                play(full_audio)

    def receive_audio_thread(self):
        try:
            data, _, _ = self._message.receiveMessage(self._serverPort)
            audio_segments = []
            while True:
                if data["code"] == 1: # Check if the message was accepted
                    self._expectedMsgId = data["id"] + 1    
                    self._receivedMsgQte += 1                
                    print("Connected")
                
                elif data["code"] == 3:  # Check if the transmission has ended
                    print("End of transmission")
                    self._receivedMsgQte += 1                
                    self.state = 1  # Set the state to stop audio playback
                    break

                elif data["code"] == 2:  # Check if it's audio data
                    if data["id"] == self._expectedMsgId:
                        # Received in order
                        print("Received in order with ID =", data["id"])
                        self._receivedMsgQte += 1
                        self._expectedMsgId += 1
                    elif data["id"] < self._expectedMsgId:
                        # Received out of order (late)
                        print("Received out of order (late) with ID =", data["id"])
                        self._lostMsgQte += 1
                    else:
                        # Lost or out of order
                        print("Lost or out of order with ID =", data["id"], " Expected = ", self._expectedMsgId)
                        self._lostMsgQte += data["id"] - self._expectedMsgId
                        self._outOfOrderMsgQte += 1
                        self._expectedMsgId = data["id"] + 1
                    msg = data["message"]
                    try:
                        audio_segment = AudioSegment.from_mp3(io.BytesIO(msg))
                        audio_segments.append(audio_segment)
                    except IndexError:
                        print("Error: No audio data found in the message.")

                    if len(audio_segments) >= self.buffer_threshold:
                        for segment in audio_segments:
                            self.audio_buffer.put(segment)
                        audio_segments = []

                data, _, _ = self._message.receiveMessage(self._serverPort)

        except TypeError:
            print("Type error")

    def play_audio_thread(self):
        self.play_buffer()  # Start playing audio

    def start_threads(self):
        # Create and start the receive audio thread
        receive_audio_thread = threading.Thread(target=self.receive_audio_thread)
        receive_audio_thread.start()

        # Create and start the play audio thread
        play_audio_thread = threading.Thread(target=self.play_audio_thread)
        play_audio_thread.start()

        # Wait for both threads to finish
        receive_audio_thread.join()
        play_audio_thread.join()

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
    client.sendMessage(msgDict, serverIP, serverPort)  # Request a connection to the server

    client.start_threads()  # Start the receive and play audio threads

    print("Received Messages: ", client._receivedMsgQte)
    print("Lost Messages: ", client._lostMsgQte)
    print("Out of Order Messages: ", client._outOfOrderMsgQte)
    client.close()

if __name__ == "__main__":
    main()
