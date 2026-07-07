from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, List, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    messages: str
    answer: Optional[Any] = None

    memory: Annotated[list[BaseMessage], add_messages] = Field(default_factory=list)