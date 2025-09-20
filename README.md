# Mark Twain Travel & Weather AI Workflow

A smart AI-powered workflow application that answers travel-related queries for a community inspired by Mark Twain’s "The Innocents Abroad."  
The system can answer questions about the book, provide current weather for destinations, and combine both sources for comprehensive advice.

---

## Features

- **Semantic Book Search:** Ask anything about Mark Twain’s "The Innocents Abroad" and get context-rich answers from the book.
- **Live Weather Info:** Get current weather for any city using the OpenWeatherMap API.
- **Combined Answers:** For queries about Twain’s travels and current weather, the system combines book insights and live data.
- **LLM-Powered Query Routing:** Uses a Bedrock LLM to classify and route queries to the right data sources.
- **Extensible Workflow:** Modular design for easy extension and integration.

---

## Setup Instructions

### 1. **Clone the Repository**

```bash
git clone <your-repo-url>
cd Assignments/
```

### 2. **Install Dependencies**

It’s recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. **Set Up Environment Variables**

Copy `.env.example` to `.env` and fill in your credentials:



### 4. **Prepare Data**

- Ensure `data/ebook.txt` is present (the full text of "The Innocents Abroad").
- If not, download from [Project Gutenberg](https://www.gutenberg.org/ebooks/3176).

### 5. **Ingest Book Data into ChromaDB**

```bash
python app/store_to_chroma.py
```
This will preprocess the book, generate embeddings and metadata, and store everything in `chroma_data/`.

---

## Usage

### **Run the End-to-End Workflow Test**

```bash
python test_workflow.py
```

You’ll see responses to example queries like:
- "What's the current weather in Paris?"
- "What did Mark Twain think about the Sphinx?"
- "I want to visit the places Twain went to in Italy - what's the weather like there now?"
- "Explain quantum physics"

### **Integrate or Extend**

- Use `app/workflow.py` as the main entry point for your own CLI, API, or UI.

---

## Example Queries & Responses

**Q:** What did Mark Twain think about the Sphinx?  
**A:** Mark Twain was deeply impressed by the Sphinx, as evidenced by his vivid descriptions in "The Innocents Abroad." He marveled at its immense size... [book passage and summary]

**Q:** What's the current weather in Paris?  
**A:** As you explore the enchanting city of Paris... The sky is clear, offering a beautiful backdrop... [live weather details]

**Q:** I want to visit the places Twain went to in Italy - what's the weather like there now?  
**A:** Mark Twain's journey in Italy took him through Milan, Naples... Here’s the current weather for these locations: [weather for each city]

---

## Configuration

- **ChromaDB Data:** Stored in `chroma_data/` (auto-created, gitignored).
- **Book Data:** Place `ebook.txt` in `data/`.
- **Environment Variables:** Use `.env` for all secrets and API keys.

---

## Testing

- Run `test_workflow.py` for end-to-end tests.
- (Optional) Add more tests in a `tests/` directory.

---

## Docker (Optional)

To run in Docker, add a `Dockerfile` like:

```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "test_workflow.py"]
```

---

## Performance & Cost Notes

- **LLM and embedding calls** are the main sources of latency and cost.
- **Batching** and **caching** can reduce costs for repeated queries.
- ChromaDB is fast for vector search; ensure you use persistent storage for large datasets.

---

## Deployment

- Deploy to any cloud platform that supports Python and Docker.
- For a web UI, add a Flask/FastAPI/Streamlit app and expose endpoints.

---

## License

MIT (or as appropriate for your project)

---

## Credits

- Book: ["The Innocents Abroad" by Mark Twain](https://www.gutenberg.org/ebooks/3176)
- Weather: [OpenWeatherMap API](https://openweathermap.org/api)
- Embeddings/LLM: [Amazon Bedrock](https://aws.amazon.com/bedrock/)

---

**For any questions or contributions, please open an issue or pull request!**