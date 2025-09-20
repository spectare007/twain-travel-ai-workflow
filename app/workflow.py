import os
from app.query_classifier import classify_query_llm
from app.query_book import search_book
from app.weather_query import get_weather_by_city
from app.bedrock_client import get_bedrock_client
from app.chroma_utils import connect_to_chromadb
from app.bedrock_embed import get_bedrock_embedding


def extract_cities_from_book(query: str) -> list:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CHROMA_DIR = os.path.join(PROJECT_ROOT, "chroma_data")
    COLLECTION_NAME = "innocents_abroad"
    client = connect_to_chromadb(CHROMA_DIR)
    collection = client.get_collection(COLLECTION_NAME)
    query_embedding = get_bedrock_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=['metadatas']
    )
    cities = set()
    for meta in results["metadatas"][0]:
        locs = meta.get("locations", "")
        
        for loc in locs.split(","):
            city = loc.strip()
            if city and city.lower() not in {"italy", "europe"}:
                cities.add(city)
    return list(cities)

def extract_location(query: str) -> str:
    """
    Dummy location extractor. Replace with a smarter NER/location parser if needed.
    """
    import re
    match = re.search(r"(?:in|at|for|of)\s+([A-Za-z\s]+)", query)
    if match:
        return match.group(1).strip()
    return "Paris"  

def generate_final_response(query: str, book_answer: str = "", weather_answer: str = "") -> str:
    """
    Use Bedrock LLM to generate a final, user-friendly response based on the query and retrieved data.
    """
    client = get_bedrock_client()
    
    prompt = (
        "You are an intelligent travel assistant for a community inspired by Mark Twain's 'The Innocents Abroad.'\n"
        "Given the user's query and the following information retrieved from the book and/or weather API, generate a helpful, concise, and context-aware response for the user.\n"
        "If both book and weather information are provided, combine them naturally in your answer.\n"
        "\n"
        f"User Query: {query}\n"
        f"Book Information: {book_answer}\n"
        f"Weather Information: {weather_answer}\n"
        "\n"
        "Response:"
    )
    response = client.converse(
        modelId="us.amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 256, "temperature": 0.3}
    )
    return response["output"]["message"]["content"][0]["text"].strip()

def process_query(query: str) -> str:
    label = classify_query_llm(query)
    if label == "book":
        book_answer = search_book(query)
        return generate_final_response(query, book_answer=book_answer)
    elif label == "weather":
        location = extract_location(query)
        weather_answer = get_weather_by_city(location)
        return generate_final_response(query, weather_answer=weather_answer)
    elif label == "both":
        
        cities = extract_cities_from_book(query)
        book_answer = search_book(query)
        weather_answers = []
        for city in cities:
            weather = get_weather_by_city(city)
            weather_answers.append(f"Weather in {city}:\n{weather}")
        weather_answer = "\n\n".join(weather_answers) if weather_answers else "No specific cities found for weather lookup."
        return generate_final_response(query, book_answer=book_answer, weather_answer=weather_answer)
    else:
        return "Sorry, I can only answer questions about Mark Twain's travels or the weather."

