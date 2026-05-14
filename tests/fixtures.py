import copy
import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent / "data"


def load_json_fixture(name: str) -> dict[str, Any]:
    path = DATA_DIR / name
    data = json.loads(path.read_text())
    return copy.deepcopy(data)
