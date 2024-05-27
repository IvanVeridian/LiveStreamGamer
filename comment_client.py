import socket

HOST, PORT = 'localhost', 65433

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        nickname = "test"
        comment = input("Enter comment: ")

        # Concatenate nickname and comment with '::' and send
        message = f"{nickname}::{comment}"
        s.sendall(message.encode('utf-8'))

        if comment.lower() == "exit":
            break

