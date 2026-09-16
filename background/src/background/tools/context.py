from langchain_core.tools import tool

CONTEXT_DIR="/home/bigsparsh/Projects/syfu/docs/context"

@tool()
def update_long_term_context(data: str):
    """
    In this we update the content that is relevant in the longer time scope and update the points to keep in mind or remove something that has been achieved.
    Note: This completely overrides the previous file. So, inclusion of the previous data is mandatory.
    Args:
        data (str): New modified data that is to be overwritten on long-term.md
    """
    print("[tool-invoke][update-long-term-context]")
    with open(f"{CONTEXT_DIR}/long-term.md", "w") as f:
        f.write(data)

@tool()
def update_short_term_context(data: str):
    """
    In this we update the content that is relevant in the shorter time scope and update the points to keep in mind or remove something that has been achieved.
    Note: This completely overrides the previous file. So, inclusion of the previous data is mandatory.
    Args:
        data (str): New modified data that is to be overwritten on short-term.md
    """

    print("[tool-invoke][update-short-term-context]")
    with open(f"{CONTEXT_DIR}/short-term.md", "w") as f:
        f.write(data)

@tool()
def get_short_term_context():
    """
    Gets the short term context stored in the MD file.
    Output:
        str : Contents of the short-term.md file containing info about the short term tasks and activities.
    """

    print("[tool-invoke][get-short-term-context]")
    with open(f"{CONTEXT_DIR}/short-term.md", "r") as f:
        return f.read()



@tool()
def get_long_term_context():
    """
    Gets the long term context stored in the MD file.
    Output:
        str : Contents of the long-term.md file containing info about the long term tasks and activities.
    """

    print("[tool-invoke][get-long-term-context]")
    with open(f"{CONTEXT_DIR}/long-term.md", "r") as f:
        return f.read()