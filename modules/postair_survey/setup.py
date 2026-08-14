"""Path setup — import as the FIRST line of book.py.

Adds the module directory (for ``custom``/``blocks`` imports) and the
shared-blocks directory (for ``shared_widgets``/``postair_data``) to sys.path.
"""

import sys
from pathlib import Path

_MODULE_DIR = Path(__file__).parent
_SHARED_DIR = _MODULE_DIR.parent / "shared-blocks"

for _p in (str(_MODULE_DIR), str(_SHARED_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
