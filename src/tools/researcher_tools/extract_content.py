from typing import List
from langchain_core.tools import tool
from langchain_tavily import TavilyExtract

from src.core.logs import logger
from src.core.settings import settings


@tool
async def extract_content_from_webpage(urls: List[str]):
    """
    Extract the content from webpages.

    Args:
        urls: List of webpage URLs.

    Returns:
        A list of dictionaries containing extracted webpage content.
    """

    logger.info(f"[extract_content_from_webpage] Tool called with {len(urls)} URL(s): {urls}")

    try:
        logger.info("[extract_content_from_webpage] Initializing TavilyExtract")
        web_extract = TavilyExtract(tavily_api_key=settings.TAVILY_API_KEY)

        logger.info("[extract_content_from_webpage] Sending extraction request to Tavily")

        response = await web_extract.ainvoke({"urls": urls})

        logger.info(f"[extract_content_from_webpage] Raw Tavily response: {response}")

        results = response.get("results", [])

        logger.info(f"[extract_content_from_webpage] Successfully extracted content from "f"{len(results)} webpage(s)")

        logger.debug(f"[extract_content_from_webpage] Returning results: {results}")

        return results

    except Exception as e:
        logger.exception(f"[extract_content_from_webpage] Failed to extract webpage content: {e}")
        raise