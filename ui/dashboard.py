import customtkinter as ctk

from ui.folder_card import FolderCard
from ui.drag_drop_card import DragDropCard

def format_size(size):
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

class Dashboard(ctk.CTkFrame):

    def update_preview(self, files):

        # Remove previous rows
        for widget in self.preview_body.winfo_children():
            widget.destroy()

        # Update title
        self.preview_title.configure(
            text=f"Preview ({len(files)} files)"
        )

        self.total_files.configure(
            text=str(len(files))
        )

        for index, file in enumerate(files):

            row = ctk.CTkFrame(
                self.preview_body,
                fg_color="#222B3A" if index % 2 == 0 else "#1C2533",
                corner_radius=8,
                height=40
            )

            row.pack_propagate(False)

            row.pack(
                fill="x",
                padx=5,
                pady=4
            )

            row.grid_columnconfigure(0, minsize=500)
            row.grid_columnconfigure(1, minsize=170)
            row.grid_columnconfigure(2, minsize=120)

            icons = {
                "Image": "🖼️",
                "Document": "📄",
                "Video": "🎬",
                "Audio": "🎵",
                "Archive": "🗜️",
                "Others": "📁"
            }

            name = file["name"]

            if len(name) > 40:
                name = name[:37] + "..."

            # File name
            ctk.CTkLabel(
                row,
                text=f"{icons.get(file['category'],'📁')}  {name}",
                anchor="w",
                justify="left",
                font=("Segoe UI", 14),
                width=350
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=(15,0)
            )

            badge_bg = {
                "Image": "#163A29",
                "Document": "#3D2B0B",
                "Video": "#102C5A",
                "Audio": "#34124F",
                "Archive": "#4A2210",
                "Others": "#303A4B"
            }

            badge_text = {
                "Image": "#34D399",
                "Document": "#FBBF24",
                "Video": "#60A5FA",
                "Audio": "#C084FC",
                "Archive": "#FB923C",
                "Others": "#94A3B8"
            }

            # Category (temporary)
            badge = ctk.CTkFrame(
                row,
                fg_color=badge_bg.get(file["category"], "#475569"),
                width=110,
                height=28,
                corner_radius=8
            )

            badge.grid(row=0, column=1)
            badge.grid_propagate(False)

            ctk.CTkLabel(
                badge,
                text=file["category"],
                text_color=badge_text.get(file["category"], "#FFFFFF"),
                font=("Segoe UI", 12, "bold"),
                fg_color="transparent"
            ).place(relx=0.5, rely=0.5, anchor="center")

            # Size
            ctk.CTkLabel(
                row,
                text=format_size(file["size"]),
                font=("Segoe UI", 13)
            ).grid(
                row=0,
                column=2,
                padx=(0,15)
            )

            row.pack_propagate(False)

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

        self.folder_card = FolderCard(
            self, 
            dashboard=self
        )

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
            height=50,
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
            font=("Segoe UI",15,"bold"),
            anchor="w"
        ).grid(row=0,column=0, sticky="w",padx=20,pady=10)

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

        self.preview_body = ctk.CTkScrollableFrame(
            self.preview_card,
            fg_color="transparent",
            corner_radius=0
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