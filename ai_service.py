def generate_response(message):

    if "refund" in message:
        return "Refund takes 5-7 days",0.9

    if "return" in message:
        return "Return policy is 7 days",0.9

    return "I will connect you to an agent",0.5