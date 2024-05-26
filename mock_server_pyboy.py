import socket
import threading
import logging
import queue
import signal
import sys
from pyboy import PyBoy, WindowEvent

logging.basicConfig(level=logging.DEBUG)
q = queue.Queue()
exit_event = threading.Event()


def process_command(command, pyboy_instance):
    """Process the command and execute the corresponding game action."""
    try:
        logging.debug("Command received: %s", command)

        repeat_commands = 1

        # Split command based on space
        parts = command.split()

        # If there are two parts and the second part is a number
        if len(parts) == 2 and parts[1].isdigit():
            command = parts[0]
            repeat_commands = min(
                int(parts[1]), 100
            )  # Limit repetitions to a maximum of 20
        if command in ["l", "r", "u", "d", "b", "select", "start", "a"]:
            # Define the events based on the command
            if command == "l":
                events = [WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT]
            elif command == "r":
                events = [
                    WindowEvent.PRESS_ARROW_RIGHT,
                    WindowEvent.RELEASE_ARROW_RIGHT,
                ]
            elif command == "u":
                events = [WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP]
            elif command == "d":
                events = [WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN]
            elif command == "b":
                events = [WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B]
            elif command == "a":
                events = [WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A]
            elif command == "select":
                events = [
                    WindowEvent.PRESS_BUTTON_SELECT,
                    WindowEvent.RELEASE_BUTTON_SELECT,
                ]
            elif command == "start":
                events = [
                    WindowEvent.PRESS_BUTTON_START,
                    WindowEvent.RELEASE_BUTTON_START,
                ]

            # Perform the actions for the events
            for _ in range(repeat_commands):
                for event in events:
                    pyboy_instance.send_input(event)
                    logging.debug("Sending event: %s", event)
                    pyboy_instance.tick()  # Process one frame to let the game register the input
                    pyboy_instance.tick()
                    WindowEvent.RELEASE_ARROW_LEFT
                    pyboy_instance.tick()

        else:
            logging.debug("Not a command: %s", command)

    except Exception as e:
        logging.error(f"Error processing command: {e}")


def player(rom_path):
    pyboy = PyBoy(rom_path, sound=True)
    pyboy.set_emulation_speed(1)

    while not exit_event.is_set():
        try:
            item = q.get(block=False)
            process_command(item, pyboy)
        except queue.Empty:
            pass

        if pyboy.tick():
            return


def comms():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 65432))
        s.listen()
        logging.info("PyBoy Server started, waiting for commands...")

        conn, addr = s.accept()
        with conn:
            while not exit_event.is_set():
                command = conn.recv(1024).decode("utf-8")
                if not command:
                    break
                q.put(command)


def signal_handler(sig, frame):
    logging.info("Exiting...")
    exit_event.set()
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mock_server_pyboy.py <path_to_rom>")
        sys.exit(1)

    rom_path = sys.argv[1]

    signal.signal(signal.SIGINT, signal_handler)

    t1 = threading.Thread(target=player, args=(rom_path,))
    t2 = threading.Thread(target=comms)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
