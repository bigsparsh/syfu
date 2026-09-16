import json
from uuid import uuid4
from datetime import date, datetime

LOG_LOCATION = "/home/bigsparsh/Projects/syfu/docs/logs/";

def create_tool_log(tool_name, input, result, prompt_id):
    dt = str(date.today())
    with open(f"{LOG_LOCATION}/{dt}.jsonl", 'a') as f:
        f.write(json.dumps({
            'log_id': str(uuid4()),
            'prompt_id': prompt_id,
            'tool_name': tool_name,
            'result': result,
            'input': input,
            'timestamp': str(datetime.now())
        }) + "\n")