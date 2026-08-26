"""Runtime flags from the module .env (STX_EDITABLE / STX_EXPORT)."""

import os
from pathlib import Path


def _load_env() -> None:
    env_file = Path(__file__).parent.parent / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


_load_env()

IS_EDITABLE = os.environ.get("STX_EDITABLE", "false").lower() == "true"
IS_EXPORTABLE = os.environ.get("STX_EXPORT", "false").lower() == "true"
