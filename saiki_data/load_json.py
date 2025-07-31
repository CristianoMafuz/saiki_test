"""
backend/saiki_data/load_json.py

Loads the local .json data to the database system.
"""

import json
from pathlib import Path
from .models import ModelAlgorithm


def load_entities(__rpath: str):
    """Loads a JSON file (with the path specified relatively to this script) into the database, from zero *."""

    # debugging database routing...
    # obj = ModelAlgorithm.objects.using("saiki_data_db").first()
    # print(obj)

    data_path = Path(__file__).resolve().parent / __rpath

    with open(data_path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    # asserting dataset in beforehand.
    for entry in entries:
        if "name" not in entry or "type" not in entry:
            raise ValueError(f"Invalid entry read: {entry}")

        entry["type"] = entry["type"].lower()

        # for instance, only the model algorithm is valid entity...
        if entry["type"] != "algorithm":
            raise NotImplementedError(f"E. Type `{entry["type"]}` isn't supported.")

    # creating the models.
    for eid, entry in enumerate(entries):
        if isinstance(entry["data"]["data_structure"], list):
            # if it is declared as list, then we join it with comma...
            entry["data"]["data_structure"] = ",".join(entry["data"]["data_structure"])
        
        ModelAlgorithm.objects.update_or_create(
            name=entry["name"],
            entity_id=eid,
            defaults={
                "category": entry["data"]["category"],
                "year": entry["data"]["year"],
                "generality": entry["data"]["generality"],
                "data_structure": entry["data"]["data_structure"],
                "temporal_complexity": entry["data"]["average_time_complexity"],
                "spatial_complexity": entry["data"]["auxiliary_space_complexity"],
                "solution_type": entry["data"]["kind_of_solution"]
            }
        )


if __name__ == "__main__":
    # loading the <test.json>.
    load_entities("test.json")
