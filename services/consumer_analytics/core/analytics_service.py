def record_event(event, sink):
    entry = {
        "event_id": event["id"],
        "event_type": event["type"],
    }
    sink(entry)