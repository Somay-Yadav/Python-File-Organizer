import customtkinter as ctk

from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from pathlib import Path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FileFlowApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        BASE_DIR = Path(__file__).resolve().parent.parent

        self.after(
            100,
            lambda: self.iconbitmap(BASE_DIR / "assets" / "icon.ico")
        )

        self.title("FileFlow - File Organizer")
        self.geometry("1400x850")
        self.minsize(1200, 750)

        self.configure(fg_color="#0E1117")

        # Grid Layout

        self.grid_columnconfigure(0, minsize=300)  # Sidebar
        self.grid_columnconfigure(1, weight=1)     #Dashboard
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Frame

        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Main Area Frame

        self.dashboard = Dashboard(self)
        self.dashboard.grid(row=0, column=1, sticky="nsew")
        self.dashboard.grid_columnconfigure(0, weight=1)
        self.dashboard.grid_rowconfigure(0, weight=1)