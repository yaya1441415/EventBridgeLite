def build_and_send(event, sender):
    to = event["email"]
    subject = "Welcome to the app"
    body = f"Hi, your {event['plan']} account is ready."

    sender(to, subject, body)