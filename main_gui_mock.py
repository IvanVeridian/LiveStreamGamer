import tkinter as tk
from tkinter import scrolledtext, filedialog
import threading
import socket
import subprocess


class LiveStreamGamerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Stream Gamer Host")

        self.rom_path = tk.StringVar()

        # Input frame
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter Comment:").grid(row=0, column=0, padx=5)
        self.comment_entry = tk.Entry(input_frame, width=50)
        self.comment_entry.grid(row=0, column=1, padx=5)

        submit_button = tk.Button(
            input_frame, text="Submit", command=self.submit_comment
        )
        submit_button.grid(row=0, column=2, padx=5)

        # Output frame
        self.comment_output = self.create_output_frame("Submitted Comments")
        self.update_output_area(
            self.comment_output, f"Set ROM Path under Config before Starting Server"
        )

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
        self.comment_process = None

    def create_output_frame(self, title):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text=title).pack()
        output_area = scrolledtext.ScrolledText(
            frame, width=80, height=10, wrap=tk.WORD
        )
        output_area.pack(padx=5, pady=5)
        output_area.config(state=tk.DISABLED)
        return output_area

    def start_server(self):
        self.server_process = subprocess.Popen(
            ["python", "mock_server_pyboy.py", self.rom_path.get()],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.client_process = subprocess.Popen(
            ["python", "mock_tiktokclient.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.comment_process = subprocess.Popen(
            ["python", "mockcomment_client.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        threading.Thread(
            target=self.read_process_output,
            args=(self.comment_process, self.comment_output),
        ).start()

    def stop_server(self):
        self.terminate_process(self.server_process)
        self.terminate_process(self.client_process)
        self.terminate_process(self.comment_process)

    def terminate_process(self, process):
        if process:
            process.terminate()
            process.wait()

    def read_process_output(self, process, output_area):
        while True:
            output = process.stdout.readline()
            if output == b"" and process.poll() is not None:
                break
            if output:
                self.update_output_area(output_area, output.decode("utf-8").strip())

    def update_output_area(self, output_area, text):
        output_area.config(state=tk.NORMAL)
        output_area.insert(tk.END, text + "\n")
        output_area.config(state=tk.DISABLED)
        output_area.yview(tk.END)

    def submit_comment(self):
        comment = self.comment_entry.get()
        self.comment_entry.delete(0, tk.END)
        if comment.lower() == "exit":
            self.stop_server()
        else:
            threading.Thread(target=self.send_comment, args=(comment,)).start()
            self.update_output_area(self.comment_output, f"test::{comment}")

    def send_comment(self, comment):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("localhost", 65433))
                message = f"test::{comment}"
                s.sendall(message.encode("utf-8"))
                print(f"Sent: {message}")  # Debugging statement
        except Exception as e:
            print(f"Failed to send comment: {e}")  # Error handling

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

    def browse_rom_path(self):
        rom_path = filedialog.askopenfilename(
            filetypes=[("Game Boy ROMs", "*.gbc *.gb")]
        )
        self.rom_path.set(rom_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = LiveStreamGamerGUI(root)
    root.mainloop()
