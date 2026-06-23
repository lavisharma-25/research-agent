from pydantic import BaseModel
from typing import Literal

class SupervisorDecision(BaseModel):
    action: Literal[
        "research_again",
        "write_post",
        "rewrite_post",
        "finish"
    ]
    
    feedback: str
