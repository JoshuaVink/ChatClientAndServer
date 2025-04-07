import tkinter as tk
import threading
import socket
import queue

host = '127.0.0.1'  # Or "localhost"
port = 5000         # Replace with your port


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

        self.message_entry = tk.Entry(master, width=40)
        self.message_entry.pack(side=tk.LEFT, padx=(10, 0))
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        # Socket connection
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((host, port))
        except Exception as e:
            self.append_message(f"Connection error: {e}")
            return

        self.socket_thread = threading.Thread(target=self.read_socket)
        self.socket_thread2 = threading.Thread(target=self.send_message)
        self.socket_thread.daemon = True  # Allow program to exit even if thread is running
        self.socket_thread2.daemon = True
        self.socket_thread.start()
        self.socket_thread2.start()

        self.update_gui()

    def append_message(self, message):
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state='disabled')
        self.chat_log.yview(tk.END)

    def read_socket(self):
        try:
            while self.running:
                data = self.socket.recv(1024)
                if not data:
                    break
                self.data_queue.put(data.decode())
        except Exception as e:
            self.data_queue.put(f"Error: {e}")

    def send_message(self, event=None):
        try:
            message = self.message_entry.get().strip()
            if message:
                name_msg = (self.name + ": " + message)
                self.socket.sendall(name_msg.encode())
        except Exception as e:
            self.data_queue.put(f"Error: {e}")
        self.message_entry.delete(0, tk.END)

    def update_gui(self):
        try:
            data = self.data_queue.get_nowait()
            self.label_text.set(data)
        except queue.Empty:
            pass  # No data yet, ignore
        if self.running:
            self.master.after(100, self.update_gui) # Check every 100 ms

    def close(self):
        self.running = False
        self.master.destroy()


root = tk.Tk()
app = App(root)
root.protocol("WM_DELETE_WINDOW", app.close)  # Handle window close event
root.mainloop()
