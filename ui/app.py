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
        self.grid_columnconfigure(1, weight=1)     # Main area
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Frame

        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Main Area Container Frame
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Initialize pages
        self.pages = {}

        self.pages["dashboard"] = Dashboard(self.main_container)
        self.pages["dashboard"].grid(row=0, column=0, sticky="nsew")

        from ui.stats_page import StatsPage
        from ui.settings_page import SettingsPage
        from ui.about_page import AboutPage

        self.pages["statistics"] = StatsPage(self.main_container, self)
        self.pages["statistics"].grid(row=0, column=0, sticky="nsew")

        self.pages["settings"] = SettingsPage(self.main_container)
        self.pages["settings"].grid(row=0, column=0, sticky="nsew")

        self.pages["about"] = AboutPage(self.main_container)
        self.pages["about"].grid(row=0, column=0, sticky="nsew")

        self.show_page("dashboard")

    def show_page(self, page_name):
        if page_name in self.pages:
            self.pages[page_name].tkraise()
            self.sidebar.set_active_button(page_name)
            
            if page_name == "statistics":
                selected_folder = self.pages["dashboard"].folder_card.selected_folder
                self.pages["statistics"].load_folder_stats(selected_folder)

    def trigger_preview(self):
        self.show_page("dashboard")
        self.pages["dashboard"].folder_card.select_folder()

    def trigger_organize(self):
        self.show_page("dashboard")
        self.pages["dashboard"].action_bar.organize()

    def trigger_undo(self):
        from core.undo import undo_last_operation
        from tkinter import messagebox
        
        res = undo_last_operation()
        if res["status"] == "error":
            messagebox.showwarning("Undo Failed", res["message"])
        else:
            messagebox.showinfo(
                "Undo Complete",
                f"Successfully restored {res['undone']} files.\n"
                f"Failed: {res['failed']}"
            )
            
            current_folder = self.pages["dashboard"].folder_card.selected_folder
            if current_folder:
                self.pages["dashboard"].folder_card.load_folder(current_folder)
            
            self.refresh_last_operation()

    def refresh_last_operation(self):
        self.sidebar.update_last_operation_card()