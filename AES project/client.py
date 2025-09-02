# secure-chat/client.py
import socket
from cryptography.fernet import Fernet
from pathlib import Path

# Load key (must be the same as server)
key = Path("secret.key").read_bytes()
cipher = Fernet(key)

# Setup logging
log_file = Path("logs/client_log.txt")
log_file.parent.mkdir(parents=True, exist_ok=True)

def log(msg):
    with open(log_file, "a") as f:
        f.write(msg + "\n")

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))
print("[+] Connected to server")
log("Connected to server")

while True:
    msg = input("You: ")
    encrypted = cipher.encrypt(msg.encode())
    client.send(encrypted)
    log(f"Client: {msg}")

    data = client.recv(4096)
    if not data:
        break
    decrypted = cipher.decrypt(data).decode()
    print(f"[Server] {decrypted}")
    log(f"Server: {decrypted}")

client.close()
