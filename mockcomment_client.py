import socket

HOST = "localhost"
PORT = 65433


def run_mock_comment_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to server. You can start sending comments.")

        while True:
            # Prompt user for input
            comment = input("Enter your comment (or type 'exit' to quit): ")
            if comment.lower() == "exit":
                break

            # Send comment to the server
            try:
                message = f"mock_user::{comment}"
                s.sendall(message.encode("utf-8"))
            except Exception as e:
                print(f"Failed to send comment: {e}")
                break


if __name__ == "__main__":
    run_mock_comment_client()
