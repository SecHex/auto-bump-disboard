import time
import webbrowser
import tkinter as tk
import customtkinter
import sys
import os
import winreg


class ServerIDWindow(customtkinter.CTk):
    def __init__(self):
        self.server_id = ""
        self.create_gui()

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("RPZ-Bumper")
        self.root.geometry("300x200")
        self.root.config(bg="#36393f")
        self.root.iconbitmap("2.ico")
        self.root.resizable(False, False)

        self.frame_1 = customtkinter.CTkFrame(self.root, fg_color="#323336")
        self.frame_1.pack(pady=20, padx=30, fill="both", expand=True)

        id_label = customtkinter.CTkLabel(self.frame_1, text="RPZ - AutoBumper", fg_color="transparent",
                                          font=("Arial", 16, "bold"))
        id_label.pack(side="top", padx=10, pady=10)

        self.id_entry = customtkinter.CTkEntry(self.frame_1, placeholder_text="Server ID")
        self.id_entry.pack(side="top", padx=10, pady=5)

        start_button = customtkinter.CTkButton(self.frame_1, text="Continue", command=self.set_server_id, fg_color="#5a5f69", hover_color="#42474f")
        start_button.pack(side="top", pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)

        self.root.mainloop()



    def set_server_id(self):
        server_id = self.id_entry.get()

        if not server_id:
            error_label = customtkinter.CTkLabel(self.frame_1, text="Please enter a server ID", text_color="red")
            error_label.pack(side="top", padx=10, pady=5)
        else:
            self.server_id = server_id
            self.root.destroy()

    def exit_program(self):
        sys.exit()


class BumpTimerApp(customtkinter.CTk):
    def __init__(self, server_id):
        self.base_url = "https://disboard.org/de/server/bump/"
        self.server_id = server_id
        self.url = ""
        self.interval = 1 * 60 * 60
        self.next_bump = 0
        self.autostart_enabled = False

        self.create_gui()

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("RPZ-Bumper")
        self.root.geometry("300x350")
        self.root.config(bg="#36393f")
        self.root.iconbitmap("2.ico")
        self.root.resizable(False, False)

        self.frame_2 = customtkinter.CTkFrame(self.root, fg_color="#323336")
        self.frame_2.pack(pady=20, padx=30, fill="both", expand=True)


        server_id_label = tk.Label(self.frame_2, text=f"Current server ID: {self.server_id}", bg="#323336", fg="#FFFFFF", font=("Arial", 8, "bold"))
        server_id_label.pack(side="top", pady=10)

        self.timer_label = tk.Label(self.frame_2, text="Next auto bump in: -", bg="#323336", fg="#FFFFFF")
        self.timer_label.pack(side="top", pady=10)

        start_button = customtkinter.CTkButton(self.frame_2, text="Start Bumping", command=self.start_bumping, fg_color="#5a5f69", hover_color="#42474f")
        start_button.pack(side="top", pady=10)


        self.root.mainloop()



    def start_bumping(self):
        self.url = self.base_url + self.server_id
        self.next_bump = time.time() + self.interval
        self.bump_server()

    def bump_server(self):
        webbrowser.open(self.url)
        self.update_timer_label()
        self.next_bump += self.interval
        self.root.after(max(0, int(self.next_bump - time.time()) * 1000), self.bump_server)

    def update_timer_label(self):
        remaining_time = self.next_bump - time.time()
        if remaining_time < 0:
            remaining_time = 0
        remaining_hours, remaining_secs = divmod(remaining_time, 3600)
        remaining_minutes, remaining_seconds = divmod(remaining_secs, 60)
        timer_text = f"Next bump in: {int(remaining_hours):02d}:{int(remaining_minutes):02d}:{int(remaining_seconds):02d}"
        self.timer_label.config(text=timer_text)
        if remaining_time > 0:
            self.root.after(1000, self.update_timer_label)

    def exit_program(self):
        sys.exit()




if __name__ == "__main__":
    server_id_window = ServerIDWindow()
    server_id = server_id_window.server_id
    app = BumpTimerApp(server_id)
