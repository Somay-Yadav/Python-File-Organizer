class Categorizer:

    FILE_TYPES = {

        "Image": {
            ".png", ".jpg", ".jpeg", ".gif",
            ".bmp", ".webp", ".svg", ".ico", ".tiff"
        },

        "Document": {
            ".pdf", ".doc", ".docx", ".txt",
            ".ppt", ".pptx", ".xls", ".xlsx",
            ".csv", ".rtf", ".md"
        },

        "Video": {
            ".mp4", ".avi", ".mkv", ".mov",
            ".wmv", ".flv", ".webm", ".m4v"
        },

        "Audio": {
            ".mp3", ".wav", ".aac", ".ogg",
            ".flac", ".m4a", ".wma"
        },

        "Archive": {
            ".zip", ".rar", ".7z",
            ".tar", ".gz", ".bz2", ".xz"
        },

        "Application": {
            ".exe", ".msi", ".bat",
            ".cmd", ".com", ".lnk"
        }

    }

    @classmethod
    def get_category(cls, extension):

        extension = extension.lower()

        for category, extensions in cls.FILE_TYPES.items():
            if extension in extensions:
                return category

        return "Others"