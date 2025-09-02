# secure-chat/server.py
import socket
from cryptography.fernet import Fernet
from pathlib import Path

# Generate or load key
key_file = Path("secret.key")
if key_file.exists():
    key = key_file.read_bytes()
else:
    key = Fernet.generate_key()
    key_file.write_bytes(key)

cipher = Fernet(key)

# Setup logging
log_file = Path("logs/server_log.txt")
log_file.parent.mkdir(parents=True, exist_ok=True)

def log(msg):
    with open(log_file, "a") as f:
        f.write(msg + "\n")

# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 12345))
server.listen(1)
print("[*] Server listening on port 12345...")

conn, addr = server.accept()
print(f"[+] Connection from {addr}")
log(f"Client connected: {addr}")

while True:
    data = conn.recv(4096)
    if not data:
        break
    try:
        decrypted = cipher.decrypt(data).decode()
        print(f"[Client] {decrypted}")
        log(f"Client: {decrypted}")

        response = input("You: ")
        encrypted = cipher.encrypt(response.encode())
        conn.send(encrypted)
        log(f"Server: {response}")
    except Exception as e:
        print("Decryption error:", e)
        break

conn.close()
