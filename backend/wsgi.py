import os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
try:
    from app import create_app  # type: ignore
    app = create_app()
except Exception:
    from app import app  # type: ignore
