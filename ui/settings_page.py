import json
import customtkinter as ctk
from pathlib import Path
from tkinter import messagebox

class SettingsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#0E1117")
        
        self.base_dir = Path(__file__).resolve().parent.parent
        self.config_path = self.base_dir / "data" / "settings.json"
        self.load_settings()

        self.grid_columnconfigure(0, weight=1, minsize=220) # Categories list
        self.grid_columnconfigure(1, weight=3) # Editor panel
        self.grid_rowconfigure(0, weight=1)

        self.selected_category = None

        self.create_categories_list()
        self.create_editor_panel()

        if self.categories:
            self.select_category(self.categories[0])

    def load_settings(self):
        try:
            with open(self.config_path, "r") as f:
                self.file_types = json.load(f)
        except Exception:
            self.file_types = {}
        self.categories = list(self.file_types.keys())

    def save_settings(self):
        try:
            self.config_path.parent.mkdir(exist_ok=True)
            with open(self.config_path, "w") as f:
                json.dump(self.file_types, f, indent=4)
            messagebox.showinfo("Settings Saved", "Your settings have been saved successfully!")
        except Exception as e:
            messagebox.showerror("Error Saving", f"Could not save settings: {e}")

    def create_categories_list(self):
        self.left_frame = ctk.CTkFrame(self, fg_color="#111827", corner_radius=14, border_width=1, border_color="#2C3645")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.left_frame, text="Categories", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, pady=(15, 10), padx=15, sticky="w")

        self.cat_scroll = ctk.CTkScrollableFrame(self.left_frame, fg_color="transparent")
        self.cat_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.cat_scroll.grid_columnconfigure(0, weight=1)

        self.cat_buttons = {}
        self.render_categories()

        self.add_cat_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.add_cat_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 15))
        self.add_cat_frame.grid_columnconfigure(0, weight=1)

        self.new_cat_entry = ctk.CTkEntry(self.add_cat_frame, placeholder_text="New Category...", font=("Segoe UI", 12))
        self.new_cat_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.add_cat_btn = ctk.CTkButton(self.add_cat_frame, text="+", width=36, font=("Segoe UI", 16, "bold"), command=self.add_category)
        self.add_cat_btn.grid(row=0, column=1)

    def render_categories(self):
        for widget in self.cat_scroll.winfo_children():
            widget.destroy()

        self.cat_buttons = {}
        for cat in self.categories:
            btn = ctk.CTkButton(
                self.cat_scroll,
                text=cat,
                anchor="w",
                font=("Segoe UI", 14),
                height=40,
                fg_color="transparent",
                text_color="#C8D1DC",
                hover_color="#1E293B",
                command=lambda c=cat: self.select_category(c)
            )
            btn.pack(fill="x", pady=2)
            self.cat_buttons[cat] = btn

    def select_category(self, category):
        if self.selected_category and self.selected_category in self.cat_buttons:
            self.cat_buttons[self.selected_category].configure(fg_color="transparent", text_color="#C8D1DC")

        self.selected_category = category
        if category in self.cat_buttons:
            self.cat_buttons[category].configure(fg_color="#2563EB", text_color="white")
        self.editor_title.configure(text=f"Edit Category: {category}")
        self.render_extensions()

    def add_category(self):
        new_cat = self.new_cat_entry.get().strip()
        if not new_cat:
            return
        if new_cat in self.file_types:
            messagebox.showwarning("Duplicate", "Category already exists!")
            return
        self.file_types[new_cat] = []
        self.new_cat_entry.delete(0, "end")
        self.load_settings()
        self.render_categories()
        self.select_category(new_cat)

    def delete_category(self):
        if not self.selected_category:
            return
        if messagebox.askyesno("Delete Category", f"Are you sure you want to delete category '{self.selected_category}'?"):
            del self.file_types[self.selected_category]
            self.load_settings()
            self.render_categories()
            if self.categories:
                self.select_category(self.categories[0])
            else:
                self.selected_category = None
                self.editor_title.configure(text="No Category Selected")
                for w in self.ext_scroll.winfo_children():
                    w.destroy()

    def create_editor_panel(self):
        self.right_frame = ctk.CTkFrame(self, fg_color="#111827", corner_radius=14, border_width=1, border_color="#2C3645")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
        header_frame.grid_columnconfigure(0, weight=1)

        self.editor_title = ctk.CTkLabel(header_frame, text="Edit Category", font=("Segoe UI", 20, "bold"))
        self.editor_title.grid(row=0, column=0, sticky="w")

        self.del_cat_btn = ctk.CTkButton(header_frame, text="Delete Category", fg_color="#EF4444", hover_color="#DC2626", font=("Segoe UI", 12, "bold"), width=120, command=self.delete_category)
        self.del_cat_btn.grid(row=0, column=1)

        self.ext_scroll = ctk.CTkScrollableFrame(self.right_frame, fg_color="transparent")
        self.ext_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)
        self.ext_scroll.grid_columnconfigure(0, weight=1)

        self.add_ext_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.add_ext_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(5, 10))
        self.add_ext_frame.grid_columnconfigure(0, weight=1)

        self.new_ext_entry = ctk.CTkEntry(self.add_ext_frame, placeholder_text="Add extension (e.g. .pdf)...", font=("Segoe UI", 13))
        self.new_ext_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.add_ext_btn = ctk.CTkButton(self.add_ext_frame, text="Add", font=("Segoe UI", 13, "bold"), width=100, command=self.add_extension)
        self.add_ext_btn.grid(row=0, column=1)

        footer = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        footer.grid(row=3, column=0, sticky="ew", padx=20, pady=15)
        footer.grid_columnconfigure(0, weight=1)

        self.save_btn = ctk.CTkButton(footer, text="Save Settings", font=("Segoe UI", 14, "bold"), height=40, fg_color="#10B981", hover_color="#059669", command=self.save_settings)
        self.save_btn.grid(row=0, column=0, sticky="ew")

    def render_extensions(self):
        for widget in self.ext_scroll.winfo_children():
            widget.destroy()

        if not self.selected_category:
            return

        exts = self.file_types.get(self.selected_category, [])
        for ext in exts:
            row = ctk.CTkFrame(self.ext_scroll, fg_color="#1E293B", height=40, corner_radius=8)
            row.pack(fill="x", pady=3)
            row.pack_propagate(False)

            ctk.CTkLabel(row, text=ext, font=("Segoe UI", 14), text_color="white").pack(side="left", padx=15)

            del_btn = ctk.CTkButton(
                row,
                text="Remove",
                fg_color="#475569",
                hover_color="#EF4444",
                font=("Segoe UI", 11, "bold"),
                width=70,
                command=lambda e=ext: self.remove_extension(e)
            )
            del_btn.pack(side="right", padx=10, pady=6)

    def add_extension(self):
        if not self.selected_category:
            return
        ext = self.new_ext_entry.get().strip().lower()
        if not ext:
            return
        if not ext.startswith("."):
            ext = "." + ext
        if ext in self.file_types[self.selected_category]:
            messagebox.showwarning("Duplicate", "Extension already exists in this category!")
            return
        
        for other_cat, other_exts in self.file_types.items():
            if ext in other_exts:
                messagebox.showwarning("Conflict", f"Extension is already mapped to '{other_cat}'!")
                return

        self.file_types[self.selected_category].append(ext)
        self.new_ext_entry.delete(0, "end")
        self.render_extensions()

    def remove_extension(self, ext):
        if not self.selected_category:
            return
        self.file_types[self.selected_category].remove(ext)
        self.render_extensions()
