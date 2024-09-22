import json


def load_registry_snapshot(filepath):
    """Load registry snapshot from a JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading registry snapshot {filepath}: {e}")
        return []


def compare_registry_data(current_data, baseline_data):
    """Compare the current registry data with baseline data."""
    differences = []

    # Convert both datasets into dictionaries for easier comparison
    baseline_dict = {
        f"{item['path']}|{item['value_name']}": item for item in baseline_data
    }
    current_dict = {
        f"{item['path']}|{item['value_name']}": item for item in current_data
    }

    # Find differences
    for key, current_item in current_dict.items():
        if key in baseline_dict:
            baseline_item = baseline_dict[key]
            if current_item["value_data"] != baseline_item["value_data"]:
                differences.append(
                    {
                        "type": "MODIFIED",
                        "path": current_item["path"],
                        "value_name": current_item["value_name"],
                        "old_value": baseline_item["value_data"],
                        "new_value": current_item["value_data"],
                    }
                )
        else:
            differences.append(
                {
                    "type": "NEW",
                    "path": current_item["path"],
                    "value_name": current_item["value_name"],
                    "new_value": current_item["value_data"],
                }
            )

    # Find deleted keys
    for key, baseline_item in baseline_dict.items():
        if key not in current_dict:
            differences.append(
                {
                    "type": "DELETED",
                    "path": baseline_item["path"],
                    "value_name": baseline_item["value_name"],
                    "old_value": baseline_item["value_data"],
                }
            )

    return differences


def main():
    baseline_file = r""
    current_file = r""

    baseline_data = load_registry_snapshot(baseline_file)
    current_data = load_registry_snapshot(current_file)

    differences = compare_registry_data(current_data, baseline_data)

    if differences:
        print("Differences found:")
        for diff in differences:
            if diff["type"] == "MODIFIED":
                print(
                    f"MODIFIED: {diff['path']}\\{diff['value_name']}, Old: {diff['old_value']}, New: {diff['new_value']}"
                )
            elif diff["type"] == "NEW":
                print(
                    f"NEW: {diff['path']}\\{diff['value_name']}, New Value: {diff['new_value']}"
                )
            elif diff["type"] == "DELETED":
                print(
                    f"DELETED: {diff['path']}\\{diff['value_name']}, Old Value: {diff['old_value']}"
                )
    else:
        print("No differences found.")


if __name__ == "__main__":
    main()
