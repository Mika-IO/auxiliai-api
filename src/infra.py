import boto3


s3 = boto3.client("s3")
dynamodb = boto3.client("dynamodb")


def create_s3_bucket(stage, resource):
    bucket_name = "nome_do_seu_bucket"
    print(f"Creating s3 bucket {bucket_name} !")
    response = s3.create_bucket(Bucket=bucket_name)
    print(response)
    print(f"-------- END {bucket_name} --------")


def create_dynamodb_table(stage, resource):
    table_name = f"{stage}-{resource}"
    print(f"Creating DynamoDB table {table_name} !")
    reponse = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "N"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    print(reponse)
    print(f"-------- END {table_name} --------")
