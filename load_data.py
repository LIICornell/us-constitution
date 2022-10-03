import json
from pathlib import Path

from models import Constitution


def load_from_json(prefix: str = "") -> Constitution:
    """Load the data from the JSON file."""
    json_file = Path(__file__).parent / "data" / "usconstitution.full.json"
    with open(json_file) as f:
        data = json.load(f)
    if prefix:
        data["path_prefix"] = prefix
    return Constitution(**data)
