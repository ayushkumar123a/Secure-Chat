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

# Server Setup
HOST = "127.0.0.1"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}  # {conn: username}

def broadcast(message, sender=None, target=None):
    """Send message to all or to a specific target client."""
    for conn, uname in clients.items():
        if conn == sender:
            continue
        if target and uname != target:
            continue
        try:
            conn.send(encrypt(message).encode())
        except:
            conn.close()
            del clients[conn]

def handle_client(conn):
    try:
        username = decrypt(conn.recv(1024).decode())
        clients[conn] = username
        print(f"[+] {username} connected.")

        while True:
            enc_msg = conn.recv(4096).decode()
            if not enc_msg:
                break
            msg = decrypt(enc_msg)

            # Private or broadcast?
            if msg.startswith("@"):  
                try:
                    target_name, real_msg = msg[1:].split(" ", 1)
                    print(f"[PRIVATE] {username} -> {target_name}: {real_msg}")
                    broadcast(f"[PRIVATE] {username}: {real_msg}", sender=conn, target=target_name)
                except:
                    conn.send(encrypt("Invalid private message format. Use @username <msg>").encode())
            else:
                print(f"[BROADCAST] {username}: {msg}")
                broadcast(f"{username}: {msg}", sender=conn)
    except:
        pass
    finally:
        if conn in clients:
            print(f"[-] {clients[conn]} disconnected.")
            del clients[conn]
            conn.close()

def server_input():
    while True:
        msg = input("")
        if msg.strip():
            print(f"[SERVER]: {msg}")
            broadcast(f"[SERVER]: {msg}")

print(f"[*] Server running on {HOST}:{PORT}")
threading.Thread(target=server_input, daemon=True).start()

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn,), daemon=True).start()
