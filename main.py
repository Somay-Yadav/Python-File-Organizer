import tkinter as tk
from tkinter import filedialog, ttk
# import core.organizer

from ui.app import FileFlowApp

def main():
    app = FileFlowApp()
    app.mainloop()

if __name__ == "__main__":
    main()

"""
selected_folder = ""

def select_folder():

    global selected_folder

    selected_folder = filedialog.askdirectory()

    if selected_folder:
        folder_label.config(text=f"Selected Folder: {selected_folder}")

def organize_files():

    if not selected_folder:
        status_label.config(text="Please select a folder first.")
        return
    
    progress['value'] = 0

    core.organizer.organize_files(selected_folder, update_progress)

    progress['value'] = 100

    status_label.config(text="Files organized successfully!")

def update_progress(current, total):
    progress['value'] = (current / total) * 100
    root.update_idletasks()


# Create the main application window
root = tk.Tk()

root.title("FileFlow - File Organizer")
root.geometry("600x400")

# Title

title = tk.Label(root, text="FileFlow - File Organizer", font=("Helvetica", 16))
title.pack(pady=10)

# Select Folder Button

select_button = tk.Button(root, text="Select Folder", command=select_folder)
select_button.pack()

# Shows the selected folder

folder_label = tk.Label(root, text="No folder selected")
folder_label.pack(pady=10)

# Organize Files Button

organize_button = tk.Button(root, text="Organize Files", command=organize_files)
organize_button.pack(pady=10)

# Progress Bar

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

# Status Label

status_label = tk.Label(root, text="Ready to organize files.", font=("Helvetica", 12))
status_label.pack()

# Run the application

root.mainloop()
"""