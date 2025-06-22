import socket
import time
import threading
import tkinter as tk
from tkinter import messagebox, ttk

class SpeedTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Speed Tester")
        self.root.attributes('-fullscreen', True)  # Full-screen mode
        self.root.configure(bg="#1e1e2e")  # Dark background color
        self.root.bind("<Escape>", self.exit_fullscreen)  # Press Esc to exit full-screen
        
        # Main Frame
        self.main_frame = tk.Frame(root, bg="#282A36", padx=20, pady=20)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Title
        self.title_label = tk.Label(self.main_frame, text="Network Speed Tester", 
                                    font=("Helvetica", 24, "bold"), fg="#ff79c6", bg="#282A36")
        self.title_label.pack(pady=10)

        # Mode Selection
        self.mode_label = tk.Label(self.main_frame, text="Select Mode:", font=("Arial", 16), fg="white", bg="#282A36")
        self.mode_label.pack(pady=5)
        
        self.mode_var = tk.StringVar(value="client")
        self.client_button = ttk.Radiobutton(self.main_frame, text="Client", variable=self.mode_var, value="client")
        self.client_button.pack(pady=5)
        self.server_button = ttk.Radiobutton(self.main_frame, text="Server", variable=self.mode_var, value="server")
        self.server_button.pack(pady=5)
        
        # Server IP for Client Mode
        self.ip_label = tk.Label(self.main_frame, text="Server IP (for Client):", font=("Arial", 14), fg="white", bg="#282A36")
        self.ip_label.pack()
        self.ip_entry = ttk.Entry(self.main_frame, font=("Arial", 12), width=30)
        self.ip_entry.pack(pady=5)
        
        # Buttons
        self.start_button = ttk.Button(self.main_frame, text="Start Test", command=self.start, style="TButton")
        self.start_button.pack(pady=10)
        
        self.speed_label = tk.Label(self.main_frame, text="Speed: 0 Mbps", font=("Arial", 18, "bold"), fg="#50fa7b", bg="#282A36")
        self.speed_label.pack(pady=10)
        
        self.stop_button = ttk.Button(self.main_frame, text="Stop", command=self.stop, style="TButton")
        self.stop_button.pack(pady=10)
        self.stop_button.config(state=tk.DISABLED)

        self.running = False

        # Style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 14), padding=10)
        self.style.configure("TRadiobutton", background="#282A36", foreground="white", font=("Arial", 12))

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

    def start(self):
        self.running = True
        mode = self.mode_var.get()
        if mode == "server":
            threading.Thread(target=self.server, daemon=True).start()
        else:
            server_ip = self.ip_entry.get()
            if not server_ip:
                messagebox.showerror("Error", "Enter server IP")
                return
            threading.Thread(target=self.client, args=(server_ip,), daemon=True).start()
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.speed_label.config(text="Testing... ⏳")

    def stop(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.speed_label.config(text="Speed: 0 Mbps")

    def server(self, host='0.0.0.0', port=12345, buffer_size=4096):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
        
        while self.running:
            start_time = time.time()
            data, addr = s.recvfrom(buffer_size)
            end_time = time.time()
            
            data_size = len(data)
            speed_mbps = (data_size * 8) / (end_time - start_time) / 1e6
            self.speed_label.config(text=f"Download Speed: {speed_mbps:.2f} Mbps ✅")

    def client(self, server_ip, port=12345, packet_size=4096, duration=5):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        data = b'0' * packet_size
        start_time = time.time()
        total_bytes_sent = 0
        
        while time.time() - start_time < duration and self.running:
            s.sendto(data, (server_ip, port))
            total_bytes_sent += packet_size
        
        end_time = time.time()
        upload_speed_mbps = (total_bytes_sent * 8) / (end_time - start_time) / 1e6
        self.speed_label.config(text=f"Upload Speed: {upload_speed_mbps:.2f} Mbps ✅")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTester(root)
    root.mainloop()
