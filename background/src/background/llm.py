from langchain_google_genai import ChatGoogleGenerativeAI
from src.background.prompts import system_prompt

from src.background.tools.brain import *
from src.background.tools.context import *
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
)

tools = [
    update_long_term_context,
    update_short_term_context,
    get_short_term_context,
    get_long_term_context,

    get_index,
    update_index,
    list_brain,
    update_brain_file,
    create_brain_file,
]

tos = {t.name: t for t in tools}

llm = llm.bind_tools(tools)

def invoke_llm(query: str):
    return llm.invoke(f"{system_prompt} {query}")