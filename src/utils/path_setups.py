
import sys
from pathlib import Path


def path_setups() -> None:
    src_path = Path(__file__).resolve().parent.parent
    sys.path.append(str(src_path))
