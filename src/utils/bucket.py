import boto3
import base64
import tempfile
from botocore.exceptions import ClientError

from botocore.client import Config
from src.utils.env import AWS_REGION, BUCKET_NAME


def send_file(file_extension, file_content, key):
    with tempfile.NamedTemporaryFile(
        suffix=f".{file_extension}", delete=False
    ) as output:
        with open(output.name, "wb") as output_file:
            base64_bytes = file_content.encode("utf-8")
            decoded_data = base64.decodebytes(base64_bytes)
            output_file.write(decoded_data)
            bucket = BUCKET_NAME
            bucket_region = AWS_REGION
            file_key = upload_file_to_s3(output.name, key, bucket, bucket_region)
            if file_key:
                return False, file_key
        return True, None


def upload_file_to_s3(file_name, key, bucket, bucket_region):
    try:
        s3_client = boto3.client("s3", region_name=bucket_region)
        response = s3_client.upload_file(
            file_name,
            bucket,
            key,
            ExtraArgs={
                "ContentType": "application/pdf",
                "ContentDisposition": "inline",
            },
        )
        print(f"Response file upload: {response}")
    except ClientError as e:
        print("Error in put object: %s" % str(e))
        return None
    return key


def generate_presigned_url(bucket_name, file_key):
    s3_client = boto3.client(
        "s3", region_name=AWS_REGION, config=Config(signature_version="s3v4")
    )
    expiration = 604800
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": file_key},
        ExpiresIn=expiration,
    )
    return url
