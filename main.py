import asyncio

from src.graph.builder import get_workflow

async def main():

    workflow = await get_workflow()

    session_id = "user_123"

    config = {
        "configurable": {
            "thread_id": session_id
        }
    }

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        result = await workflow.ainvoke(
            {
                "messages": user_input
            },
            config=config
        )

        print("\nAssistant:")
        print(result["answer"])

        # Memory dekhne ke liye
        state = await workflow.aget_state(config)

        print(
            "\nMemory Length:",
            len(state.values.get("memory", []))
        )


if __name__ == "__main__":
    asyncio.run(main())
