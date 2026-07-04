import customtkinter as ctk

class AboutPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#0E1117")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        container = ctk.CTkFrame(self, fg_color="#111827", corner_radius=18, border_width=1, border_color="#2C3645")
        container.grid(row=0, column=0, padx=40, pady=40)
        
        logo_lbl = ctk.CTkLabel(container, text="📂", font=("Segoe UI", 72))
        logo_lbl.pack(pady=(30, 10))

        title_lbl = ctk.CTkLabel(container, text="FileFlow", font=("Segoe UI", 28, "bold"), text_color="white")
        title_lbl.pack(pady=5)

        version_lbl = ctk.CTkLabel(container, text="Version 3.1.0", font=("Segoe UI", 14), text_color="#3B82F6")
        version_lbl.pack(pady=2)

        desc_lbl = ctk.CTkLabel(
            container, 
            text="A modern desktop application to organize messy folders in seconds.\n"
                 "Perfect for Downloads, Desktop, Documents, and other cluttered folders.",
            font=("Segoe UI", 14), 
            text_color="#94A3B8",
            justify="center"
        )
        desc_lbl.pack(pady=15, padx=30)

        dev_frame = ctk.CTkFrame(container, fg_color="#1E293B", corner_radius=10)
        dev_frame.pack(fill="x", padx=30, pady=15)

        ctk.CTkLabel(dev_frame, text="Author: Somay Yadav", font=("Segoe UI", 13, "bold"), text_color="white").pack(pady=(8, 2))
        ctk.CTkLabel(dev_frame, text="License: MIT License", font=("Segoe UI", 12), text_color="#94A3B8").pack(pady=(0, 8))

        copyright_lbl = ctk.CTkLabel(container, text="© 2026 Somay Yadav. All rights reserved.", font=("Segoe UI", 11), text_color="#475569")
        copyright_lbl.pack(pady=(10, 25))
