import boto3
from app.core.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    S3_BUCKET_NAME,
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)


def upload_file_to_s3(file_obj, s3_key: str, content_type: str):
    s3_client.upload_fileobj(
        file_obj,
        S3_BUCKET_NAME,
        s3_key,
        ExtraArgs={
            "ContentType": content_type,
        },
    )

    return f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"


def delete_file_from_s3(s3_key: str):
    s3_client.delete_object(
        Bucket=S3_BUCKET_NAME,
        Key=s3_key,
    )