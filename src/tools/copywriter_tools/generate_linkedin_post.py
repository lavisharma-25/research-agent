from langchain_core.tools import tool

from src.core.settings import settings

@tool
async def generate_linkedin_post(title: str, content: str):
    """Use this tool to generate a LinkedIn post.
    
    Args:
        title: The title of the post.
        content: The content of the post in markdown format.

    Returns:
        A string indicating the location of the saved post.
    """
    file_name = f"linkedin_{title}.md"
    file_path = settings.AI_FILES / file_name
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"The LinkedIn post has been generated and saved to {file_path}"