import operator
from typing import Annotated
from pydantic import BaseModel
from langgraph.graph import add_messages


class SupervisorState(BaseModel):
    """The state of the supervisor agent. 
    
    The research_reports attribute is shared with the researcher agent. This allows us to share the research reports between the researcher and copywriter agents.
    """
    messages: Annotated[list, add_messages] = []
    research_reports: Annotated[list, operator.add] = []
    task_description: str | None = None