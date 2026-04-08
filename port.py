import socket
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time

COMMON_PORTS = {
    21: ("FTP", "High"),
    22: ("SSH", "Low"),
    23: ("Telnet", "High"),
    25: ("SMTP", "Medium"),
    53: ("DNS", "Low"),
    80: ("HTTP", "Medium"),
    443: ("HTTPS", "Low"),
    445: ("SMB", "High"),
    3306: ("MySQL", "High"),
    3389: ("RDP", "High"),
}

# ---------------------------
# Scanner
# ---------------------------
class PortScanner:
    def __init__(self, target, start, end):
        self.target = target
        self.start = start
        self.end = end
        self.running = True
        self.open_ports = []

    def stop(self):
        self.running = False

    def scan(self, callback, progress_callback):
        total = self.end - self.start + 1
        count = 0

        for port in range(self.start, self.end + 1):
            if not self.running:
                break

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                result = s.connect_ex((self.target, port))

                if result == 0:
                    service, risk = COMMON_PORTS.get(port, ("Unknown", "Low"))
                    self.open_ports.append((port, service, risk))
                    callback(port, service, risk)

                s.close()
            except:
                pass

            count += 1
            progress_callback(count, total)


# ---------------------------
# GUI
# ---------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Port Scanner")
        self.geometry("850x550")
        self.configure(bg="#f5f5f5")

        self.scanner = None
        self.start_time = None

        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Network Port Scanner",
                 font=("Segoe UI", 16, "bold"),
                 bg="#f5f5f5").pack(pady=10)

        # INPUT
        frame = tk.Frame(self, bg="#f5f5f5")
        frame.pack(pady=5)

        tk.Label(frame, text="Target:", bg="#f5f5f5").grid(row=0, column=0)
        self.target_entry = tk.Entry(frame, width=25)
        self.target_entry.grid(row=0, column=1)

        tk.Label(frame, text="Start Port:", bg="#f5f5f5").grid(row=0, column=2)
        self.start_entry = tk.Entry(frame, width=10)
        self.start_entry.insert(0, "1")
        self.start_entry.grid(row=0, column=3)

        tk.Label(frame, text="End Port:", bg="#f5f5f5").grid(row=0, column=4)
        self.end_entry = tk.Entry(frame, width=10)
        self.end_entry.insert(0, "1024")
        self.end_entry.grid(row=0, column=5)

        # BUTTONS
        btn_frame = tk.Frame(self, bg="#f5f5f5")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Start Scan", command=self.start_scan).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Stop", command=self.stop_scan).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Export", command=self.export).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Quick Scan", command=self.quick_scan).grid(row=0, column=4, padx=5)

        # STATUS
        self.progress = ttk.Progressbar(self, length=600)
        self.progress.pack(pady=5)

        self.status_label = tk.Label(self, text="Status: Idle", bg="#f5f5f5")
        self.status_label.pack()

        self.info_label = tk.Label(self, text="Open Ports: 0 | Time: 0s", bg="#f5f5f5")
        self.info_label.pack()

        # TABLE
        columns = ("Port", "Service", "Risk Level")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    # ---------- FUNCTIONS ----------
    def validate_target(self, target):
        try:
            socket.gethostbyname(target)
            return True
        except:
            return False

    def start_scan(self):
        target = self.target_entry.get()

        if not self.validate_target(target):
            messagebox.showerror("Error", "Invalid IP / Hostname")
            return

        try:
            start = int(self.start_entry.get())
            end = int(self.end_entry.get())
        except:
            messagebox.showerror("Error", "Invalid port range")
            return

        self.tree.delete(*self.tree.get_children())
        self.progress["value"] = 0
        self.status_label.config(text="Status: Scanning...")
        self.start_time = time.time()

        self.scanner = PortScanner(target, start, end)

        threading.Thread(target=self.run_scan, daemon=True).start()

    def run_scan(self):
        def update(port, service, risk):
            self.tree.insert("", "end", values=(port, service, risk))
            self.update_info()

        def progress_update(count, total):
            self.progress["value"] = (count / total) * 100

        self.scanner.scan(update, progress_update)

        elapsed = round(time.time() - self.start_time, 2)
        self.status_label.config(text="Status: Completed")
        self.info_label.config(text=f"Open Ports: {len(self.scanner.open_ports)} | Time: {elapsed}s")

        messagebox.showinfo("Done", "Scan Completed")

    def update_info(self):
        self.info_label.config(text=f"Open Ports: {len(self.scanner.open_ports)}")

    def stop_scan(self):
        if self.scanner:
            self.scanner.stop()
            self.status_label.config(text="Status: Stopped")

    def export(self):
        if not self.scanner:
            return

        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if not file:
            return

        with open(file, "w") as f:
            for port, service, risk in self.scanner.open_ports:
                f.write(f"{port} - {service} ({risk})\n")

    def clear(self):
        self.tree.delete(*self.tree.get_children())
        self.progress["value"] = 0
        self.status_label.config(text="Status: Idle")
        self.info_label.config(text="Open Ports: 0 | Time: 0s")

    def quick_scan(self):
        self.start_entry.delete(0, END)
        self.end_entry.delete(0, END)
        self.start_entry.insert(0, "1")
        self.end_entry.insert(0, "1024")


# RUN
if __name__ == "__main__":
    app = App()
    app.mainloop()