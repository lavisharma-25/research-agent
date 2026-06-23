from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

from src.core.settings import settings


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
config = {
    "project": settings.credentials.project_id,
    "credentials": settings.credentials,
    "location": settings.LOCATION,
    "vertexai": True,
    "temperature": 0,
    "model_kwargs": {
        "thinking": 0,
    },
}

# safety_settings = {
#     HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
# }


# -----------------------------------------------------------------------------
# LLM Factory
# -----------------------------------------------------------------------------
def create_llm(model_name: str):
    return ChatGoogleGenerativeAI(
        model=model_name,
        # safety_settings=safety_settings,
        **config,
    )


# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------
llm_model_flash = create_llm(settings.GEMINI_MODEL_FLASH)