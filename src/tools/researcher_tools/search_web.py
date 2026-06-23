from langchain_core.tools import tool
from langchain_tavily import TavilySearch

from core.logs import logger
from src.core.settings import settings


@tool
async def search_web(query: str, num_results: int = 3):
    """Search the web and return relevant search results."""

    logger.info(f"[search_web] Called | query='{query}' | num_results={num_results}")

    try:
        logger.info("[search_web] Initializing TavilySearch")

        web_search = TavilySearch(
            max_results=min(num_results, 3),
            topic="general",
            tavily_api_key=settings.TAVILY_API_KEY,
        )

        logger.info("[search_web] Executing search")

        search_results = await web_search.ainvoke({"query": query})

        logger.info(f"[search_web] Received {len(search_results.get('results', []))} results")

        processed_results = {
            "query": query,
            "results": []
        }

        for result in search_results.get("results", []):
            processed_results["results"].append({
                "title": result.get("title"),
                "url": result.get("url"),
                "content_preview": result.get("content")
            })

        logger.info(f"[search_web] Returning {len(processed_results['results'])} processed results")

        return processed_results

    except Exception as e:
        logger.exception(f"[search_web] Failed | query='{query}' | error={str(e)}")
        raise