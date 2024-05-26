import tkinter as tk
from tkinter import scrolledtext, filedialog
import threading
import socket
import subprocess
import queue
import os


class LiveStreamGamerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Stream Gamer Host")

        self.rom_path = tk.StringVar()
        self.tiktok_username = tk.StringVar()

        # Input frame
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        # Output frame
        self.comment_output = self.create_output_frame("Output")

        # Buttons to start and stop the server
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        start_button = tk.Button(
            button_frame, text="Start Server", command=self.start_server
        )
        start_button.grid(row=0, column=0, padx=5)

        stop_button = tk.Button(
            button_frame, text="Stop Server", command=self.stop_server
        )
        stop_button.grid(row=0, column=1, padx=5)

        config_button = tk.Button(
            button_frame, text="Config", command=self.open_config_window
        )
        config_button.grid(row=0, column=2, padx=5)

        self.server_process = None
        self.client_process = None

        self.output_queue = queue.Queue()
        self.root.after(100, self.update_output)

    def create_output_frame(self, title):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text=title).pack()
        output_area = scrolledtext.ScrolledText(
            frame, width=80, height=20, wrap=tk.WORD
        )
        output_area.pack(padx=5, pady=5)
        output_area.config(state=tk.DISABLED)
        return output_area

    def start_server(self):
        self.update_tiktok_username()
        self.server_process = subprocess.Popen(
            ["python", "server_pyboy.py", self.rom_path.get()],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        )
        self.client_process = subprocess.Popen(
            ["python", "tiktokclient.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        )

        threading.Thread(
            target=self.read_process_output,
            args=(self.server_process, self.comment_output),
            daemon=True,
        ).start()

        threading.Thread(
            target=self.read_process_output,
            args=(self.client_process, self.comment_output),
            daemon=True,
        ).start()

    def stop_server(self):
        self.terminate_process(self.server_process)
        self.terminate_process(self.client_process)

    def terminate_process(self, process):
        if process:
            process.terminate()
            process.wait()

    def read_process_output(self, process, output_area):
        for line in process.stdout:
            self.output_queue.put(line)
        for line in process.stderr:
            self.output_queue.put(line)

    def update_output_area(self, output_area, text):
        output_area.config(state=tk.NORMAL)
        output_area.insert(tk.END, text + "\n")
        output_area.config(state=tk.DISABLED)
        output_area.yview(tk.END)

    def update_output(self):
        while not self.output_queue.empty():
            line = self.output_queue.get_nowait()
            self.update_output_area(self.comment_output, line.strip())
        self.root.after(100, self.update_output)

    def open_config_window(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuration")

        tk.Label(config_window, text="Select PyBoy ROM Path:").pack(pady=10)
        path_entry = tk.Entry(config_window, textvariable=self.rom_path, width=50)
        path_entry.pack(padx=10)

        browse_button = tk.Button(
            config_window, text="Browse", command=self.browse_rom_path
        )
        browse_button.pack(pady=10)

        tk.Label(config_window, text="Enter TikTok Username:").pack(pady=10)
        username_entry = tk.Entry(
            config_window, textvariable=self.tiktok_username, width=50
        )
        username_entry.pack(padx=10, pady=5)

        save_button = tk.Button(
            config_window, text="Save", command=config_window.destroy
        )
        save_button.pack(pady=10)

    def browse_rom_path(self):
        rom_path = filedialog.askopenfilename(
            filetypes=[("Game Boy ROMs", "*.gbc *.gb")]
        )
        self.rom_path.set(rom_path)

    def update_tiktok_username(self):
        with open("tiktokclient.py", "r") as file:
            lines = file.readlines()
        with open("tiktokclient.py", "w") as file:
            for line in lines:
                if line.strip().startswith("client: TikTokLiveClient"):
                    file.write(
                        f'client: TikTokLiveClient = TikTokLiveClient(unique_id="@{self.tiktok_username.get()}")\n'
                    )
                else:
                    file.write(line)


if __name__ == "__main__":
    root = tk.Tk()
    app = LiveStreamGamerGUI(root)
    root.mainloop()
