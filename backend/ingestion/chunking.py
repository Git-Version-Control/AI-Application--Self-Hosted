from transformers import AutoTokenizer

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/LaBSE")

def chunk_text(text, max_length=512):
    tokens = tokenizer.encode(text, truncation=False)
    chunks = []
    for i in range(0, len(tokens), max_length):
        chunk = tokens[i:i + max_length]
        chunks.append(chunk)
    return [tokenizer.decode(chunk) for chunk in chunks]

# Example text
text = "A very long document..."  # Add your long text here
chunks = chunk_text(text)
for idx, chunk in enumerate(chunks):
    print(f"Chunk {idx+1}: {chunk}")