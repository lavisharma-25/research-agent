import asyncio
from pprint import pprint
from datetime import datetime

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage

from src.core.settings import settings
from src.utils.load_file import load_file
from src.services.llm_service.factory import llm
from src.graph.state import AgentState

from src.tools.supervisor_tools.researcher_tool import call_researcher
from src.tools.supervisor_tools.copywriter_tool import call_copywriter


# Load prompt
supervisor_prompt = load_file(
    file_path=settings.SUPERVISOR_PROMPT
)

# Create Supervisor Agent
supervisor_agent = create_agent(
    model=llm,
    tools=[
        call_researcher,
        call_copywriter,
    ],
    system_prompt=supervisor_prompt.format(
        current_datetime=datetime.now()
    ),
)


async def supervisor(state: AgentState):

    conversation = [
        *state.memory,
        HumanMessage(content=state.messages)
    ]

    result = await supervisor_agent.ainvoke(
        {
            "messages": conversation
        }
    )

    last_message = result["messages"][-1]

    if isinstance(last_message.content, list):
        answer = "\n".join(
            item["text"]
            for item in last_message.content
            if isinstance(item, dict) and item.get("type") == "text"
        )
    else:
        answer = str(last_message.content)

    return {
        "answer": answer,

        "memory": [
            HumanMessage(content=state.messages),
            AIMessage(content=answer)
        ]
    }