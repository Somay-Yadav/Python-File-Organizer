import os

from core.categorizer import Categorizer

class FileScanner:

    @staticmethod
    def scan(folder_path):
        files = []

        if not folder_path:
            return files

        for item in os.listdir(folder_path):

            full_path = os.path.join(folder_path, item)

            if os.path.isfile(full_path):

                extension = os.path.splitext(item)[1].lower()

                files.append({
                    "name": item,
                    "path": full_path,
                    "size": os.path.getsize(full_path),
                    "extension": extension,
                    "category": Categorizer.get_category(extension)
                })

        return files