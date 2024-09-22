import json
import winreg
from datetime import datetime


# Function to recursively fetch registry keys and values
def fetch_registry_values(key, path):
    registry_entries = []

    try:
        # Enumerate values in the current registry key
        j = 0
        while True:
            try:
                value_name, value_data, value_type = winreg.EnumValue(key, j)
                registry_entries.append(
                    {
                        "path": path,
                        "value_name": value_name,
                        "value_data": str(value_data),
                        "value_type": value_type,
                    }
                )
                j += 1
            except OSError:
                # No more values to enumerate
                break

        # Enumerate subkeys in the current registry key
        i = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(key, i)
                subkey_path = path + "\\" + subkey_name
                with winreg.OpenKey(key, subkey_name) as subkey:
                    registry_entries.extend(fetch_registry_values(subkey, subkey_path))
                i += 1
            except OSError:
                # No more subkeys to enumerate
                break

    except Exception as e:
        print(f"Error: {e}")

    return registry_entries


# Main function to dump the entire registry in flat format
def main():
    try:
        # Root keys to iterate through
        root_keys = {
            "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
            "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
            "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
            "HKEY_USERS": winreg.HKEY_USERS,
            "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
        }

        all_registry_entries = []

        # Iterate through all root keys
        for root_name, root in root_keys.items():
            print(f"Processing {root_name}...")
            root_path = root_name
            all_registry_entries.extend(
                fetch_registry_values(winreg.OpenKey(root, ""), root_path)
            )

        # Generate timestamp for the filename
        timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
        filename = f"registry_snapshot_{timestamp}.json"

        # Save to JSON file with timestamp
        with open(filename, "w") as json_file:
            json.dump(all_registry_entries, json_file, indent=4)

        print(f"Registry saved to {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
