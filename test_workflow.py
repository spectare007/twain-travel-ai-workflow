from app.workflow import process_query

def main():
    queries = [
        "What's the current weather in Paris?",
        "What did Mark Twain think about the Sphinx?",
        "I want to visit the places Twain went to in Italy - what's the weather like there now?",
        "Explain quantum physics"
    ]
    print("="*60)
    print("AI Workflow End-to-End Test")
    print("="*60)
    for q in queries:
        print(f"\nUser: {q}\nSystem: {process_query(q)}\n{'-'*40}")

if __name__ == "__main__":
    main()