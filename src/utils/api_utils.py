def response(message: str, payload: dict = {}, status_code: int = 200):
    return {
        "message": message,
        "status_code": status_code,
        "payload": payload,
    }


def is_body_valid(body, required_fields):
    for field in required_fields:
        if field not in body or not body[field]:
            return False, f"{field} is required"
    return True, "Perfect! My boy!"
