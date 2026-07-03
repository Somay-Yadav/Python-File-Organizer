import customtkinter as ctk


class FolderCard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#1B2434",
            corner_radius=18,
            height=220
        )

        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # ===========================
        # Header
        # ===========================

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(18, 10)
        )

        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="📁  Selected Folder",
            font=("Segoe UI", 20, "bold")
        )

        title.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.browse_button = ctk.CTkButton(
            header,
            text="Browse Folder",
            width=165,
            height=38,
            corner_radius=10,
            font=("Segoe UI", 15, "bold")
        )

        self.browse_button.grid(
            row=0,
            column=1
        )

        # ===========================
        # Path Entry
        # ===========================

        self.folder_entry = ctk.CTkEntry(
            self,
            height=42,
            placeholder_text="No folder selected...",
            state="readonly",
            corner_radius=10
        )

        self.folder_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 18)
        )