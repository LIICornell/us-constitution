import json
from pathlib import Path
from typing import Dict

from usconstitution.models import Constitution


def add_numbers_to_provision(provision: Dict, index: int) -> Dict:
    if provision.get("sections"):
        for j, section in enumerate(provision["sections"]):
            section["article_number"] = index
            section["index"] = j + 1
            if section.get("clauses"):
                for k, subsection in enumerate(section["clauses"]):
                    subsection["article_number"] = index
                    subsection["section_number"] = j + 1
                    subsection["index"] = k + 1
    if provision.get("clauses"):
        for j, clause in enumerate(provision["clauses"]):
            clause["article_number"] = index
            clause["index"] = j + 1
    return provision


def add_numbers_to_data(data: Dict) -> Dict:
    """Add numbers to the data."""
    for i, article in enumerate(data["articles"]):
        article["index"] = i + 1
        add_numbers_to_provision(article, i + 1)
    for i, amendment in enumerate(data["amendments"]):
        amendment["index"] = i + 1
        add_numbers_to_provision(amendment, i + 1)
    return data


def flatten_content_in_clauses(amendment: Dict) -> Dict:
    if amendment.get("clauses"):
        amendment["content"] = " ".join(
            clause["content"][0] for clause in amendment.pop("clauses")
        )
    if amendment.get("sections"):
        for section in amendment["sections"]:
            section = flatten_content_in_clauses(section)
    return amendment


def load_from_json(prefix: str = "") -> Constitution:
    """Load the data from the JSON file."""
    json_file = Path(__file__).parent / "data" / "usconstitution.full.json"
    with open(json_file) as f:
        data = json.load(f)
    data = add_numbers_to_data(data)
    if prefix:
        data["path_prefix"] = prefix
    data["amendments"] = [
        flatten_content_in_clauses(amendment) for amendment in data["amendments"]
    ]
    return Constitution(**data)
