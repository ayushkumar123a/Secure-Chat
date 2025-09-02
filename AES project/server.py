import socket

def start_server(host="127.0.0.1", port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"[+] Server listening on {host}:{port}")

    conn, addr = server.accept()
    print(f"[+] Connected by {addr}")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"Client: {data}")
        reply = input("You: ")
        conn.sendall(reply.encode())

    conn.close()

if __name__ == "__main__":
    start_server()
