def response(message: str, payload: dict, status_code: int = 200):
    return {
        "message": message,
        "status_code": status_code,
        "payload": payload,
    }
