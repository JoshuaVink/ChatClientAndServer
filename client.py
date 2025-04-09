import tkinter as tk
import threading
import socket
import queue
import webbrowser
import re

host = '127.0.0.1'  # Or "localhost"
port = 5003         # Replace with your port

EMOJI_MAP = {
    ":)": "😊",
    ":(": "😢",
    ":D": "😄",
    "<3": "❤️",
    ":P": "😛",
    ":poop:": "💩",
    ";)": "😉",
    ":thumbsup:": "👍",
    ":fire:": "🔥"
    }

def replace_emojis(message):
    for shortcut, emoji in EMOJI_MAP.items():
        message = message.replace(shortcut, emoji)
    return message


class App:
    def __init__(self, master):
        self.master = master
        self.name = input("Enter your name: ")
        window_title = ("Client", self.name, "at", port)
        master.title(window_title)

        self.label_text = tk.StringVar()
        self.label = tk.Label(master, textvariable=self.label_text)
        self.label.pack()

        self.data_queue = queue.Queue()
        self.running = True

        self.chat_log = tk.Text(master, state='disabled', height=15, width=50)
        self.chat_log.pack()

        self.chat_log.tag_config("link", foreground="blue", underline=1)
        self.chat_log.tag_bind("link", "<Button-1>", self.open_url)
        self.chat_log.tag_config("own", background="#ccffcc", font=("Helvetica", 10, "bold"))
        self.chat_log.tag_config("other", background="white", font=("Helvetica", 10))
        self.own_msg = False

        # CHANGED: Use Text instead of Entry for multi-line input
        self.message_entry = tk.Text(master, height=3, width=40)
        self.message_entry.pack(side=tk.LEFT, padx=(10, 0))

        # NEW: Bind <Return> to send, and <Shift-Return> to newline
        self.message_entry.bind("<Return>", self.send_message)
        self.message_entry.bind("<Shift-Return>", self.insert_newline)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        # Socket connection
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((host, port))
            connect_msg = f"{self.name} has joined the chat."
            self.socket.sendall(connect_msg.encode())
        except Exception as e:
            self.append_message(f"Connection error: {e}")
            return

        self.socket_thread = threading.Thread(target=self.read_socket)
        self.socket_thread.daemon = True  # Allow program to exit even if thread is running
        self.socket_thread.start()

        self.update_gui()

    def append_message(self, message):
        self.chat_log.config(state='normal')

        tag = "own" if self.own_msg else "other"
        message = replace_emojis(message)  # This adds emojis

        url_pattern = r"(https?://[^\s]+)"
        parts = re.split(url_pattern, message)

        for part in parts:
            if re.match(url_pattern, part):
                start = self.chat_log.index(tk.END)
                self.chat_log.insert(tk.END, part, ("link", tag))
                end = self.chat_log.index(tk.END)
                self.chat_log.tag_add("link", start, end)
            else:
                self.chat_log.insert(tk.END, part, tag)

        self.chat_log.insert(tk.END, "\n")
        self.chat_log.config(state='disabled')
        self.chat_log.yview(tk.END)


    def read_socket(self):
        try:
            while self.running:
                data = self.socket.recv(1024)
                if not data:
                    break

                decoded_data = data.decode()
                if decoded_data.startswith(self.name + ": "):
                    continue

                self.data_queue.put(data.decode())
                self.own_msg = False
        except ConnectionResetError:
            self.data_queue.put("The chat server crashed. Please try reconnecting.")
        except Exception as e:
            self.data_queue.put(f"Error: {e}")

    def send_message(self, event=None):
        try:
            message = self.message_entry.get("1.0", tk.END).strip()
            if message:
                name_msg = (self.name + ": " + message)
                self.data_queue.put(message)
                self.own_msg = True
                self.socket.sendall(name_msg.encode())
        except Exception as e:
            self.append_message(f"Send error: {e}")
        self.message_entry.delete("1.0", tk.END)
        return 'break'  # Prevents a newline when pressing Enter

    def update_gui(self):
        try:
            data = self.data_queue.get_nowait()
            self.append_message(data)
        except queue.Empty:
            pass  # No data yet, ignore
        if self.running:
            self.master.after(100, self.update_gui) # Check every 100 ms

    def insert_newline(self, event=None):
        self.message_entry.insert(tk.INSERT, "\n")
        return 'break'  # Prevent default behavior

    def open_url(self, event):
        idx = self.chat_log.index(f"@{event.x},{event.y}")
        line_start = self.chat_log.index(f"{idx} linestart")
        line_end = self.chat_log.index(f"{idx} lineend")
        text = self.chat_log.get(line_start, line_end)

        match = re.search(r"(https?://[^\s]+)", text)
        if match:
            webbrowser.open(match.group(0))


    def close(self):
        self.running = False
        try:
            disconnect_msg = f"{self.name} has left the chat."
            self.socket.sendall(disconnect_msg.encode())
            print(f"{self.name} disconnected.")
        except:
            pass  # Ignore errors if socket is already closed
        finally:
            self.socket.close()
            self.master.destroy()



root = tk.Tk()
app = App(root)
root.protocol("WM_DELETE_WINDOW", app.close)  # Handle window close event
root.mainloop()
