from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.models.copywriter_schema import CopyWriterState

@tool
async def review_research_reports(state: Annotated[CopyWriterState, InjectedState]):
    """Use this tool to review available research reports to inform your writing.
    
    Returns:
        A list of research reports.
    """

    return [report.model_dump_json() for report in state.research_reports]