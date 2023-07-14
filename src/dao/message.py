import boto3
from boto3.dynamodb.conditions import Key
from src.utils.env import AWS_REGION

table_name = "MESSAGES"

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)


def insert_message(message_data):
    table = dynamodb.Table(table_name)
    table.put_item(Item=message_data)


def get_messages_by_chat(chat_id):
    table = dynamodb.Table("MESSAGES")

    # Defina a expressão de filtro para buscar mensagens do chat específico
    filter_expression = Key("chatId").eq(chat_id)

    # Faça a consulta no banco de dados usando o filtro
    response = table.scan(FilterExpression=filter_expression)

    # Obtenha as mensagens retornadas na resposta
    messages = response.get("Items", [])

    return messages
