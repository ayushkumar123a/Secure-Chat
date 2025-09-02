import socket
import threading
from Crypto.Cipher import AES
import base64
import hashlib

# AES Setup
SECRET_KEY = "mysecretkey"
key = hashlib.sha256(SECRET_KEY.encode()).digest()

def encrypt(msg):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt(enc_msg):
    data = base64.b64decode(enc_msg)
    nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

# Connect to Server
HOST = "127.0.0.1"
PORT = 5555
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Enter your username: ")
client.send(encrypt(username).encode())

def receive():
    while True:
        try:
            enc_msg = client.recv(4096).decode()
            msg = decrypt(enc_msg)
            print(msg)
        except:
            print("[!] Connection closed.")
            client.close()
            break

def send():
    while True:
        msg = input("")
        if msg.strip():
            client.send(encrypt(msg).encode())

threading.Thread(target=receive, daemon=True).start()
send()
