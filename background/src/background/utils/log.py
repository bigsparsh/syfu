import json
from datetime import date, timedelta, datetime
from operator import itemgetter
from pathlib import Path
from itertools import islice
from pprint import pprint

SYNC_FILE_PATH="/home/bigsparsh/Projects/syfu/background/src/background/.sync_state.json"
LOG_FILE_PATH="/home/bigsparsh/Projects/syfu/docs/logs"
LOG_INGEST_THRESHOLD = 3

def get_sync_state() -> dict[any]:
    with open(SYNC_FILE_PATH, 'r') as f:
        res = f.read()
        if res.strip() == "": 
            return {
                "last_file": f"{date.today()}.jsonl",
                "last_offset": 0
            }
        res = json.loads(res)
        return res

def update_sync_state(date_file: str, log_idx: int):
    with open(SYNC_FILE_PATH, "w") as f:
        f.write(json.dumps({"last_file": date_file, 'last_offset': log_idx}))

def get_log_data():
    last_file, last_offset = itemgetter("last_file", "last_offset")(get_sync_state())
    logs = []
    date_format = "%Y-%m-%d"
    last_date = datetime.strptime(last_file.split(".")[0], date_format).date()

    try:
        with open(f"{LOG_FILE_PATH}/{str(last_date)}.jsonl", "r") as f:
            for line in islice(f, last_offset, last_offset + LOG_INGEST_THRESHOLD):
                logs.append(json.loads(line))
            last_offset += LOG_INGEST_THRESHOLD
            while len(logs) != LOG_INGEST_THRESHOLD:
                last_offset = 0
                last_date += timedelta(days=1)
                log_file_path = Path(f"{LOG_FILE_PATH}/{str(last_date)}.jsonl")
                if log_file_path.exists():
                    last_offset += 1
                    with open(log_file_path, 'r') as f1:
                        for line in islice(f1, last_offset, LOG_INGEST_THRESHOLD - len(logs)):
                            logs.append(json.loads(line))
        print("LOGS FETCHED")
        pprint(logs)
    except FileNotFoundError: print("This log file doesn't exist yet.")
    with open(SYNC_FILE_PATH, "w") as f:
        f.write(json.dumps({"last_file": f"{str(last_date)}.jsonl", "last_offset": last_offset}))
    return logs