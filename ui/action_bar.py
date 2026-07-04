import customtkinter as ctk
from PIL import Image
from pathlib import Path

from core.organizer import organize_files
from tkinter import messagebox



def load_white_icon(path, size=(22, 22)):
    img = Image.open(path).convert("RGBA")

    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a > 0:  # keep transparency
                pixels[x, y] = (255, 255, 255, a)

    return ctk.CTkImage(light_image=img, dark_image=img, size=size)

class ActionBar(ctk.CTkFrame):

    def preview(self):
        folder = self.dashboard.folder_card.selected_folder
        if folder:
            self.dashboard.folder_card.load_folder(folder)
        else:
            messagebox.showwarning(
                "No Folder Selected",
                "Please select a folder first."
            )

    def organize(self):

        folder = self.dashboard.folder_card.selected_folder

        if not folder:
            messagebox.showwarning(
                "No Folder Selected",
                "Please select a folder first."
            )
            return

        stats = organize_files(folder)

        messagebox.showinfo(
            "Organization Complete",
            f"Moved: {stats['moved']}\n"
            f"Skipped: {stats['skipped']}"
        )

        # Refresh dashboard
        self.dashboard.folder_card.load_folder(folder)

        # Update sidebar last operation card
        app = self.dashboard.master
        while app and not hasattr(app, "refresh_last_operation"):
            app = getattr(app, "master", None)
        if app and hasattr(app, "refresh_last_operation"):
            app.refresh_last_operation()


    def undo(self):
        app = self.dashboard.master
        while app and not hasattr(app, "trigger_undo"):
            app = getattr(app, "master", None)
        if app and hasattr(app, "trigger_undo"):
            app.trigger_undo()

    def __init__(self, master, dashboard):
        super().__init__(
            master,
            fg_color="transparent",
            height=70
        )
        
        self.dashboard = dashboard
        self.selected_folder = None

        BASE_DIR = Path(__file__).resolve().parent.parent

        self.eye_icon = load_white_icon(
            BASE_DIR / "assets/icons/preview.png"
        )

        self.folder_icon = load_white_icon(
            BASE_DIR / "assets/icons/folder.png"
        )

        self.undo_icon = load_white_icon(
            BASE_DIR / "assets/icons/undo.png"
        )

        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.files_card, self.files_value = self.create_info_card(
            "Files",
            "0"
        )

        self.categories_card, self.categories_value = self.create_info_card(
            "Categories",
            "0"
        )

        self.size_card, self.size_value = self.create_info_card(
            "Total Size",
            "0 B"
        )

        self.files_card.grid(
            row=0,
            column=0,
            padx=(0,8),
            sticky="ew"
        )

        self.categories_card.grid(
            row=0,
            column=1,
            padx=8,
            sticky="ew"
        )

        self.size_card.grid(
            row=0,
            column=2,
            padx=8,
            sticky="ew"
        )

        self.preview_btn = self.create_button(
            "Preview",
            self.eye_icon,
            "#2563EB",
            "#1D4ED8"
        )

        self.organize_btn = self.create_button(
            "Organize",
            self.folder_icon,
            "#16A34A",
            "#15803D"
        )

        self.undo_btn = self.create_button(
            "Undo",
            self.undo_icon,
            "#DC2626",
            "#B91C1C"
        )



        self.preview_btn.configure(command=self.preview)

        self.organize_btn.configure(command=self.organize)

        self.undo_btn.configure(command=self.undo)

        self.preview_btn.grid(
            row=0,
            column=3,
            padx=(20,8),
            sticky="ew"
        )

        self.organize_btn.grid(
            row=0,
            column=4,
            padx=8,
            sticky="ew"
        )

        self.undo_btn.grid(
            row=0,
            column=5,
            padx=(8,0),
            sticky="ew"
        )

    def create_info_card(self, title, value):

        card = ctk.CTkFrame(
            self,
            fg_color="#1B2434",
            corner_radius=14,
            border_width=1,
            border_color="#2C3645",
            height=70
        )

        card.grid_propagate(False)
        card.pack_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 12)
        )

        title_label.pack(pady=(10, 1))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 18, "bold")
        )

        value_label.pack()

        return card, value_label
    
    def create_button(self, text, image, color, hover):
        return ctk.CTkButton(
            self,
            text=text,
            image=image,
            compound="left",
            fg_color=color,
            hover_color=hover,
            corner_radius=12,
            height=58,
            font=("Segoe UI", 15, "bold"),
            border_spacing=10
        )
    
    def update_stats(self, files, categories, total_size):

        self.files_value.configure(
            text=str(files)
        )

        self.categories_value.configure(
            text=str(categories)
        )

        self.size_value.configure(
            text=total_size
        )
