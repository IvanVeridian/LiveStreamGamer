from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, LikeEvent, GiftEvent, JoinEvent
import socket
import logging
import asyncio
from asyncio import Lock

logging.basicConfig(level=logging.INFO)

lock = Lock()

global pyboy_socket
pyboy_socket = None

# Initialize the client
client: TikTokLiveClient = TikTokLiveClient(unique_id="@tiktokusername")

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
        
@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)


@client.on("comment")
async def on_comment(event):
    logging.debug("on_comment start")
    print(f"{event.user.nickname} -> {event.comment}")

    async with lock:
        command = event.comment.lower()
        send_command_to_pyboy(command)

@client.on("like")
async def on_like(event: LikeEvent):
    print(f"@{event.user.unique_id} liked the stream!")
    async with lock:
        command = "likex34"
        send_command_to_pyboy(command)

@client.on("gift")
async def on_gift(event: GiftEvent):
    # Streakable gift & streak is over
    if event.gift.streakable and not event.gift.streaking:
        print(f"Thank you {event.user.unique_id}! They sent {event.gift.count}x \"{event.gift.info.name}\"")

    # Non-streakable gift
    elif not event.gift.streakable:
        print(f"Thank you {event.user.unique_id}! They sent \"{event.gift.info.name}\"")

@client.on("join")
async def on_join(event: JoinEvent):
    print(f"Hi and welcome, @{event.user.unique_id}! Thank you for joining the stream!")

def run_tiktok_client():
    logging.debug("run_tiktok_client start")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client.run()
    loop.close()
    logging.debug("run tiktok_client end")
    
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
    run_tiktok_client()