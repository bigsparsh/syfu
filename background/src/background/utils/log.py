import json
from datetime import date, timedelta, datetime
from operator import itemgetter
from pathlib import Path

SYNC_FILE_PATH="/home/bigsparsh/Projects/syfu/background/src/background/.sync_state.json"
LOG_FILE_PATH="/home/bigsparsh/Projects/syfu/docs/logs"

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
        # with open(f"{LOG_FILE_PATH}/{last_file}", 'r') as f:
        #     for js in f.readlines():
        #         logs.append(json.loads(js))
        while last_date != date.today():
            print(last_date, date.today())
            log_file_path = Path(f"{LOG_FILE_PATH}/{str(last_date)}.jsonl")
            if log_file_path.exists():
                with open(log_file_path, 'r') as f:
                    for js in f.readlines():
                        logs.append(json.loads(js))
            print(len(logs))
            last_date += timedelta(days=1)
    except FileNotFoundError: print("This log file doesn't exist yet.")
    with open(SYNC_FILE_PATH, "w") as f:
        f.write(json.dumps({"last_file": f"{str(last_date)}.jsonl", "last_offset": 0}))
    return logs