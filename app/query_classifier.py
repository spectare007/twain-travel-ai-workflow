from app.bedrock_client import get_bedrock_client

def classify_query_llm(query: str) -> str:
    """
    Classify a user query as 'book', 'weather', 'both', or 'out-of-scope' using a Bedrock LLM.
    Returns the label as a string.
    """
    client = get_bedrock_client()
    prompt = (
    "You are an intelligent travel assistant for a community inspired by Mark Twain's 'The Innocents Abroad.'\n"
    "Your job is to classify user queries so the system can decide which data sources to use for generating a response.\n"
    "The system has access to:\n"
    "- The full text of 'The Innocents Abroad' by Mark Twain (for literary, historical, or travel-related questions about Twain's journeys, opinions, or experiences).\n"
    "- The OpenWeatherMap API (for current weather information about any city or location).\n"
    "\n"
    "Classify the following user query as one of these four categories:\n"
    "1. book — if the query is about Mark Twain, his travels, his opinions, or anything that can be answered from 'The Innocents Abroad.'\n"
    "2. weather — if the query is about the current weather, temperature, or forecast for a specific place, and does not require information from the book.\n"
    "3. both — if the query requires information from both the book and the weather API (for example, asking about places Twain visited and the current weather there).\n"
    "4. out-of-scope — if the query is unrelated to Mark Twain, his travels, or the weather (for example, questions about quantum physics or unrelated topics).\n"
    "\n"
    "Return only the label: book, weather, both, or out-of-scope.\n"
    "\n"
    "Here is the user query:\n"
    f'"{query}"'
)
    response = client.converse(
        modelId="us.amazon.nova-pro-v1:0",  # Replace with your Bedrock LLM model ID if different
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 10, "temperature": 0}
    )
    label = response["output"]["message"]["content"][0]["text"].strip().lower()
    
    if label not in {"book", "weather", "both", "out-of-scope"}:
        label = "out-of-scope"
    return label