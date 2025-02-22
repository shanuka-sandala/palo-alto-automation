import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Toplevel
import requests
import os
from datetime import datetime
import threading
import queue
import xml.etree.ElementTree as ET

__version__ = "1.1.0"
__author__ = "Shanuka Jayakodi"
__contact__ = "shanuka@the-debugging-diaries.com"
__blog__ = "https://the-debugging-diarie.com"

class FirewallBackupTool:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Palo Alto Running Config Backup Tool")
        self.log_queue = queue.Queue()
        
        self.create_widgets()
        self.process_queue()

    def create_widgets(self):
        # IP Address Input
        ttk.Label(self.root, text="Firewall IPs (comma-separated):").grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.ip_entry = ttk.Entry(self.root, width=160)
        self.ip_entry.grid(column=0, row=1, padx=5, pady=5, columnspan=1)

        # Username Input
        ttk.Label(self.root, text="Username:").grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.root, width=40)
        self.username_entry.grid(column=0, row=2, padx=5, pady=5, columnspan=1)

        # Password Input
        ttk.Label(self.root, text="Password:").grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.root, width=40, show="*")
        self.password_entry.grid(column=0, row=4, padx=5, pady=5, columnspan=1)

        # Buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.grid(column=0, row=6, padx=5, pady=5, columnspan=2, sticky=tk.EW)
        
        self.start_btn = ttk.Button(self.button_frame, text="Start Backup", command=self.start_backup)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.info_btn = ttk.Button(self.button_frame, text="Info", command=self.show_info)
        self.info_btn.pack(side=tk.LEFT, padx=5)

        # Log Display
        self.log_text = scrolledtext.ScrolledText(self.root, width=120, height=30, state='disabled')
        self.log_text.grid(column=0, row=7, padx=5, pady=5, columnspan=2)

    def show_info(self):
        info_window = Toplevel(self.root)
        info_window.title("About")
        
        info_text = f"""Palo Alto Backup Tool
Version: {__version__}
Author: {__author__}
Contact: {__contact__}
Blog: {__blog__}"""
        
        text = scrolledtext.ScrolledText(info_window, width=60, height=10)
        text.insert(tk.INSERT, info_text)
        text.configure(state='disabled')
        text.pack(padx=10, pady=10)

    def log_message(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.configure(state='disabled')
        self.log_text.see(tk.END)

    def process_queue(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get_nowait()
            self.log_message(msg)
        self.root.after(100, self.process_queue)

    def get_api_key(self, ip, username, password):
        try:
            url = f"https://{ip}/api/?type=keygen&user={username}&password={password}"
            response = requests.get(url, verify=False, timeout=10)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                return root.find('.//key').text
            return None
        except Exception as e:
            self.log_queue.put(f"Error getting API key for {ip}: {str(e)}")
            return None

    def backup_firewall(self, ip, username, password):
        try:
            # Get API key first
            api_key = self.get_api_key(ip, username, password)
            if not api_key:
                self.log_queue.put(f"Failed: {ip} - Could not obtain API key")
                return

            # Configuration export
            url = f"https://{ip}/api/"
            params = {
                'type': 'export',
                'category': 'configuration',
                'key': api_key
            }

            response = requests.get(url, params=params, verify=False, timeout=15)
            
            if response.status_code == 200:
                date_str = datetime.now().strftime('%Y-%m-%d')
                backup_dir = os.path.join('C:\\', 'Configuration-Backups', date_str)
                os.makedirs(backup_dir, exist_ok=True)
                
                file_path = os.path.join(backup_dir, f'{ip}-running-config.xml')
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                self.log_queue.put(f"Success: {ip} - Backup saved to {file_path}")
            else:
                self.log_queue.put(f"Failed: {ip} - HTTP Error {response.status_code}")

        except Exception as e:
            self.log_queue.put(f"Failed: {ip} - Error: {str(e)}")

    def start_backup(self):
        ips = [ip.strip() for ip in self.ip_entry.get().split(',') if ip.strip()]
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not ips:
            self.log_message("Error: Please provide at least one IP address")
            return
        if not username or not password:
            self.log_message("Error: Please provide both username and password")
            return

        for ip in ips:
            thread = threading.Thread(target=self.backup_firewall, args=(ip, username, password))
            thread.daemon = True
            thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = FirewallBackupTool(root)
    root.mainloop()