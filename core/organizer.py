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

    for index, file_path in enumerate(files, start=1):

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

            destination_folder.mkdir(exist_ok=True)

            unique_name = get_unique_filename(
                destination_folder,
                file_path.name
            )

            destination = destination_folder / unique_name

            shutil.move(str(file_path), str(destination))

            moved_files += 1

            logging.info(
                f"Moved '{file_path}' -> '{destination}' (Others)"
            )

            if progress_callback:
                progress_callback(index, total_files)

            continue

        # Create folder if needed
        destination_folder.mkdir(exist_ok=True)

        unique_name = get_unique_filename(
            destination_folder,
            file_path.name
        )

        destination = destination_folder / unique_name

        shutil.move(str(file_path), str(destination))

        moved_files += 1

        logging.info(
            f"Moved '{file_path}' -> '{destination}'"
        )

        if progress_callback:
            progress_callback(index, total_files)

    return {
        "moved": moved_files,
        "skipped": skipped_files,
        "total": total_files
    }