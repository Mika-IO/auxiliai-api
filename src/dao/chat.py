import boto3
from boto3.dynamodb.conditions import Key
from src.utils.env import AWS_REGION

table_name = "CHATS"
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)


def insert_chat(chat_data):
    table = dynamodb.Table(table_name)
    table.put_item(Item=chat_data)


def get_chat(chat_id):
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={"id": chat_id})
    chat_data = response.get("Item")
    return chat_data


def get_chats_by_owner(email):
    table = dynamodb.Table(table_name)
    response = table.scan(FilterExpression=Key("owner").eq(email))
    return response.get("Items")


def delete_chat(chat_id):
    table = dynamodb.Table(table_name)
    table.delete_item(Key={"id": chat_id})
    return True
