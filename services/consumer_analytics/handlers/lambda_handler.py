import json

from adapters.console_sink import write as console_write
from core.analytics_service import record_event


def handler(event, context):
    for record in event["Records"]:
        envelope = json.loads(record["body"])
        payload = json.loads(envelope["Message"])
        record_event(payload, console_write)