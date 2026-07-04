import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from core.scanner import FileScanner

def format_size(size):
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

class StatsPage(ctk.CTkFrame):
    def __init__(self, master, app=None):
        super().__init__(master, fg_color="#0E1117")
        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=20)
        self.header_title = ctk.CTkLabel(self.header_frame, text="Folder Statistics & Analytics", font=("Segoe UI", 24, "bold"))
        self.header_title.pack(anchor="w")

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 20))
        self.content_frame.grid_columnconfigure((0, 1), weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.show_no_folder()

    def load_folder_stats(self, folder_path):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not folder_path:
            self.show_no_folder()
            return

        files = FileScanner.scan(folder_path)
        if not files:
            self.show_empty_folder()
            return

        categories = {}
        total_size = 0
        total_files = len(files)

        for f in files:
            cat = f["category"]
            if cat not in categories:
                categories[cat] = {"count": 0, "size": 0}
            categories[cat]["count"] += 1
            categories[cat]["size"] += f["size"]
            total_size += f["size"]

        # Left panel: Metrics table
        left_panel = ctk.CTkFrame(self.content_frame, fg_color="#111827", corner_radius=14, border_width=1, border_color="#2C3645")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(left_panel, text="Category Details", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, pady=15, padx=20, sticky="w")

        table_scroll = ctk.CTkScrollableFrame(left_panel, fg_color="transparent")
        table_scroll.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        table_scroll.grid_columnconfigure((0, 1, 2, 3), weight=1)

        headers = ["Category", "Files Count", "Total Size", "Percentage"]
        for col_idx, h in enumerate(headers):
            lbl = ctk.CTkLabel(table_scroll, text=h, font=("Segoe UI", 12, "bold"), text_color="#94A3B8")
            lbl.grid(row=0, column=col_idx, pady=5, sticky="w" if col_idx == 0 else "e")

        row_idx = 1
        for cat, data in categories.items():
            pct = (data["size"] / total_size * 100) if total_size > 0 else 0
            
            lbl1 = ctk.CTkLabel(table_scroll, text=cat, font=("Segoe UI", 13), text_color="white")
            lbl1.grid(row=row_idx, column=0, pady=6, sticky="w")
            
            lbl2 = ctk.CTkLabel(table_scroll, text=str(data["count"]), font=("Segoe UI", 13), text_color="#C8D1DC")
            lbl2.grid(row=row_idx, column=1, pady=6, sticky="e")
            
            lbl3 = ctk.CTkLabel(table_scroll, text=format_size(data["size"]), font=("Segoe UI", 13), text_color="#C8D1DC")
            lbl3.grid(row=row_idx, column=2, pady=6, sticky="e")
            
            lbl4 = ctk.CTkLabel(table_scroll, text=f"{pct:.1f}%", font=("Segoe UI", 13, "bold"), text_color="#3B82F6")
            lbl4.grid(row=row_idx, column=3, pady=6, sticky="e")
            
            row_idx += 1

        summary_frame = ctk.CTkFrame(left_panel, fg_color="#1E293B", corner_radius=10)
        summary_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=15)
        summary_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkLabel(summary_frame, text=f"Total Files: {total_files}", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, pady=10, padx=15, sticky="w")
        ctk.CTkLabel(summary_frame, text=f"Folder Size: {format_size(total_size)}", font=("Segoe UI", 14, "bold")).grid(row=0, column=1, pady=10, padx=15, sticky="e")

        # Right panel: Charts
        right_panel = ctk.CTkFrame(self.content_frame, fg_color="#111827", corner_radius=14, border_width=1, border_color="#2C3645")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(right_panel, text="Size Distribution", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, pady=15, padx=20, sticky="w")

        chart_container = ctk.CTkFrame(right_panel, fg_color="transparent")
        chart_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))

        fig = Figure(figsize=(4, 4), dpi=100, facecolor="#111827")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#111827")

        sorted_cats = sorted(categories.items(), key=lambda x: x[1]["size"], reverse=True)
        names = [x[0] for x in sorted_cats]
        sizes_mb = [x[1]["size"] / (1024*1024) for x in sorted_cats]

        bars = ax.barh(names, sizes_mb, color="#2563EB", edgecolor="#2C3645")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#2C3645')
        ax.spines['bottom'].set_color('#2C3645')
        ax.tick_params(colors='white', labelsize=9)
        ax.set_xlabel("Size (MB)", color="white", fontsize=10)

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.05 * (max(sizes_mb) + 1), bar.get_y() + bar.get_height()/2, f'{width:.1f} MB', 
                    va='center', ha='left', color='white', fontsize=8)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_container)
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_no_folder(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        frame = ctk.CTkFrame(self.content_frame, fg_color="#111827", corner_radius=14, border_width=1, border_color="#2C3645")
        frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        container = ctk.CTkFrame(frame, fg_color="transparent")
        container.grid(row=0, column=0)

        ctk.CTkLabel(container, text="📊", font=("Segoe UI", 64)).pack(pady=10)
        ctk.CTkLabel(container, text="No Folder Selected", font=("Segoe UI", 20, "bold"), text_color="white").pack(pady=5)
        ctk.CTkLabel(container, text="Please select a folder in the Dashboard first to view detailed statistics.", font=("Segoe UI", 14), text_color="#94A3B8").pack(pady=5)

    def show_empty_folder(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        frame = ctk.CTkFrame(self.content_frame, fg_color="#111827", corner_radius=14, border_width=1, border_color="#2C3645")
        frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        container = ctk.CTkFrame(frame, fg_color="transparent")
        container.grid(row=0, column=0)

        ctk.CTkLabel(container, text="📂", font=("Segoe UI", 64)).pack(pady=10)
        ctk.CTkLabel(container, text="Folder is Empty", font=("Segoe UI", 20, "bold"), text_color="white").pack(pady=5)
        ctk.CTkLabel(container, text="There are no files to analyze in this directory.", font=("Segoe UI", 14), text_color="#94A3B8").pack(pady=5)
