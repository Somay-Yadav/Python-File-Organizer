import os
import sys
from pathlib import Path

from core.categorizer import Categorizer

class FileScanner:

    @staticmethod
    def scan(folder_path):
        files = []

        if not folder_path:
            return files

        # Determine active log path to filter it out
        if getattr(sys, "frozen", False):
            log_path = Path(sys.executable).parent / "organizer.log"
        else:
            base_dir = Path(__file__).resolve().parent.parent
            log_path = base_dir / "logs" / "organizer.log"

        for item in os.listdir(folder_path):

            full_path = os.path.join(folder_path, item)

            if os.path.isfile(full_path):

                try:
                    full_path_obj = Path(full_path).resolve()
                    is_exe = full_path_obj == Path(sys.executable).resolve()
                    is_log = full_path_obj == log_path.resolve()
                    is_script = False
                    if sys.argv:
                        is_script = full_path_obj == Path(sys.argv[0]).resolve()
                    
                    if is_exe or is_log or is_script:
                        continue
                except Exception:
                    pass

                extension = os.path.splitext(item)[1].lower()

                files.append({
                    "name": item,
                    "path": full_path,
                    "size": os.path.getsize(full_path),
                    "extension": extension,
                    "category": Categorizer.get_category(extension)
                })

        return files