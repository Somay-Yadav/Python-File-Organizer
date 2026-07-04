import customtkinter as ctk

from core.folder_manager import FolderManager
from core.scanner import FileScanner

class FolderCard(ctk.CTkFrame):
    def __init__(self, master, dashboard):
        super().__init__(
            master,
            fg_color="transparent",
            corner_radius=18,
            height=140
        )

        self.dashboard = dashboard

        self.selected_folder = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

        ctk.CTkLabel(
            self,
            text="Selected Folder",
            font=("Segoe UI", 20, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(0,8)
        )

        
        controls = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        controls.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0,10)
        )

        controls.grid_columnconfigure(0, weight=1)

        self.browse_button = ctk.CTkButton(
            controls,
            text="Browse Folder",
            width=180,
            height=46,
            corner_radius=10,
            font=("Segoe UI", 15, "bold")
        )

        self.browse_button.configure(
            command=self.select_folder
        )


        # ===========================
        # Path Display
        # ===========================

        self.folder_entry = ctk.CTkFrame(
            controls,
            fg_color="#162233",
            border_width=1,
            border_color="#304155",
            corner_radius=10,
            height=46
        )

        self.folder_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0,15)
        )

        self.browse_button.grid(
            row=0,
            column=1
        )

        self.folder_entry.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.folder_entry,
            text="📁",
            font=("Segoe UI", 18)
        ).grid(
            row=0,
            column=0,
            padx=(15,8),
            pady=10
        )

        self.path_label = ctk.CTkLabel(
            self.folder_entry,
            text="No folder selected...",
            anchor="w",
            font=("Segoe UI", 14),
            text_color="#C8D1DC"
        )

        self.path_label.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(0,15)
        )


    def select_folder(self):

        folder = FolderManager.browse_folder()

        if not folder:
            return

        self.load_folder(folder)

    def load_folder(self, folder):

        self.selected_folder = folder

        display_path = folder

        if len(display_path) > 70:
            display_path = "..." + display_path[-67:]

        self.path_label.configure(text=display_path)

        files = FileScanner.scan(folder)

        self.dashboard.update_preview(files)