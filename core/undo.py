import json
import os
import shutil
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
HISTORY_PATH = BASE_DIR / "data" / "history.json"

def get_history():
    if not HISTORY_PATH.exists():
        return []
    try:
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_history(history):
    HISTORY_PATH.parent.mkdir(exist_ok=True)
    try:
        with open(HISTORY_PATH, "w") as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        print(f"Failed to save history: {e}")

def save_operation(folder_path, moves):
    if not moves:
        return
    history = get_history()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append({
        "timestamp": timestamp,
        "folder": str(folder_path),
        "moves": moves
    })
    # Limit history to last 10 operations
    if len(history) > 10:
        history = history[-10:]
    save_history(history)

def undo_last_operation():
    history = get_history()
    if not history:
        return {"status": "error", "message": "No operations to undo."}
    
    last_op = history.pop()
    moves = last_op["moves"]
    undone_count = 0
    failed_count = 0
    
    # Move files in reverse order
    for move in reversed(moves):
        src = Path(move["source"])
        dest = Path(move["destination"])
        
        if dest.exists():
            try:
                # Ensure the original directory exists
                src.parent.mkdir(exist_ok=True, parents=True)
                shutil.move(str(dest), str(src))
                undone_count += 1
            except Exception as e:
                failed_count += 1
                print(f"Failed to undo move: {dest} -> {src}: {e}")
        else:
            failed_count += 1
            
    # Try to clean up empty directories that were created
    created_dirs = set(Path(move["destination"]).parent for move in moves)
    for folder in sorted(created_dirs, key=lambda x: len(x.parts), reverse=True):
        try:
            if folder.exists() and not os.listdir(folder):
                folder.rmdir()
        except Exception:
            pass
            
    save_history(history)
    return {
        "status": "success",
        "undone": undone_count,
        "failed": failed_count,
        "total": len(moves)
    }

def get_last_operation():
    history = get_history()
    if not history:
        return None
    return history[-1]
