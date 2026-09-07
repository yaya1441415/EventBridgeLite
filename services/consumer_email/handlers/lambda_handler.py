import json
import os
from core.email_service import build_and_send
from adapters.console_sender import send as console_send
from adapters.dynamo_dedupe import DynamoDedupe

dedup = DynamoDedupe()
consumer = os.environ["CONSUMER_NAME"]

def handler(event, context):
    for record in event["Records"]:
        envelope = json.loads(record["body"])
        payload = json.loads(envelope["Message"])
        if not dedup.claim(f"{consumer}#{payload['id']}"):
            print("[SKIP] duplicate", payload["id"])
            continue
        build_and_send(payload, console_send)




