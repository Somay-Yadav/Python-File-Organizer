from tkinter import filedialog


class FolderManager:

    @staticmethod
    def browse_folder():
        return filedialog.askdirectory(
            title="Select Folder"
        )