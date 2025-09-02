# Secure-Chat
🔐 Secure Chat – Encrypted Messaging App
📌 Overview

Secure Chat is a Python-based client-server application that allows two users to exchange messages securely over a network.
It uses AES (Advanced Encryption Standard) to encrypt messages, ensuring privacy and confidentiality.

This project is part of my cybersecurity internship, where I am building hands-on projects to strengthen my practical skills.

⚡ Features

Encrypted communication between client and server

Secure key handling

Simple Python implementation (easy to understand)

Extendable for group chats or GUI integration in the future

🛠️ Tech Stack

Language: Python 3

Libraries: socket, cryptography (AES), threading

Platform: Windows / Linux

📂 Project Structure
secure-chat/
│── server.py          # Server-side script
│── client.py          # Client-side script
│── logs/              # Daily update (saved here)
│── screenshots/       # Screenshots of outputs

│── README.md          # Project overview (this file)

🚀 How to Run
1️⃣ Start the Server
python server.py

2️⃣ Start the Client
python client.py

3️⃣ Exchange Messages

Messages typed in the client appear in the server console (and vice versa).

Encrypted logs are saved in logs/.
