import uuid

from src.utils.api_utils import is_body_valid, response

from src.dao.user import insert_user, get_user
from src.utils.security import (
    generate_hashed_password,
    verify_password,
    generate_jwt_token,
)
from chalice import Blueprint

auth = Blueprint(__name__)

# - POST -> SignUp


@auth.route("/signup", methods=["POST"], cors=True)
def create_user():
    body = auth.current_request.json_body

    required_fields = ["email", "password", "role"]
    is_valid, message = is_body_valid(body, required_fields)

    if not is_valid:
        return response(message, {}, status_code=400)

    existing_user = get_user(body["email"])
    if existing_user:
        return response("email already exists", {}, status_code=400)

    user_id = str(uuid.uuid4())
    hashed_password = generate_hashed_password(body["password"])

    if body.get("role") == "admin":
        role = body["role"]
        admin_id = user_id
    else:
        role = "basic"
        if not body.get("admin_id"):
            return response("admin_id is required", {}, status_code=400)
        admin_id = body["admin_id"]

    user_data = {
        "id": user_id,
        "email": body["email"],
        "role": role,
        "admin_id": admin_id,
        "credits": 10,
        "hashed_password": hashed_password,
    }
    insert_user(user_data)
    return response("user created successfully")


# - POST -> SignIn


@auth.route("/signin", methods=["POST"], cors=True)
def create_token():
    body = auth.current_request.json_body

    required_fields = ["email", "password"]
    is_valid, message = is_body_valid(body, required_fields)

    if not is_valid:
        return response(message, {}, status_code=400)
    email = body["email"]
    password = body["password"]

    user = get_user(body["email"])
    if not user:
        return response("user does not exists", {}, status_code=400)

    hashed_password = user["hashed_password"]
    if not verify_password(email, password, hashed_password):
        return response("invalid password", {}, status_code=400)

    token = generate_jwt_token(email)
    return response("success", {"token": token}, status_code=200)
