class Categorizer:

    FILE_TYPES = {

        "Image": {
            ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg", ".ico"
        },

        "Document": {
            ".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx",
            ".xls", ".xlsx", ".csv"
        },

        "Video": {
            ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"
        },

        "Audio": {
            ".mp3", ".wav", ".aac", ".ogg", ".flac", ".m4a"
        },

        "Archive": {
            ".zip", ".rar", ".7z", ".tar", ".gz"
        },

        "Code": {
            ".py", ".cpp", ".c", ".java", ".js",
            ".html", ".css", ".json", ".xml"
        }

    }

    @classmethod
    def get_category(cls, extension):

        extension = extension.lower()

        for category, extensions in cls.FILE_TYPES.items():

            if extension in extensions:
                return category

        return "Others"