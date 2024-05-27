# TikTok Live Gaming Integration

This repository contains a set of Python scripts designed to integrate TikTok Live streaming with a PyBoy Gameboy emulator, allowing for interactive game sessions through TikTok comments. 

## Description

The project is structured into several key components:

1. **tiktokclient.py**: Connects to a TikTok Live session and listens for events such as comments, likes, and gifts. It sends specific commands to the PyBoy emulator based on these interactions.

2. **server_pyboy.py**: A server that receives commands from the TikTok client and processes them in the PyBoy emulator to simulate game actions.

3. **mock_tiktokclient.py**: A mock implementation of the TikTok client for testing purposes without connecting to an actual live session.

4. **mock_server_pyboy.py**: Similar to server_pyboy.py but designed for use with the mock TikTok client.

5. **mockcomment_client.py**: Used to simulate a live TikTok session by sending comments to the TikTok client.

6. **main_gui_mock.py**: A GUI application to control and configure the mock setup, allowing users to define the PyBoy ROM location and simulate comments through an interactive interface.

6. **main_gui.py**: A GUI application to control and configure the live setup.

## Requirements

- Python 3.x
- PyBoy emulator
- TikTokLive Python library
- asyncio, socket, threading, logging, queue libraries
- tkinter (for GUI)

## Setup and Usage

1. **Setting up the environment**: 
   - Ensure Python 3.x is installed.
   - Install required Python libraries:
     ```sh
     pip install -r requirements.txt
     ```

2. **Running Main Gui for Live**:
   - Run `main_gui.py` to start listening to a live TikTok session.
   - Ensure to complete the config setup, under the config button.

3. **Testing with Mock Client Using GUI**:
   - Use `main_gui_mock.py` for a GUI-based interface to run and control the mock setup.
   - Run the GUI script using:
     ```sh
     python main_gui.py
     ```
   - In the GUI, use the "Config" button to select the PyBoy ROM file.
   - Start the server and client processes through the GUI buttons.
   - Simulate comments directly from the GUI.

## GUI Instructions

1. **Start the GUI**:
   - Run `python main_gui_mock.py` or `python main_gui.py` to start the GUI application.

2. **Config Setup**:
   - Click on the "Config" button to open the configuration window.
   - Browse and select the PyBoy ROM file location.
   - Enter tiktok username if using main_gui, pull the username from their main profile page (@username without the @ symbol)

3. **Starting and Stopping the Server**:
   - Use the "Start Server" button to start the mock server and client processes.
   - Use the "Stop Server" button to stop all running processes.

4. **Submitting Comments**:
   - Enter a comment in the input field and click "Submit" to send the comment.
   - The submitted comments and server outputs will be displayed in the output area.

## Screenshots

![image](https://github.com/IvanVeridian/LiveStreamGamer/assets/100320639/f9d3c8b7-8b45-41da-af7d-31bda4bbd333)
![unnamed](https://github.com/IvanVeridian/LiveStreamGamer/assets/100320639/33d8a3ef-7711-4123-8059-b629f7d0aff9)


## Contributing

Feel free to fork this repository and contribute to the development. Pull requests are welcome.

## License

MIT
