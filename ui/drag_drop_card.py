import customtkinter as ctk


class DragDropCard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#111827",
            corner_radius=15,
            border_width=1,
            border_color="#30363D",
            height=150
        )
        
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        

        self.icon = ctk.CTkLabel(
            self,
            text="☁",
            font=("Segoe UI Emoji", 42),
            text_color="#8B949E"
        )
        self.icon.grid(row=0, column=0, pady=(25, 5))

        self.title = ctk.CTkLabel(
            self,
            text="Drag & Drop a Folder Here",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        )
        self.title.grid(row=1, column=0)

        self.subtitle = ctk.CTkLabel(
            self,
            text="or click Browse Folder to select",
            font=("Segoe UI", 14),
            text_color="#8B949E"
        )
        self.subtitle.grid(row=2, column=0, pady=(5, 25))