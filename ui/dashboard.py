import customtkinter as ctk

from ui.folder_card import FolderCard
from ui.drag_drop_card import DragDropCard
from ui.action_bar import ActionBar
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        self.preview_count.configure(
            text=f"({len(files)} files)"
        )

        # ---------------- Statistics ---------------- #

        counts = {
            "Images": 0,
            "Documents": 0,
            "Videos": 0,
            "Audio": 0,
            "Archives": 0,
            "Applications": 0,
            "Others": 0
        }

        mapping = {
            "Image": "Images",
            "Document": "Documents",
            "Video": "Videos",
            "Audio": "Audio",
            "Archive": "Archives",
            "Application": "Applications",
            "Others": "Others"
        }

        total_size = 0

        for f in files:
            category = mapping.get(f["category"], "Others")
            counts[category] += 1
            total_size += f["size"]

        for category, label in self.stat_labels.items():
            label.configure(text=str(counts[category]))

        self.action_bar.size_value.configure(
            text=format_size(total_size)
        )

        # ---------------- Action Bar ---------------- #

        self.action_bar.files_value.configure(
            text=str(len(files))
        )

        used_categories = sum(
            1 for count in counts.values() if count > 0
        )

        self.action_bar.categories_value.configure(
            text=str(used_categories)
        )

        self.action_bar.size_value.configure(
            text=format_size(total_size)
        )

        values = list(counts.values())

        colors = [
            "#22C55E",  # Images
            "#FACC15",  # Documents
            "#3B82F6",  # Videos
            "#A855F7",  # Audio
            "#F97316",  # Archives
            "#EF4444",  # Applications
            "#94A3B8"   # Others
        ]

        self.ax.clear()

        self.ax.pie(
            values,
            colors=colors,
            startangle=90,
            wedgeprops=dict(width=0.38, edgecolor="#1B2434")
        )

        self.ax.set_aspect("equal")
        self.ax.set_facecolor("#1B2434")

        self.canvas.draw()

        for index, file in enumerate(files):

            row = ctk.CTkFrame(
                self.preview_body,
                fg_color="#202938" if index % 2 == 0 else "#1B2434",
                corner_radius=0,
                height=36
            )

            row.pack_propagate(False)

            row.pack(
                fill="x",
                padx=0,
                pady=0
            )

            ctk.CTkFrame(
                self.preview_body,
                height=1,
                fg_color="#313B4A",
                corner_radius=0
            ).pack(fill="x")

            row.grid_columnconfigure(0, minsize=500)
            row.grid_columnconfigure(1, minsize=170)
            row.grid_columnconfigure(2, weight=1)

            icons = {
                "Image": "🖼️",
                "Document": "📄",
                "Video": "🎬",
                "Audio": "🎵",
                "Archive": "🗜️",
                "Application": "🖥️",
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
                padx=(18,10)
            )

            badge_bg = {
                "Image": "#163A29",
                "Document": "#3D2B0B",
                "Video": "#102C5A",
                "Audio": "#34124F",
                "Archive": "#4A2210",
                "Application": "#4A1E1E",
                "Others": "#303A4B"
            }

            badge_text = {
                "Image": "#34D399",
                "Document": "#FBBF24",
                "Video": "#60A5FA",
                "Audio": "#C084FC",
                "Archive": "#FB923C",
                "Application": "#EF4444",
                "Others": "#94A3B8"
            }

            # Category (temporary)
            badge = ctk.CTkFrame(
                row,
                fg_color=badge_bg.get(file["category"], "#475569"),
                width=105,
                height=24,
                corner_radius=8
            )

            badge.grid(row=0, column=1, padx=10)
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
                font=("Segoe UI", 13),
                anchor="e",
                justify="right"
            ).grid(
                row=0,
                column=2,
                sticky="e",
                padx=(0,18)
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

        self.action_bar = ActionBar(self, self)

        self.action_bar.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=(0, 12)
        )

        

        self.content_frame.grid_columnconfigure(0, weight=5)
        self.content_frame.grid_columnconfigure(1, weight=2)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.preview_card = ctk.CTkFrame(
            self.content_frame,
            fg_color="#101722",
            corner_radius=14,
            border_width=1,
            border_color="#2C3645"
        )

        self.preview_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,10),
            pady=(38,0)
        )

        self.preview_card.grid_columnconfigure(0, weight=1)
        self.preview_card.grid_rowconfigure(2, weight=1)

        self.preview_title = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )

        self.preview_title.grid(
            row=0,
            column=0,
            sticky="nw",
            padx=18,
            pady=(0,8)
        )

        self.preview_label = ctk.CTkLabel(
            self.preview_title,
            text="Preview ",
            font=("Segoe UI",22,"bold")
        )

        self.preview_label.pack(side="left")

        self.preview_count = ctk.CTkLabel(
            self.preview_title,
            text="(0 files)",
            font=("Segoe UI",22,"bold"),
            text_color="#3B82F6"
        )

        self.preview_count.pack(side="left")

        self.table_header = ctk.CTkFrame(
            self.preview_card,
            fg_color="#273246",
            height=50,
            corner_radius=0
        )

        self.table_header.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        ctk.CTkFrame(
            self.preview_card,
            height=1,
            fg_color="#2C3645",
            corner_radius=0
        ).grid(
            row=2,
            column=0,
            sticky="ew"
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

        self.preview_container = ctk.CTkFrame(
            self.preview_card,
            fg_color="transparent",
            corner_radius=0
        )

        self.preview_container.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=0,
            pady=0
        )

        self.preview_body = ctk.CTkScrollableFrame(
            self.preview_container,
            fg_color="transparent",
            corner_radius=0
        )

        self.preview_body.pack(
            fill="both",
            expand=True
        )

        self.stats_card = ctk.CTkFrame(
            self.content_frame,
            fg_color="#1B2434",
            corner_radius=18,
            border_width=1,
            border_color="#2C3645"
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
            pady=(18,5)
        )

        self.chart_frame = ctk.CTkFrame(
            self.stats_card,
            fg_color="transparent",
            height=170
        )

        self.chart_frame.pack(fill="x", padx=15, pady=(0,1))

        self.figure = Figure(
            figsize=(2.5,2.5),
            dpi=100,
            facecolor="#1B2434"
        )

        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self.chart_frame
        )

        self.canvas.get_tk_widget().pack(fill="both", expand=True)


        self.stat_labels = {}

        stats = [
            ("Images", "#22C55E"),
            ("Documents", "#FACC15"),
            ("Videos", "#3B82F6"),
            ("Audio", "#A855F7"),
            ("Archives", "#F97316"),
            ("Applications", "#EF4444"),
            ("Others", "#94A3B8")
        ]

        for name, color in stats:

            row = ctk.CTkFrame(
                self.stats_card,
                fg_color="transparent"
            )
            row.pack(fill="x", padx=25, pady=1)

            left = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )
            left.pack(side="left")

            ctk.CTkLabel(
                left,
                text="●",
                text_color=color,
                font=("Segoe UI",16)
            ).pack(side="left")

            ctk.CTkLabel(
                left,
                text=name,
                font=("Segoe UI",14)
            ).pack(side="left", padx=6)

            value = ctk.CTkLabel(
                row,
                text="0",
                font=("Segoe UI",14,"bold")
            )

            value.pack(side="right")

            self.stat_labels[name] = value


        