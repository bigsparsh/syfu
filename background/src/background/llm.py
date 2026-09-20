from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# from langchain_openai import ChatOpenAI
from src.background.prompts import system_prompt
from src.background.tools.brain import *
from src.background.tools.context import *

load_dotenv()

# llm = ChatOpenAI(
#     base_url="http://localhost:8080/v1",
#     api_key="not-needed",  # llama-server doesn't enforce an API key by default
#     model="Qwen/Qwen2.5-7B-Instruct-GGUF",
#     temperature=0.2,
#     max_tokens=2048,
#     streaming=False
# )
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
)

tools = [
    # Context
    update_long_term_context,
    update_short_term_context,
    get_short_term_context,
    get_long_term_context,
    # Brain Manipulation
    get_index,
    update_index,
    list_brain,
    update_brain_file,
    create_brain_folder,
    get_uuid,
    create_brain_file,
]

tos = {t.name: t for t in tools}

llm = llm.bind_tools(tools)


def invoke_llm(query: str):
    return llm.invoke(f"{system_prompt} {query}")
