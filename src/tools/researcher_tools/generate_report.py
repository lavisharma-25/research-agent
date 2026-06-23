from langchain_core.tools import tool

from core.logs import logger
from src.models.researcher_schema import ResearchReport


@tool
async def generate_research_report(topic: str, report: str):
    """
    Generate a structured research report.

    Args:
        topic: The research topic.
        report: The generated report content.

    Returns:
        Structured research report.
    """

    logger.info(f"[generate_research_report] Tool called for topic: {topic}")

    try:
        logger.info("[generate_research_report] Creating ResearchReport model")

        research_report = ResearchReport.model_validate({
            "topic": topic,
            "report": report
        })

        logger.info("[generate_research_report] Research report created successfully")

        result = research_report.model_dump()

        logger.info("[generate_research_report] Returning structured report")

        return result

    except Exception as e:
        logger.exception(f"[generate_research_report] Error generating report: {str(e)}")
        raise