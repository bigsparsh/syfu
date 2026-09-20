import json
from pathlib import Path
from uuid import uuid4
from datetime import date, datetime
from platformdirs import user_cache_dir, user_cache_path

LOG_LOCATION = user_cache_path("syfu") / "logs"

def ensure_cache_structure() -> None:

    cache_root = Path(user_cache_dir("syfu"))

    directories = [
        cache_root / "context",
        cache_root / "brain",
        cache_root / "logs",
    ]

    for d in directories:
        d.mkdir(parents=True, exist_ok=True)

    files = [
        cache_root / ".sync_state.json",
        cache_root / "context" / "long-term-context.md",
        cache_root / "context" / "short-term-context.md",
        cache_root / "brain" / "index.md",
    ]

    for f in files:
        if not f.exists():
            f.touch()

ensure_cache_structure()

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