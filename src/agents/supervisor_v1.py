from datetime import datetime
import asyncio
from pprint import pprint

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from src.core.settings import settings
from src.utils.load_file import load_file
from src.services.llm_service import llm_model_flash

from src.tools.supervisor_tools.researcher_tool import call_researcher
from src.tools.supervisor_tools.copywriter_tool import call_copywriter


# Load prompt
supervisor_prompt = load_file(
    file_path=settings.SUPERVISOR_PROMPT
)

# Create Supervisor Agent
supervisor_agent = create_agent(
    model=llm_model_flash,
    tools=[
        call_researcher,
        call_copywriter,
    ],
    system_prompt=supervisor_prompt.format(
        current_datetime=datetime.now()
    ),
)


async def supervisor(state):
    """Supervisor node for LangGraph."""

    result = await supervisor_agent.ainvoke(
        {
            "messages": state["messages"]
        }
    )

    return {
        "messages": result["messages"]
    }


# -------------------------
# Local Testing
# -------------------------

async def main():

    state = {
        "messages": [
            HumanMessage(
                content="Write a blog on AI Agents"
            )
        ]
    }

    result = await supervisor(state)

    print("\n=== MESSAGES ===\n")
    pprint(result["messages"])

    print("\n=== FINAL RESPONSE ===\n")
    response = result["messages"][-1].content[0]
    print(response.get("text"))


if __name__ == "__main__":
    asyncio.run(main())


# from datetime import datetime
# from langchain_core.messages import SystemMessage

# from src.core.settings import settings
# from src.utils.load_file import load_file
# from src.services.llm_service import llm_model_flash
# from src.models.supervisor_schema import SupervisorState
# from src.tools.supervisor_tools.researcher_tool import call_researcher
# from src.tools.supervisor_tools.copywriter_tool import call_copywriter

# supervisor_prompt = load_file(file_path=settings.SUPERVISOR_PROMPT)

# tools = [call_researcher, call_copywriter]

# supervisor_llm = llm_model_flash.bind_tools(tools)

# async def supervisor(state: SupervisorState):
#     """The main supervisor agent."""
#     response = await supervisor_llm.ainvoke([
#         SystemMessage(
#             content=supervisor_prompt.format(
#                 current_datetime=datetime.now()
#             )
#         )
#     ] + state["messages"] )
#     return {"messages": [response]}


# import asyncio
# from pprint import pprint
# from langchain_core.messages import HumanMessage

# async def main():

#     state = {
#         "messages": [
#             HumanMessage(
#                 content="Write a blog on AI Agents"
#             )
#         ]
#     }

#     result = await supervisor(state)

#     msg = result["messages"][0]

#     print("\n=== CONTENT ===\n")
#     print(msg.content)

#     print("\n=== TOOL CALLS ===\n")
#     pprint(msg.tool_calls)

# asyncio.run(main())