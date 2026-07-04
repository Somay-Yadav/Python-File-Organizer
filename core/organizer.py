import os
import shutil
import logging
import json
import sys
from pathlib import Path

# ==========================
# Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_PATH = BASE_DIR / "data" / "settings.json"

if getattr(sys, "frozen", False):
    LOG_PATH = Path(sys.executable).parent / "organizer.log"
else:
    LOG_PATH = BASE_DIR / "logs" / "organizer.log"

LOG_PATH.parent.mkdir(exist_ok=True)

# ==========================
# Load Settings
# ==========================

try:
    with open(CONFIG_PATH, "r") as file:
        FILE_TYPES = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    FILE_TYPES = {}

# ==========================
# Logger
# ==========================

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ==========================
# Helper Functions
# ==========================

def get_unique_filename(destination_folder, filename):
    """
    Returns a unique filename if a duplicate exists.
    Example:
        photo.png
        photo (1).png
        photo (2).png
    """

    name, extension = os.path.splitext(filename)

    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(destination_folder, new_filename)):
        new_filename = f"{name} ({counter}){extension}"
        counter += 1

    return new_filename


# ==========================
# Main Organizer
# ==========================

def organize_files(folder_path, progress_callback=None):
    """
    Organizes files inside the selected folder.

    Returns:
    {
        "moved": int,
        "skipped": int,
        "total": int
    }
    """

    folder_path = Path(folder_path)

    if not folder_path.exists():
        raise FileNotFoundError(folder_path)

    items = list(folder_path.iterdir())

    files = [item for item in items if item.is_file()]

    total_files = len(files)

    moved_files = 0
    skipped_files = 0
    moves = []

    for index, file_path in enumerate(files, start=1):
        # Skip the running executable, the active log file, and the running script
        try:
            resolved_path = file_path.resolve()
            is_exe = resolved_path == Path(sys.executable).resolve()
            is_log = resolved_path == LOG_PATH.resolve()
            is_script = False
            if sys.argv:
                is_script = resolved_path == Path(sys.argv[0]).resolve()
            
            if is_exe or is_log or is_script:
                skipped_files += 1
                logging.info(f"Skipped application file: {file_path}")
                if progress_callback:
                    progress_callback(index, total_files)
                continue
        except Exception as e:
            logging.error(f"Error resolving path '{file_path}': {e}")

        extension = file_path.suffix.lower()

        destination_folder = None

        # Find matching category
        for folder_name, extensions in FILE_TYPES.items():

            if extension in extensions:
                destination_folder = folder_path / folder_name
                break

        # Skip unsupported files
        # Move unknown files to Others
        if destination_folder is None:

            destination_folder = folder_path / "Others"

            try:
                destination_folder.mkdir(exist_ok=True)

                unique_name = get_unique_filename(
                    destination_folder,
                    file_path.name
                )

                destination = destination_folder / unique_name

                shutil.move(str(file_path), str(destination))

                moved_files += 1
                moves.append({"source": str(file_path), "destination": str(destination)})

                logging.info(
                    f"Moved '{file_path}' -> '{destination}' (Others)"
                )
            except Exception as e:
                skipped_files += 1
                logging.error(f"Failed to move '{file_path}' to Others: {e}")

            if progress_callback:
                progress_callback(index, total_files)

            continue

        # Create folder if needed
        try:
            destination_folder.mkdir(exist_ok=True)

            unique_name = get_unique_filename(
                destination_folder,
                file_path.name
            )

            destination = destination_folder / unique_name

            shutil.move(str(file_path), str(destination))

            moved_files += 1
            moves.append({"source": str(file_path), "destination": str(destination)})

            logging.info(
                f"Moved '{file_path}' -> '{destination}'"
            )
        except Exception as e:
            skipped_files += 1
            logging.error(f"Failed to move '{file_path}' to '{destination_folder}': {e}")

        if progress_callback:
            progress_callback(index, total_files)

    if moves:
        from core.undo import save_operation
        save_operation(folder_path, moves)

    return {
        "moved": moved_files,
        "skipped": skipped_files,
        "total": total_files
    }