import customtkinter as ctk

from ui.folder_card import FolderCard
from ui.drag_drop_card import DragDropCard

class Dashboard(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#0E1117"
        )

        self.grid_rowconfigure(0, minsize=105)
        self.grid_rowconfigure(1, minsize=180)
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

        # Layout
        self.grid_rowconfigure(0, weight=0)  # Folder card
        self.grid_rowconfigure(1, weight=0)  # Drag & Drop
        self.grid_rowconfigure(2, weight=1)  # Preview section
        self.grid_rowconfigure(3, weight=0)  # Bottom action cards
        self.grid_rowconfigure(4, weight=0)  # Status bar

        # ---------- Folder Card ---------- #

        self.folder_card = FolderCard(self)

        self.folder_card.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=(25,20)
        )

        # --------- Drag And Drop ---------- #

        self.drag_drop = DragDropCard(self)

        self.drag_drop.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=(0,20)
        )

        # ==========================
        # Preview + Statistics Frame
        # ==========================

        self.content_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.content_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=25,
            pady=(0,25)
        )

        self.content_frame.grid_columnconfigure(0, weight=5)
        self.content_frame.grid_columnconfigure(1, weight=2)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.preview_card = ctk.CTkFrame(
            self.content_frame,
            fg_color="#1B2434",
            corner_radius=18
        )

        self.preview_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,10),
            pady=0
        )

        self.preview_card.grid_columnconfigure(0, weight=1)
        self.preview_card.grid_rowconfigure(2, weight=1)

        self.preview_title = ctk.CTkLabel(
            self.preview_card,
            text="Preview (0 files)",
            font=("Segoe UI", 22, "bold")
        )

        self.preview_title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20,15)
        )

        self.table_header = ctk.CTkFrame(
            self.preview_card,
            fg_color="#273246",
            height=45,
            corner_radius=10
        )

        self.table_header.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20
        )

        self.table_header.grid_columnconfigure(0, weight=3)
        self.table_header.grid_columnconfigure(1, weight=2)
        self.table_header.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(
            self.table_header,
            text="File Name",
            font=("Segoe UI",15,"bold")
        ).grid(row=0,column=0,pady=10)

        ctk.CTkLabel(
            self.table_header,
            text="Category",
            font=("Segoe UI",15,"bold")
        ).grid(row=0,column=1,pady=10)

        ctk.CTkLabel(
            self.table_header,
            text="Size",
            font=("Segoe UI",15,"bold")
        ).grid(row=0,column=2,pady=10)

        self.preview_body = ctk.CTkFrame(
            self.preview_card,
            fg_color="transparent",
            height=320
        )

        self.preview_body.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(15,20)
        )

        self.stats_card = ctk.CTkFrame(
            self.content_frame,
            fg_color="#1B2434",
            corner_radius=18
        )

        self.stats_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10,0),
            pady=0
        )

        self.stats_card.grid_columnconfigure(0, weight=1)

        self.stats_title = ctk.CTkLabel(
            self.stats_card,
            text="Statistics",
            font=("Segoe UI", 24, "bold")
        )

        self.stats_title.pack(
            anchor="w",
            padx=25,
            pady=(20,10)
        )

        self.chart_placeholder = ctk.CTkFrame(
            self.stats_card,
            width=180,
            height=180,
            fg_color="#263449",
            corner_radius=90
        )

        self.chart_placeholder.pack(pady=10)

        self.chart_placeholder.pack_propagate(False)

        ctk.CTkLabel(
            self.chart_placeholder,
            text="Pie\nChart",
            font=("Segoe UI",18,"bold")
        ).pack(expand=True)


        stats = [
            ("Images",0),
            ("Documents",0),
            ("Videos",0),
            ("Audio",0),
            ("Archives",0),
            ("Others",0)
        ]

        for name,count in stats:
            row = ctk.CTkFrame(
                self.stats_card,
                fg_color="transparent"
            )

            row.pack(fill="x", padx=25, pady=3)

            ctk.CTkLabel(
                row,
                text=name
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=str(count),
                font=("Segoe UI",14,"bold")
            ).pack(side="right")


        ctk.CTkLabel(
            self.stats_card,
            text="",
        ).pack(pady=8)

        ctk.CTkLabel(
            self.stats_card,
            text="Total Files",
            font=("Segoe UI",16)
        ).pack()

        self.total_files = ctk.CTkLabel(
            self.stats_card,
            text="0",
            font=("Segoe UI",28,"bold"),
            text_color="#3B82F6"
        )

        self.total_files.pack(pady=(0,20))