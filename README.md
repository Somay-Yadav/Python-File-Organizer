# 📁 File Organizer

A simple Python automation tool that automatically organizes files into different folders based on their file extensions.

## 🚀 Features 

- 📁 Organize files by file type
- 🖥️ Tkinter GUI interface
- 📂 Select folder using file dialog
- 📊 Live progress bar while organizing
- 📦 Modular project structure

## 🛠️ Technologies Used

* Python
* os module
* shutil module
* tkinter module
* time module

## 📂 Project Structure

```
File-Organizer/
│
├── main.py
├── organizer.py
├── requirements.txt
├── README.md
├── .gitignore
└── (other project files)
```

## ⚙️ Installation & Setup

1. Clone the repository:

```bash
git clone https://github.com/Somay-Yadav/Python-File-Organizer.git
```

2. Open the project folder:

```bash
cd File-Organizer
```

3. Install requirements:

```bash
pip install -r requirements.txt
```

## ▶️ How to Run

Run the program:

```bash
python organizer.py
```

Enter the folder path you want to organize.

Example:

```
Enter folder path: Downloads
```

The program will automatically create folders and move files.

## 📌 Example

Before:

```
Downloads/
 ├── photo.png
 ├── movie.mp4
 ├── notes.pdf
 └── song.mp3
```

After:

```
Downloads/
 ├── Images/
 │    └── photo.png
 ├── Videos/
 │    └── movie.mp4
 ├── Documents/
 │    └── notes.pdf
 └── Music/
      └── song.mp3
```

## 🔮 Future Improvements

* Add duplicate file handling
* Add file organization logs
* Add custom categories
* Create executable application (.exe)

## 👨‍💻 Author

**Somay Yadav**

⭐ If you like this project, consider giving it a star!
