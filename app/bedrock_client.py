import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def get_bedrock_client():
    """
    Returns a boto3 Bedrock Runtime client using credentials from environment variables.
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_session_token = os.getenv("AWS_SESSION_TOKEN")  # Optional
    region_name = os.getenv("AWS_REGION", "us-east-1")

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name
    )
    return session.client("bedrock-runtime", region_name=region_name)