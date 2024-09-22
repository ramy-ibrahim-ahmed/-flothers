import os
import winreg
import time
from datetime import datetime
import json
import base64


def collect_registry_keys(hive, path):
    try:
        reg = winreg.ConnectRegistry(None, hive)
        try:
            key = winreg.OpenKey(reg, path)
        except OSError as e:
            print(f"Error accessing registry key {path}: {e}")
            return [], []

        keys = []
        values = []
        i = 0
        while True:
            try:
                subkey = winreg.EnumKey(key, i)
                keys.append(subkey)
                i += 1
            except OSError:
                break

        i = 0
        while True:
            try:
                value = winreg.EnumValue(key, i)
                # Convert binary data to base64 for JSON serialization
                value_data = value[1]
                if isinstance(value_data, bytes):
                    value_data = base64.b64encode(value_data).decode(
                        "utf-8"
                    )  # Convert bytes to base64 string

                values.append((value[0], value_data, value[2]))
                i += 1
            except OSError:
                break

        winreg.CloseKey(key)
        return keys, values
    except Exception as e:
        print(f"Error accessing registry: {e}")
        return [], []


def save_registry_data(data, folder):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    filename = f"registry_snapshot_{timestamp}.json"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=4)


def flatten_registry_data(data):
    flattened_data = []
    for path, values in data.items():
        for value in values["values"]:
            flattened_entry = {
                "path": path,
                "value_name": value[0],
                "value_data": value[1],
                "value_type": value[2],
            }
            flattened_data.append(flattened_entry)
    return flattened_data


def main():
    registry_hives = {
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
    }

    # Add additional registry paths here
    registry_paths = [
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
        r"Software\Microsoft\Windows\CurrentVersion\Policies",
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"Software\Microsoft\Windows NT\CurrentVersion\Windows",
        r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon",
        r"Software\Microsoft\Windows\CurrentVersion\Group Policy",
        # r"SYSTEM\CurrentControlSet\Services\EventLog\Security",
        # r"Software\Policies\Microsoft\Windows\System",
        # r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
        # r"SYSTEM\CurrentControlSet\Services\LanmanServer\Shares",
        # r"SYSTEM\CurrentControlSet\Control\Session Manager",
        # r"SYSTEM\CurrentControlSet\Control\Lsa",
        # r"SYSTEM\CurrentControlSet\Services\W32Time\Parameters",
    ]

    while True:
        collected_data = {}
        for hive_name, hive in registry_hives.items():
            for path in registry_paths:
                keys, values = collect_registry_keys(hive, path)
                collected_data[f"{hive_name}\\{path}"] = {
                    "keys": keys,
                    "values": values,
                }

        flattened_data = flatten_registry_data(collected_data)

        folder = "registry_snapshots"
        save_registry_data(flattened_data, folder)

        print(f"Registry data collected and saved to {folder}")

        time.sleep(10)  # Sleep for 10 seconds


if __name__ == "__main__":
    main()
