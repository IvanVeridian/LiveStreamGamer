import socket
import logging
import asyncio
from asyncio import Lock

logging.basicConfig(level=logging.DEBUG)

lock = Lock()

global pyboy_socket
pyboy_socket = None


# Mock the event classes to resemble the real ones
class ConnectEvent:
    pass

class CommentEvent:
    def __init__(self, user, comment):
        self.user = user
        self.comment = comment

class LikeEvent:
    def __init__(self, user):
        self.user = user

class GiftEvent:
    pass

class MockTikTokLiveClient:
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.listeners = {}

    def on(self, event_name):
        def decorator(func):
            self.listeners[event_name] = func
            return func
        return decorator

    def add_listener(self, event_name, func):
        self.listeners[event_name] = func

    async def emit(self, event_name, *args, **kwargs):
        if event_name in self.listeners:
            await self.listeners[event_name](*args, **kwargs)

    def run(self):
        # In the mock client, this won't do anything. It's just for compatibility.
        pass
        
# Initialize the client
client = MockTikTokLiveClient(unique_id="@tiktokusername")

def send_command_to_pyboy(command):
    """Send a command to the PyBoy script."""
    global pyboy_socket
    if pyboy_socket is None:
        logging.error("PyBoy socket is not connected.")
        return

    try:
        pyboy_socket.sendall(command.encode('utf-8'))
    except Exception as e:
        logging.error(f"Error sending command to PyBoy: {e}")


@client.on("comment")
async def on_comment(event):
    logging.debug("on_comment start")
    print(f"{event['user']['nickname']} -> {event['comment']}")

    async with lock:
        command = event['comment'].lower()
        send_command_to_pyboy(command)

# ... The rest of the event handlers, if they involve game actions, would also call send_command_to_pyboy ...
# Socket server to listen for comments
HOST, PORT = 'localhost', 65433
async def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server started, waiting for comments...")
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(2048).decode('utf-8') # Assuming that nickname + comment won't exceed 2048 bytes
                if not data:
                    break
                nickname, comment = data.split('::', 1) # Split on the first occurrence of '::'

                # Emit the comment event
                await client.emit("comment", {"user": {"nickname": nickname}, "comment": comment})

def run_mock_client():
    logging.debug("run_mock_client start")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_server())
    loop.close()
    logging.debug("run_mock_client end")

def connect_to_pyboy():
    global pyboy_socket
    try:
        pyboy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pyboy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        pyboy_socket.connect(('localhost', 65432))
    except Exception as e:
        logging.error(f"Error connecting to PyBoy: {e}")
        pyboy_socket = None

    
if __name__ == '__main__':
    connect_to_pyboy()
    run_mock_client()

