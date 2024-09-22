import win32evtlog
import time


def log_change(message):
    print(f"{time.ctime()}: {message}")


def monitor_registry():
    server = "localhost"
    logtype = "Security"
    hand = win32evtlog.OpenEventLog(server, logtype)
    flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    print("started")
    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if events:
            for event in events:
                if event.EventID == 4657:  # Event ID for registry changes
                    log_change(f"Registry change detected: {event.StringInserts}")
        time.sleep(5)


if __name__ == "__main__":
    monitor_registry()
