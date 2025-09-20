import json
from app.bedrock_client import get_bedrock_client

def get_bedrock_embedding(text: str, model_id="amazon.titan-embed-text-v1") -> list:
    """
    Get embedding vector for a single text chunk from Bedrock.
    Returns a list of floats (the embedding vector).
    """
    client = get_bedrock_client()
    
    body = {
        "inputText": text
    }
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(body),
        contentType="application/json"
    )
    result = json.loads(response["body"].read())
    
    return result["embedding"]