# bedrock_converse.py

import json
from typing import Dict, Any
from app.bedrock_client import get_bedrock_client

def get_nova_pro_metadata(chunk_text: str) -> Dict[str, Any]:
    import re
    import json
    client = get_bedrock_client()

    prompt = (
        "Given the following text, provide:\n"
        "1. A one-sentence summary.\n"
        "2. A list of locations mentioned (if any).\n"
        "3. A list of people mentioned (if any).\n"
        "Text:\n"
        f"{chunk_text}\n"
        "Respond in JSON with keys: summary, locations, people."
    )

    response = client.converse(
        modelId="us.amazon.nova-pro-v1:0",
        messages=[
            {
                "role": "user",
                "content": [ {"text": prompt} ]
            }
        ],
        inferenceConfig={
            "maxTokens": 256,
            "temperature": 0.2
        }
    )

    output = response["output"]["message"]["content"][0]["text"].strip()

    
    if not output:
        print("Warning: LLM returned empty output for metadata.")
        return {
            "summary": "",
            "locations": [],
            "people": [],
            "llm_error": "Empty output"
        }

    
    try:
        return json.loads(output)
    except Exception:
        pass

    
    match = re.search(r'\{.*\}', output, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass

    
    print(f"Warning: Could not parse metadata for chunk. LLM output:\n{output[:300]}\n")
    return {
        "summary": "",
        "locations": [],
        "people": [],
        "llm_error": "Malformed output",
        "llm_raw": output[:500]
    }

# if __name__ == "__main__":
#     from app.book_preprocess import clean_gutenberg_text, chunk_text_by_paragraph

#     with open("ebook.txt", "r", encoding="utf-8") as f:
#         raw_text = f.read()
#     clean_text = clean_gutenberg_text(raw_text)
#     chunks = chunk_text_by_paragraph(clean_text)

#     for i, chunk in enumerate(chunks[:3]):
#         meta = get_nova_pro_metadata(chunk)
#         meta["chunk_id"] = i
#         meta["text_preview"] = chunk[:60]
#         print(f"Chunk {i} metadata:\n{json.dumps(meta, indent=2)}\n")
#         break