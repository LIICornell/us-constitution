import json
from pathlib import Path
from typing import Dict

from usconstitution.models import Constitution


def add_numbers_to_data(data: Dict) -> Dict:
    """Add numbers to the data."""
    for i, article in enumerate(data["articles"]):
        article["index"] = i + 1
        for j, section in enumerate(article["sections"]):
            section["article_number"] = i + 1
            section["index"] = j + 1
            for k, subsection in enumerate(section["clauses"]):
                subsection["article_number"] = i + 1
                subsection["section_number"] = j + 1
                subsection["index"] = k + 1
    for i, amendment in enumerate(data["amendments"]):
        amendment["index"] = i + 1
        for j, clause in enumerate(amendment["clauses"]):
            clause["amendment_number"] = i + 1
            clause["index"] = j + 1
    return data


def load_from_json(prefix: str = "") -> Constitution:
    """Load the data from the JSON file."""
    json_file = Path(__file__).parent / "data" / "usconstitution.full.json"
    with open(json_file) as f:
        data = json.load(f)
    data = add_numbers_to_data(data)
    if prefix:
        data["path_prefix"] = prefix
    return Constitution(**data)
