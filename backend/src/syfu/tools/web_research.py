from langchain_core.tools import tool
from ddgs import DDGS


@tool()
def web_search(queries: list[str]):
    """
    This tool is used to search the web for relevant results.
    Args:
        queries (list[str]): List of keywords to search for.
    Output: List of all the relevant documents.
    """
    res = []
    with DDGS() as ddgs:
        for q in queries:
            for d in ddgs.text(q, max_results=3):
                res.append(d.copy())
    return res
