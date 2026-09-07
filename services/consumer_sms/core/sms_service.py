def build_and_send(event, sender):
    phone_number = event["phone"]
    order_id = event["orderId"]
    amount = event["amount"]
    message = f'{order_id} has been placed for an amount of {amount}'

    sender(phone_number, message)