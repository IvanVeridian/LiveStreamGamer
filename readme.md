# LiveStreamGamer

This repository contains a set of Python scripts designed to integrate TikTok Live streaming with a PyBoy Gameboy emulator, allowing for interactive game sessions through TikTok comments. 

## Description

The project is structured into several key components:

1. **TikTokClient.py**: Connects to a TikTok Live session and listens for events such as comments, likes, and gifts. It sends specific commands to the PyBoy emulator based on these interactions.

2. **Server-Pyboy.py**: A server that receives commands from the TikTok client and processes them in the PyBoy emulator to simulate game actions.

3. **TikTokClient-mock.py**: A mock implementation of the TikTok client for testing purposes without connecting to an actual live session.

4. **Server-Pyboy-mock.py**: Similar to Server-Pyboy.py but designed for use with the mock TikTok client.

5. **comment_client.py**: Used to simulate a live TikTok session by sending comments to the mock TikTok client.

## Requirements

- Python 3.x
- PyBoy emulator
- TikTokLive Python library
- asyncio, socket, threading, logging, queue libraries

## Setup and Usage

1. **Setting up the environment**: 
   - Ensure Python 3.x is installed.
   - Install required Python libraries (`pip install <library_name>`).

2. **Running the TikTok Client**:
   - Run `TikTokClient.py` to start listening to a live TikTok session.
   - Ensure to replace `@tiktokusername` with the actual TikTok username.

3. **Running the PyBoy Server**:
   - Run `Server-Pyboy.py` in parallel to receive and process commands.
   - Replace the dir `pyboy = PyBoy('C:\\Users\\user\\LiveStreamGamer\\Silver.gbc', sound=True)` with your own

4. **Testing with Mock Client**:
   - Use `tiktokclient-mock.py` and `Server-Pyboy-mock.py` for testing without a live TikTok session.
   - Run the mock client and server scripts.
   - Replace the dir `pyboy = PyBoy('C:\\Users\\user\\LiveStreamGamer\\Silver.gbc', sound=True)` with your own

5. **Simulating Comments with the Mock Server/Client**:
   - Run `comment_client.py` to send simulated comments to the TikTok client.

## Contributing

Feel free to fork this repository and contribute to the development. Pull requests are welcome.

## License

MIT

## Shoutout
https://github.com/Baekalfen/PyBoy
https://github.com/isaackogan/TikTokLive

Huge thanks to the creators/maintainers of the above, they made this project possible.
