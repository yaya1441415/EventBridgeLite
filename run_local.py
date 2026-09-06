import time
from services.consumer_email.core.email_service import build_and_send
from services.consumer_email.adapters.console_sender import send as console_send
event = {
    "type": "user.signed_up",
    "email": "yahya@toto.com",
    "plan": "superPaid",
}



def send_sms(event):
    raise RuntimeError("SMS Provider down")

def send_email(event):
    build_and_send(event, console_send)

#handlers = [send_email, send_sms]
handlers = [send_sms, send_email]
failed = []


for h in handlers:
    succeed = False
    for attempt in range(3):
        try:
            h(event)
            succeed =True
            break

        except Exception as e:
            print(f"[FAIL] {h.__name__} attempt {attempt + 1}: {e}")
            if attempt < 2:
                time.sleep(2 ** attempt)
                

    if not succeed:
        failed.append((h.__name__, event))


print(f"\nDead letter queue: {failed}")