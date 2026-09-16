from langchain_core.tools import tool
import json
from crawl4ai import AsyncWebCrawler
import asyncio
from ddgs import DDGS
from fake_useragent import UserAgent
from syfu.utils.file_handling import create_tool_log

@tool()
def web_search (queries: list[str], prompt_id: str):
    """
    This tool is used to search the web for relevant results.
    Args:
        queries (list[str]): List of keywords to search for.
    Output: List of all the relevant documents.
    """

    print("[tool-invoke][web_search]")
    res = []
    with DDGS() as ddgs:
        for q in queries:
            for d in ddgs.text(q, max_results=3):
                res.append(d.copy())

    create_tool_log("web_search", queries, res, prompt_id)
    return json.dumps(res)


@tool()
async def deep_search(links: list[str], prompt_id: str):
    """
    This tool is used to search deeper through given links which are relevant to the user query.
    Agrs:
        links (list[str]): List of links to scrape.
    Output: List of information in Markdown string.
    """

    print("[tool-invoke][deep_search]")
    out = []
    async with AsyncWebCrawler() as crawler:
        for link in links:
            try: 
                res = await crawler.arun(url=link)
                out.append(res.markdown)
            except Exception as e: 
                print(f"Error occured while scraping '{link}': {e}")
                out.append(f"Error occured while scraping this link: {link}")
    create_tool_log("deep_search", links, out, prompt_id)
    return out
