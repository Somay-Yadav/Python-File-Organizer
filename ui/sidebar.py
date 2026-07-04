import customtkinter as ctk
import os
from PIL import Image, ImageOps
from pathlib import Path

def load_white_icon(path, size=(22, 22)):
    image = Image.open(path).convert("RGBA")

    # Invert the RGB channels
    rgb = image.convert("RGB")
    rgb = ImageOps.invert(rgb)

    # Restore the original transparency
    image = Image.merge("RGBA", (*rgb.split(), image.getchannel("A")))

    return ctk.CTkImage(
        light_image=image,
        dark_image=image,
        size=size
    )

class Sidebar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            width=300,
            fg_color="#111827",
            border_width=1,
            border_color="#374151",
            corner_radius=0
        )

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ICON_DIR = os.path.join(BASE_DIR, "assets", "icons")

        self.logo = ctk.CTkImage(
            light_image=Image.open(Path(BASE_DIR) / "assets" / "logo.png"),
            dark_image=Image.open(Path(BASE_DIR) / "assets" / "logo.png"),
            size=(46, 46)
        )

        self.icons = {
            "dashboard": load_white_icon(os.path.join(ICON_DIR, "dashboard.png")),
            "preview": load_white_icon(os.path.join(ICON_DIR, "preview.png")),
            "organize": load_white_icon(os.path.join(ICON_DIR, "organize.png")),
            "statistics": load_white_icon(os.path.join(ICON_DIR, "statistics.png")),
            "undo": load_white_icon(os.path.join(ICON_DIR, "undo.png")),
            "settings": load_white_icon(os.path.join(ICON_DIR, "settings.png")),
            "about": load_white_icon(os.path.join(ICON_DIR, "about.png")),
        }
        self.app = master
        self.grid_propagate(False)

        self.grid_rowconfigure(0, weight=0) # Logo
        self.grid_rowconfigure(1, weight=0) # Navigation
        self.grid_rowconfigure(2, weight=1) # Flexible Space
        self.grid_rowconfigure(3, weight=0) # Bottom Card

        self.grid_columnconfigure(0, weight=1)

        self.build_ui()
        self.update_last_operation_card()

    def build_ui(self):

        # ===========================
        # Logo Section
        # ===========================

        logo_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        logo_frame.grid(
            row = 0,
            column = 0,
            sticky = "ew",
            padx = 22,
            pady = (25, 20)
        )

        title = ctk.CTkLabel(
            logo_frame,
            image=self.logo,
            text="  FileFlow",
            compound="left",
            font=("Segoe UI", 30, "bold"),
            anchor="w"
        )

        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            logo_frame,
            text="Organize your files smartly",
            font=("Segoe UI", 14),
            text_color="#94A3B8",
            anchor="w"
        )

        subtitle.pack(anchor="w")

        # ===========================
        # Navigation
        # ===========================

        nav = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        nav.grid(
            row = 1,
            column = 0,
            sticky = "ew",
            padx = 18
        )

        self.buttons = {}

        self.dashboard_btn = self.create_button(
            nav,
            "Dashboard",
            self.icons["dashboard"],
            command=lambda: self.app.show_page("dashboard"),
            active=True
        )
        self.buttons["dashboard"] = self.dashboard_btn

        self.preview_btn = self.create_button(
            nav,
            "Preview",
            self.icons["preview"],
            command=lambda: self.app.trigger_preview()
        )

        self.organize_btn = self.create_button(
            nav,
            "Organize",
            self.icons["organize"],
            command=lambda: self.app.trigger_organize()
        )

        self.statistics_btn = self.create_button(
            nav,
            "Statistics",
            self.icons["statistics"],
            command=lambda: self.app.show_page("statistics")
        )
        self.buttons["statistics"] = self.statistics_btn

        self.undo_btn = self.create_button(
            nav,
            "Undo",
            self.icons["undo"],
            command=lambda: self.app.trigger_undo()
        )

        self.settings_btn = self.create_button(
            nav,
            "Settings",
            self.icons["settings"],
            command=lambda: self.app.show_page("settings")
        )
        self.buttons["settings"] = self.settings_btn

        self.about_btn = self.create_button(
            nav,
            "About",
            self.icons["about"],
            command=lambda: self.app.show_page("about")
        )
        self.buttons["about"] = self.about_btn

        # ===========================
        # Last Operation Card
        # ===========================

        card = ctk.CTkFrame(
            self,
            height=190,
            fg_color="#1E293B",
            corner_radius=18,
            border_width=1,
            border_color="#374151"
        )

        card.grid(
            row=3,
            column=0,
            padx=18,
            pady=18,
            sticky="ew"
        )

        card.grid_propagate(False)

        ctk.CTkLabel(
            card,
            text="Last Operation",
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 5)
        )

        self.last_op_status = ctk.CTkLabel(
            card,
            text="No recent activity",
            font=("Segoe UI", 13),
            text_color="#94A3B8",
            justify="left",
            anchor="w",
            wraplength=200
        )
        self.last_op_status.pack(
            anchor="w",
            padx=18,
            pady=(0, 5)
        )

        self.view_details_btn = ctk.CTkButton(
            card,
            text="View Details",
            font=("Segoe UI", 14, "bold"),
            height=38,
            corner_radius=10,
            fg_color="#111827",
            border_width=1,
            border_color="#122B71",
            hover_color="#1D4ED8",
            command=self.view_last_op_details
        )
        self.view_details_btn.pack(
            fill="x",
            padx=18,
            pady=12
        )

    def set_active_button(self, page_name):
        for name, btn in self.buttons.items():
            if name == page_name:
                btn.configure(fg_color="#2563EB", hover_color="#122B71")
            else:
                btn.configure(fg_color="transparent", hover_color="#1E293B")

    def update_last_operation_card(self):
        from core.undo import get_last_operation
        last_op = get_last_operation()
        if not last_op:
            self.last_op_status.configure(text="No recent activity")
            return
        
        folder_name = os.path.basename(last_op["folder"])
        if not folder_name:
            folder_name = last_op["folder"]
        
        num_moved = len(last_op["moves"])
        text = f"Folder: {folder_name}\nMoved: {num_moved} files\nTime: {last_op['timestamp']}"
        self.last_op_status.configure(text=text)

    def view_last_op_details(self):
        from core.undo import get_last_operation
        from tkinter import messagebox
        last_op = get_last_operation()
        if not last_op:
            messagebox.showinfo("No Activity", "There is no recent activity to show details for.")
            return
        
        details = f"Folder: {last_op['folder']}\n"
        details += f"Time: {last_op['timestamp']}\n\n"
        details += "Files Moved:\n"
        for move in last_op["moves"][:15]:
            src_name = os.path.basename(move["source"])
            dest_cat = os.path.basename(os.path.dirname(move["destination"]))
            details += f"• {src_name} -> {dest_cat}\n"
        
        if len(last_op["moves"]) > 15:
            details += f"... and {len(last_op['moves']) - 15} more files."
            
        messagebox.showinfo("Last Operation Details", details)

    def create_button(self, parent, text, icon, command=None, active=False):

        color = "#2563EB" if active else "transparent"

        button = ctk.CTkButton(
            parent,
            text=text,
            image=icon,
            height=56,
            corner_radius=15,
            fg_color=color,
            hover_color="#122B71" if active else "#1E293B",
            anchor="w",
            font=("Segoe UI", 18),
            border_width=0,
            command=command
        )

        button.pack(fill="x", pady=6)

        return button