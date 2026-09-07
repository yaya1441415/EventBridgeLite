import json
import os
from adapters.dynamo_dedupe import DynamoDedupe
from adapters.console_sink import write as console_write
from core.analytics_service import record_event

dedup = DynamoDedupe()
consumer = os.environ["CONSUMER_NAME"]

def handler(event, context):
    for record in event["Records"]:
        envelope = json.loads(record["body"])
        payload = json.loads(envelope["Message"])
        if not dedup.claim(f"{consumer}#{payload['id']}"):
            print("[SKIP] duplicate", payload["id"])
            continue
        record_event(payload, console_write)