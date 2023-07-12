from chalice import Chalice

app = Chalice(app_name="auxiliAI")


# - POST -> SignUp


@app.route("/signup", methods=["POST"])
def create_user():
    body = app.current_request.json_body
    return {"user": body}


# - POST -> SignIn


@app.route("/signin", methods=["POST"])
def create_token():
    body = app.current_request.json_body
    token = "798nd8uynsdihjuhkjh"
    return {"token": token}


# - POST -> Chat


@app.route("/chat", methods=["POST"])
def create_chat():
    body = app.current_request.json_body
    return {"chat": body}


# - POST -> Message


@app.route("/message", methods=["POST"])
def create_message():
    body = app.current_request.json_body
    return {"message": body}


# - GET -> Chats


@app.route("/chats/{email}")
def get_chats(email):
    return {
        "email": email,
        "chats": [],
    }


# - GET -> Messages


@app.route("/messages/{email}/{chat_id}")
def get_messages(email, chat_id):
    return {
        "email": email,
        "chat_id": chat_id,
        "messages": [],
    }


# - DELETE -> Chat


@app.route("/chat/{chat_id}", methods=["DELETE"])
def delete_chat(chat_id):
    return {"http-method": app.current_request.method, "chat_id": chat_id}
