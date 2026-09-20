from pathlib import Path

from platformdirs import user_cache_dir


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
