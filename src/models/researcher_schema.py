from pydantic import BaseModel

class ResearchReport(BaseModel):
    topic: str
    report: str