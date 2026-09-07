from core.email_service import build_and_send
from adapters.console_sender import send as console_send
import json

def handler(event, context):
    for record in event["Records"]:
        envelope = json.loads(record["body"])
        payload = json.loads(envelope["Message"])
        build_and_send(payload, console_send)



