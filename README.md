# 📁 File Organizer

A simple Python automation tool that automatically organizes files into different folders based on their file extensions.

## ✨ Features

- 📁 Organize files by extension
- 🖥️ Tkinter GUI
- 📂 Folder picker
- 📊 Progress bar
- 🔄 Duplicate file handling
- 📝 File organization logs
- ⚙️ Custom categories using `config.json`

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
├── config.json
├── README.md
├── requirements.txt
└── .gitignore
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

* Create executable application (.exe)
* Improved UI

## 👨‍💻 Author

**Somay Yadav**

⭐ If you like this project, consider giving it a star!
