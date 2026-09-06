from services.consumer_email.core.email_service import build_and_send


def test_email_uses_plan():
    sent = []

    def fake_sender(to, subject, body):
        sent.append((to, subject, body))

    event = {"type": "user.signed_up", "email": "a@b.com", "plan": "free"}
    build_and_send(event, fake_sender)
    

    assert len(sent) == 1
    assert sent[0][0] == "a@b.com"
    assert "free" in sent[0][2]

