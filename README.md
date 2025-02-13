# Keylogger Project

This is a Python-based keylogger tool that listens for keyboard events, encrypts the captured keystrokes, and periodically writes them to a file.
It includes functionality for both encryption and decryption of captured data using a simple XOR encryption algorithm.

## Features
- **Key Logging**: Captures keypress events (including special keys like space and enter).
- **Encryption**: Captures keystrokes and encrypts them using XOR encryption.
- **File Writing**: Writes encrypted keystrokes to a file every 10 seconds.
- **Decryption**: Decrypts the encrypted file contents and writes the plain text to a separate file.
