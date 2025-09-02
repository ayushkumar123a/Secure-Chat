import socket

def start_client(host="127.0.0.1", port=5555):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"[+] Connected to {host}:{port}")

    while True:
        msg = input("You: ")
        client.sendall(msg.encode())
        data = client.recv(1024).decode()
        print(f"Server: {data}")

if __name__ == "__main__":
    start_client()
