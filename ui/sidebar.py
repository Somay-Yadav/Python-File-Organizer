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

        self.icons = {
            "dashboard": load_white_icon(os.path.join(ICON_DIR, "dashboard.png")),
            "preview": load_white_icon(os.path.join(ICON_DIR, "preview.png")),
            "organize": load_white_icon(os.path.join(ICON_DIR, "organize.png")),
            "statistics": load_white_icon(os.path.join(ICON_DIR, "statistics.png")),
            "undo": load_white_icon(os.path.join(ICON_DIR, "undo.png")),
            "settings": load_white_icon(os.path.join(ICON_DIR, "settings.png")),
            "about": load_white_icon(os.path.join(ICON_DIR, "about.png")),
        }

        self.grid_propagate(False)

        self.grid_rowconfigure(0, weight=0) # Logo
        self.grid_rowconfigure(1, weight=0) # Navigation
        self.grid_rowconfigure(2, weight=1) # Flexible Space
        self.grid_rowconfigure(3, weight=0) # Bottom Card

        self.grid_columnconfigure(0, weight=1)

        self.build_ui()

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
            text="📂 FileFlow",
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

        self.dashboard = self.create_button(
            nav,
            "Dashboard",
            self.icons["dashboard"],
            active=True
        )

        self.preview = self.create_button(
            nav,
            "Preview",
            self.icons["preview"]
        )

        self.organize = self.create_button(
            nav,
            "Organize",
            self.icons["organize"]
        )

        self.statistics = self.create_button(
            nav,
            "Statistics",
            self.icons["statistics"]
        )

        self.undo = self.create_button(
            nav,
            "Undo",
            self.icons["undo"]
        )

        self.settings = self.create_button(
            nav,
            "Settings",
            self.icons["settings"]
        )

        self.about = self.create_button(
            nav,
            "About",
            self.icons["about"]
        )

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

        ctk.CTkLabel(
            card,
            text="No recent activity",
            font=("Segoe UI", 14),
            text_color="#94A3B8"
        ).pack(
            anchor="w",
            padx=18
        )

        ctk.CTkButton(
            card,
            text="View Details",
            font=("Segoe UI", 14, "bold"),
            height=38,
            corner_radius=10,
            fg_color="#111827",
            border_width=1,
            border_color="#122B71",
            hover_color="#1D4ED8"
        ).pack(
            fill="x",
            padx=18,
            pady=18
        )

    def create_button(self, parent, text, icon, active=False):

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
            border_width=0
        )

        button.pack(fill="x", pady=6)

        return button