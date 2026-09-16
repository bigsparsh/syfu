# sync file read, log file read, init llm, init
import asyncio, json
from langchain.messages import HumanMessage
from src.background.graph import agent
from src.background.utils.log import get_log_data

async def main():
    log_data = get_log_data()
    if not log_data:
        print("NO LOGS: nothing to compress")
        return

    messages = [HumanMessage(content=json.dumps(log_data))]
    result = await agent.ainvoke({'messages': messages})

    for msg in result['messages']:
        print(msg.content)
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())