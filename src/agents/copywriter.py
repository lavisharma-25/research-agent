from datetime import datetime
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage

from src.tools.copywriter_tools.review_research_tool import review_research_reports
from src.tools.copywriter_tools.generate_linkedin_post import generate_linkedin_post
from src.tools.copywriter_tools.generate_blog_post import generate_blog_post

from src.utils.load_file import load_file
from src.core.settings import settings
from src.services.llm_service.factory import llm

copywriter_prompt = load_file(file_path=settings.COPYWRITER_PROMPT)
linkedin_example = load_file(file_path=settings.LINKEDIN_EXAMPLE)
blog_example = load_file(file_path=settings.BLOG_EXAMPLE)

tools = [
    review_research_reports,
    generate_linkedin_post, 
    generate_blog_post
]

copywriter_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt = SystemMessage(
        content=copywriter_prompt.format(
            current_datetime=datetime.now(),
            linkedin_example=linkedin_example,
            blog_example=blog_example,
        )
    )
)

# import json
# import asyncio

# async def main():
#     response = await copywriter_agent.ainvoke(
#         {
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": input
#                 }
#             ]
#         }
#     )


#     print(json.dumps(response, indent=4, default=str))

# if __name__ == "__main__":
#     asyncio.run(main())