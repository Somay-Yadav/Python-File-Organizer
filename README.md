# 📁 File Organizer

A simple Python automation tool that automatically organizes files into different folders based on their file extensions.

## 🚀 Features

* Automatically sorts files into categories
* Creates folders automatically if they don't exist
* Supports multiple file types:

  * Images
  * Videos
  * Documents
  * Music
  * Applications
* Uses Python file handling and automation

## 🛠️ Technologies Used

* Python
* os module
* shutil module

## 📂 Project Structure

```
File-Organizer/
│
├── organizer.py
├── README.md
└── requirements.txt
```

## ⚙️ Installation & Setup

1. Clone the repository:

```bash
git clone <your-repository-link>
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

* Add GUI interface
* Add duplicate file handling
* Add file organization logs
* Add custom categories
* Add progress bar
* Create executable application (.exe)

## 👨‍💻 Author

**Somay Yadav**

⭐ If you like this project, consider giving it a star!
