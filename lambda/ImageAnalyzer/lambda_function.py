import boto3
import json
import os

s3 = boto3.client("s3")

BUCKET = os.environ["BUCKET_NAME"]

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)
