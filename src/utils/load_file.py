from src.core.settings import settings

def load_file(file_path: str) -> str:

    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")

    return file_path.read_text(encoding="utf-8")