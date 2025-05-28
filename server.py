from socket import *
import threading
import tkinter as tk
from tkinter import messagebox
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame, filedialog, CTkTextbox

class ChatClient:
    def __init__(self):
        self.root = CTk()
        self.root.title("Chat Client")
        self.username = ""
        self.sock = None
        self.setup_ui()
        
    def setup_ui(self):
        # Login Frame
        self.login_frame = CTkFrame(self.root)
        self.login_frame.pack(pady=20)
        
        self.name_label = CTkLabel(self.login_frame, text="Enter your name:")
        self.name_label.pack(pady=5)
        
        self.name_entry = CTkEntry(self.login_frame, width=200)
        self.name_entry.pack(pady=5)
        
        self.login_button = CTkButton(self.login_frame, text="Join Chat", command=self.connect_to_server)
        self.login_button.pack(pady=10)
        
        # Chat Frame (initially hidden)
        self.chat_frame = CTkFrame(self.root)
        
        self.chat_textbox = CTkTextbox(self.chat_frame, width=400, height=300, state="disabled")
        self.chat_textbox.pack(pady=10, padx=10)
        
        self.message_entry = CTkEntry(self.chat_frame, width=350)
        self.message_entry.pack(side="left", pady=10, padx=5)
        self.message_entry.bind("<Return>", self.send_message)
        
        self.send_button = CTkButton(self.chat_frame, text="Send", width=50, command=self.send_message)
        self.send_button.pack(side="left", pady=10)
    
    def connect_to_server(self):
        self.username = self.name_entry.get().strip()
        if not self.username:
            messagebox.showerror("Error", "Please enter a name")
            return
            
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            # Replace with your actual server address
            self.sock.connect(('2.tcp.eu.ngrok.io', 16963))
            
            # Send join message
            join_msg = f"TEXT@{self.username}@[SYSTEM] {self.username} joined the chat!\n"
            self.sock.send(join_msg.encode('utf-8'))
            
            # Switch to chat UI
            self.login_frame.pack_forget()
            self.chat_frame.pack(pady=20)
            
            # Start receiving thread
            threading.Thread(target=self.receive_messages, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to server: {e}")
    
    def receive_messages(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message:
                    self.add_message(message)
                else:
                    break
            except Exception as e:
                self.add_message(f"[SYSTEM] Connection error: {e}")
                break
    
    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message:
            try:
                full_msg = f"TEXT@{self.username}@{message}\n"
                self.sock.send(full_msg.encode('utf-8'))
                self.message_entry.delete(0, 'end')
            except Exception as e:
                self.add_message(f"[SYSTEM] Failed to send message: {e}")
    
    def add_message(self, message):
        self.chat_textbox.configure(state="normal")
        self.chat_textbox.insert("end", message + "\n")
        self.chat_textbox.configure(state="disabled")
        self.chat_textbox.see("end")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    client = ChatClient()
    client.run()