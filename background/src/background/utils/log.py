import json
from datetime import date, datetime, timedelta
from itertools import islice
from operator import itemgetter
from pathlib import Path

from platformdirs import user_cache_path

from src.background.utils.cache import ensure_cache_structure

ensure_cache_structure()
cache_path = user_cache_path("syfu")

SYNC_FILE_PATH = cache_path / ".sync_state.json"
LOG_FILE_PATH = cache_path / "logs"
LOG_INGEST_THRESHOLD = 5

IGNORE_TOOLS = ["deep_search", "web_search"]


def get_sync_state() -> dict[any]:
    with open(SYNC_FILE_PATH, "r") as f:
        res = f.read()
        if res.strip() == "":
            return {"last_file": f"{date.today()}.jsonl", "last_offset": 0}
        res = json.loads(res)
        return res


def update_sync_state(date_file: str, log_idx: int):
    with open(SYNC_FILE_PATH, "w") as f:
        f.write(json.dumps({"last_file": date_file, "last_offset": log_idx}))


def get_log_data():
    last_file, last_offset = itemgetter("last_file", "last_offset")(get_sync_state())
    logs = []
    date_format = "%Y-%m-%d"
    last_date = datetime.strptime(last_file.split(".")[0], date_format).date()

    try:
        with open(f"{LOG_FILE_PATH / str(last_date)}.jsonl", "r") as f:
            for line in islice(f, last_offset, None):
                print(last_date, last_offset)
                log = json.loads(line)
                if log["tool_name"] not in IGNORE_TOOLS:
                    logs.append(json.loads(line))
                last_offset += 1
                if len(logs) == LOG_INGEST_THRESHOLD:
                    break

            while len(logs) != LOG_INGEST_THRESHOLD:
                last_offset = 0
                last_date += timedelta(days=1)
                log_file_path = Path(f"{LOG_FILE_PATH / str(last_date)}.jsonl")
                if log_file_path.exists():
                    with open(log_file_path, "r") as f1:
                        for line in islice(f1, last_offset, None):
                            print(last_date, last_offset)
                            log = json.loads(line)
                            if log["tool_name"] not in IGNORE_TOOLS:
                                logs.append(json.loads(line))
                            last_offset += 1
                            if len(logs) == LOG_INGEST_THRESHOLD:
                                break
                if last_date > date.today():
                    last_date -= timedelta(days=1)
                    break

    except FileNotFoundError:
        print("This log file doesn't exist yet.")
    with open(SYNC_FILE_PATH, "w") as f:
        f.write(
            json.dumps(
                {"last_file": f"{last_date!s}.jsonl", "last_offset": last_offset}
            )
        )
    return logs
