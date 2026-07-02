# 📁 Python File Organizer

A polished desktop tool that organizes files into folders by extension — simple, fast, and configurable.

![Hero screenshot](assets/screenshot.png)

---

**Quick links:** [Releases](https://github.com/Somay-Yadav/Python-File-Organizer/releases) • [Download ZIP (main)](https://github.com/Somay-Yadav/Python-File-Organizer/archive/refs/heads/main.zip)

---

**Badges:**

- ![Made with Python](https://img.shields.io/badge/Made%20with-Python-3.10-blue)
- ![License: MIT](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Features

- **Intuitive GUI:** Lightweight Tkinter interface for easy folder selection.
- **Automatic sorting:** Files moved into categorized folders by extension.
- **Progress tracking:** Live progress bar and logs for transparency.
- **Duplicate handling:** Safe renaming strategy to avoid data loss.
- **Custom categories:** Edit `config.json` to add/remove types.
- **Windows friendly:** Build a single-file executable with `PyInstaller`.

---

## 📂 Supported Categories (default)

| Category | Extensions |
|---|---|
| Images | .jpg, .jpeg, .png, .gif, .bmp |
| Documents | .pdf, .docx, .txt, .xlsx, .pptx |
| Audio | .mp3, .wav, .aac |
| Videos | .mp4, .avi, .mkv |
| Applications | .exe, .msi, .apk |

You can customize these by editing `config.json`.

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Somay-Yadav/Python-File-Organizer.git
```

Change into the project directory:

```bash
cd Python-File-Organizer
```

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Run the app:

```bash
python main.py
```

---

## 🧭 Project Structure

```
Python-File-Organizer/
├── main.py            # app entry
├── organizer.py       # core organizing logic
├── config.json        # custom categories
├── requirements.txt
├── README.md
├── assets/            # screenshots and icons
└── organizer.log      # runtime log (generated)
```

---

## 🛠️ Build a Windows Executable

Build a single-file GUI executable using `PyInstaller`:

```bash
python -m PyInstaller --onefile --windowed --name FileOrganizer --add-data "config.json;." main.py
```

The `dist` folder will contain `FileOrganizer.exe`.

---

## 📥 Releases & Direct Downloads

- Branch ZIP (latest main): https://github.com/Somay-Yadav/Python-File-Organizer/archive/refs/heads/main.zip
- Releases page: https://github.com/Somay-Yadav/Python-File-Organizer/releases

If the project has a release asset, the direct download usually looks like:

```
https://github.com/Somay-Yadav/Python-File-Organizer/releases/download/<tag>/<asset-filename>
```

---

## 🔌 API: Check latest release (example)

Use this minimal Node.js/Express snippet to fetch latest release assets and download URLs via GitHub API.

```javascript
const express = require('express');
const axios = require('axios');
const app = express();

app.get('/api/check-download', async (req, res) => {
	try {
		const owner = 'Somay-Yadav';
		const repo = 'Python-File-Organizer';
		const r = await axios.get(`https://api.github.com/repos/${owner}/${repo}/releases/latest`, {
			headers: { 'Accept': 'application/vnd.github+json', 'User-Agent': 'node.js' }
		});
		const release = r.data;
		if (!release.assets || release.assets.length === 0) return res.json({ success: false, message: 'No assets found' });
		const assets = release.assets.map(a => ({ name: a.name, size: a.size, url: a.browser_download_url }));
		res.json({ success: true, tag: release.tag_name, name: release.name, assets });
	} catch (err) {
		res.status(500).json({ success: false, message: err.message });
	}
});

app.listen(3000, () => console.log('API running on http://localhost:3000'));
```

Use `GET /api/check-download` to retrieve latest release assets and direct download links.

---

## ✅ Contributing

- Fork the repo, open a feature branch, and submit a PR.
- Add tests or a small demo when you add features.

---

## 📄 License

This project is released under the MIT License.

---

Made with ❤️ by the community.