from src.core.settings import settings

def load_prompt(file_name: str) -> str:
    prompt_file_path = settings.PROMPTS_DIR / f"{file_name}.md"

    if not prompt_file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file_path}")

    return prompt_file_path.read_text(encoding="utf-8")