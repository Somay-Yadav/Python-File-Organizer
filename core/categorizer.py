import json
from pathlib import Path

class Categorizer:

    @classmethod
    def get_category(cls, extension):
        extension = extension.lower()

        base_dir = Path(__file__).resolve().parent.parent
        config_path = base_dir / "data" / "settings.json"

        try:
            with open(config_path, "r") as file:
                file_types = json.load(file)
        except Exception:
            file_types = {}

        for category, extensions in file_types.items():
            if extension in extensions:
                return category

        return "Others"