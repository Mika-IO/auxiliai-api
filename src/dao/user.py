import boto3
from src.utils.env import AWS_REGION

table_name = "USERS"
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)


def insert_user(user_data):
    table = dynamodb.Table(table_name)
    table.put_item(Item=user_data)


def get_user(email):
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={"email": email})
    user_data = response.get("Item")
    return user_data


def update_user(email, updated_data):
    table = dynamodb.Table(table_name)
    table.update_item(
        Key={"email": email},
        UpdateExpression="SET role = :role, admin_id = :admin_id",
        ExpressionAttributeValues={
            ":role": updated_data["role"],
            ":admin_id": updated_data["admin_id"],
        },
    )


def get_user_password(email):
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={"email": email}, ProjectionExpression="hashed_password"
    )
    item = response.get("Item")
    if item:
        return item.get("hashed_password")
    else:
        return None
