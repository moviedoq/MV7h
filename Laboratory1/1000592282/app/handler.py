from app.channels import EmailChannel, SMSChannel

def build_chain(channels):
    chain = None
    for ch in reversed(channels):
        if ch == 'email':
            chain = EmailChannel(next_channel=chain)
        elif ch == 'sms':
            chain = SMSChannel(next_channel=chain)
    return chain
