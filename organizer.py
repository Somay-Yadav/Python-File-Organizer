import os
import shutil

path = input("Enter the path of the folder you want to organize: ")

file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Applications": [".exe", ".msi", ".apk"],
}

for file in os.listdir(path):

    file_path = os.path.join(path, file)
    
    if os.path.isfile(file_path):

        extension = os.path.splitext(file)[1].lower()

        moved = False

        for folder, extensions in file_types.items():

            if extension in extensions:

                folder_path = os.path.join(path,folder)

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                shutil.move(file_path, folder_path)
                print(f"Moved {file} to {folder} folder.")
                moved = True
                break
            
        if not moved:
            print(f"No folder found for {file}.")