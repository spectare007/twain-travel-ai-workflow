import re

def clean_gutenberg_text(raw_text: str) -> str:
    """
    Remove Project Gutenberg header/footer and return only the main book content.
    Also removes illustrations, footnotes, and normalizes whitespace.
    """
    
    start_match = re.search(r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*\*\*\*", raw_text, re.IGNORECASE)
    end_match = re.search(r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*\*\*\*", raw_text, re.IGNORECASE)

    if not start_match or not end_match:
        raise ValueError("Could not find Project Gutenberg book boundaries.")

    content = raw_text[start_match.end():end_match.start()]
    content = re.sub(r'^\s*CHAPTER[\s\w-]*\n', '', content, flags=re.MULTILINE | re.IGNORECASE)
    content = re.sub(r'\[Illustration:.*?\]', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\[\d+\]', '', content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r'[ \t]+', ' ', content)
    content = content.strip()

    return content

def chunk_text_by_paragraph(text: str, min_words: int = 30, max_words: int = 200, overlap: int = 50) -> list:
    """
    Split text into chunks by paragraph, merging small paragraphs to reach min_words,
    and splitting large ones to not exceed max_words.
    Adds overlap between chunks for better context.
    """
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks = []
    current_chunk = []
    current_word_count = 0

    for para in paragraphs:
        words = para.split()
        if len(words) >= min_words and len(words) <= max_words:
            
            if current_chunk:
                
                prev_words = ' '.join(current_chunk).split()
                if len(prev_words) > overlap:
                    overlap_text = ' '.join(prev_words[-overlap:])
                    chunks.append(overlap_text + ' ' + ' '.join(words))
                else:
                    chunks.append(' '.join(current_chunk) + ' ' + ' '.join(words))
                current_chunk = []
                current_word_count = 0
            else:
                chunks.append(para)
        elif len(words) < min_words:
            
            current_chunk.append(para)
            current_word_count += len(words)
            if current_word_count >= min_words:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_word_count = 0
        else:
            
            for i in range(0, len(words), max_words - overlap):
                chunk = words[i:i+max_words]
                if i != 0:
                    
                    chunk = words[max(i-overlap, 0):i] + chunk
                if len(chunk) >= min_words:
                    chunks.append(' '.join(chunk))
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    
    return [c for c in chunks if len(c.split()) >= min_words]