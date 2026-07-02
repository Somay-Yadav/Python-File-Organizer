import os
import shutil
import time
import logging
import json
import sys

# Utility function to get the absolute path to a resource, works for both development and PyInstaller environments
# This function checks if the script is running in a PyInstaller bundle (frozen) or in a normal Python environment. It returns the absolute path to the specified resource, ensuring that the application can access its resources correctly regardless of how it is executed.

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

CONFIG_PATH = resource_path("config.json")

# Save logs next to the executable when bundled
if getattr(sys, "frozen", False):
    LOG_PATH = os.path.join(os.path.dirname(sys.executable), "organizer.log")
else:
    LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "organizer.log")

with open(CONFIG_PATH, "r") as file:
    file_types = json.load(file)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def get_unique_filename(destination_folder, filename):

    name, extension = os.path.splitext(filename)

    counter = 1

    new_filename = filename

    while os.path.exists(os.path.join(destination_folder, new_filename)):
        new_filename = f"{name} ({counter}){extension}"
        counter += 1

    return new_filename

def organize_files(path, progress_callback=None):

    files = os.listdir(path)
    total_files = len(files)

    for index, file in enumerate(files, start=1):

        file_path = os.path.join(path, file)
        
        if os.path.isfile(file_path):

            extension = os.path.splitext(file)[1].lower()

            moved = False

            for folder, extensions in file_types.items():

                if extension in extensions:

                    folder_path = os.path.join(path,folder)

                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                    unique_filename = get_unique_filename(folder_path, file)

                    destination_path = os.path.join(folder_path, unique_filename)
                    
                    shutil.move(file_path, destination_path)

                    logging.info(f"Moved '{file_path}' -> '{destination_path}'")
                    moved = True
                    break
                
            if not moved:
                print(f"No folder found for {file}.")
                logging.info(f"No folder found for {file}.")

        if progress_callback:
            progress_callback(index, total_files)
            time.sleep(0.2)  # Simulate some processing time