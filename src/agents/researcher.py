from langchain.agents import create_agent

from src.tools.researcher_tools.search_web import search_web
from src.tools.researcher_tools.extract_content import extract_content_from_webpage
from src.tools.researcher_tools.generate_report import generate_research_report

from src.core.settings import settings
from src.utils.load_file import load_file
from src.services.llm_service.factory import llm

researcher_agent = create_agent(
    model=llm,
    tools=[search_web, extract_content_from_webpage, generate_research_report],
    system_prompt=load_file(file_path=settings.RESEARCHER_PROMPT)
)

# import json
# import asyncio

# async def main():
#     response = await researcher_agent.ainvoke(
#         {
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": "Research the latest advancements in Agentic AI and generate a detailed report."
#                 }
#             ]
#         }
#     )


#     print(json.dumps(response, indent=4, default=str))

# if __name__ == "__main__":
#     asyncio.run(main())