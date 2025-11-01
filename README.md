# KEITH LeakProof Drive RAG System

A complete Retrieval-Augmented Generation (RAG) system for querying technical documentation about the KEITH LeakProof Drive using OpenAI's API.

## Features

- ✅ **Document Processing**: Semantic chunking of technical documentation
- ✅ **Vector Embeddings**: Using OpenAI's text-embedding-3-small model
- ✅ **Semantic Search**: Cosine similarity-based retrieval
- ✅ **Context-Aware Responses**: GPT-4 powered answers with source citations
- ✅ **Persistent Index**: Save and load embeddings for faster startup
- ✅ **Interactive Mode**: Ask questions in real-time

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key

You need an OpenAI API key to use this system. Get one at [platform.openai.com](https://platform.openai.com/api-keys)

**Option A: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

**Option B: Create a .env file**
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

**Option C: Pass directly in code**
```python
rag = LeakProofRAG(api_key="your-api-key-here")
```

## Usage

### Basic Usage

```python
from leakproof_rag import LeakProofRAG

# Initialize the RAG system
rag = LeakProofRAG()

# Load document and create embeddings
rag.load_document("leakproof_drive.pdf")
rag.create_embeddings()

# Query the system
result = rag.query("What is the unloading time at 25 gallons per minute?")
print(result['answer'])
```

### Run the Demo

```bash
python leakproof_rag.py
```

This will:
1. Initialize the RAG system
2. Process the document and create embeddings
3. Run example queries
4. Enter interactive mode for custom questions

### Example Queries

- "What is the unloading time for a 45-foot trailer at 25 gallons per minute?"
- "What types of waste is the LeakProof Drive designed for?"
- "What are the key features of the hydraulic cylinder design?"
- "What is the maximum working pressure?"
- "How do I contact KEITH Manufacturing in Europe?"

## How It Works

### 1. Document Processing
The PDF is split into semantic chunks with metadata:
- Overview and introduction
- Applications and use cases
- Technical specifications
- Performance data (by pump flow rate)
- Feature descriptions
- Contact information

### 2. Embedding Creation
Each chunk is converted to a vector embedding using OpenAI's `text-embedding-3-small` model (1536 dimensions).

### 3. Query Processing
When you ask a question:
1. Your question is converted to an embedding
2. System finds the most similar chunks using cosine similarity
3. Top K chunks are retrieved (default: 3)
4. Chunks are passed as context to GPT-4
5. GPT-4 generates an answer based on the context

### 4. Response Generation
The system uses GPT-4o-mini with:
- Temperature: 0.3 (for consistent, factual responses)
- System prompt: Technical expert persona
- Context: Retrieved documentation chunks

## Code Structure

```python
class LeakProofRAG:
    __init__()              # Initialize with OpenAI API
    load_document()         # Load and chunk the PDF
    create_embeddings()     # Generate vector embeddings
    retrieve_relevant_chunks()  # Find similar content
    generate_response()     # Get GPT-4 answer
    query()                 # Main method: retrieve + generate
    save_index()           # Persist embeddings
    load_index()           # Load saved embeddings
```

## Advanced Usage

### Save and Load Index

Save embeddings to avoid recreating them:

```python
# First run - create and save
rag = LeakProofRAG()
rag.load_document("leakproof_drive.pdf")
rag.create_embeddings()
rag.save_index("leakproof_index.json")

# Subsequent runs - load from file
rag = LeakProofRAG()
rag.load_index("leakproof_index.json")
result = rag.query("Your question here")
```

### Customize Retrieval

```python
# Retrieve more chunks for complex queries
result = rag.query("Complex question", top_k=5)

# Hide source information
result = rag.query("Your question", show_sources=False)
```

### Access Raw Results

```python
result = rag.query("What is the cylinder bore size?")

print(result['question'])   # Original question
print(result['answer'])     # Generated answer
print(result['sources'])    # Retrieved chunks with similarity scores
```

## Cost Estimation

Approximate costs per query (as of 2024):
- **Embeddings**: $0.00002 per query (1 query embedding)
- **Generation**: $0.0001-0.0003 per query (GPT-4o-mini)
- **Total**: ~$0.0003 per query

Initial setup (embedding all chunks): ~$0.0003

## Customization

### Change the LLM Model

```python
# In the __init__ method
self.chat_model = "gpt-4o"  # For more accurate responses
# or
self.chat_model = "gpt-3.5-turbo"  # For lower cost
```

### Adjust Response Style

Modify the `system_prompt` in `generate_response()` method:

```python
system_prompt = """You are a friendly sales assistant for KEITH products.
Be enthusiastic and focus on highlighting the benefits and applications..."""
```

### Add More Documents

To extend this to multiple documents:

```python
def load_multiple_documents(self, pdf_paths: List[str]):
    all_chunks = []
    for pdf_path in pdf_paths:
        chunks = self._extract_chunks_from_pdf(pdf_path)
        all_chunks.extend(chunks)
    self.chunks = all_chunks
```

## Troubleshooting

### "API key is required" error
Make sure your OpenAI API key is set:
```bash
export OPENAI_API_KEY='your-key-here'
```

### "Rate limit exceeded" error
You're making too many requests. Add a delay:
```python
import time
time.sleep(1)  # Wait 1 second between queries
```

### Poor answer quality
Try:
- Increasing `top_k` to retrieve more context
- Using a more powerful model (gpt-4o instead of gpt-4o-mini)
- Adjusting the temperature (lower = more focused)

## Next Steps

To enhance this RAG system:

1. **Better PDF Processing**: Use `pypdf2` or `pdfplumber` for automatic text extraction
2. **Vector Database**: Integrate Pinecone, Weaviate, or ChromaDB for scaling
3. **Hybrid Search**: Combine semantic search with keyword matching
4. **Re-ranking**: Add a re-ranking step after initial retrieval
5. **Multi-document**: Support multiple product manuals
6. **Streaming**: Stream responses for better UX
7. **Chat History**: Add conversation memory
8. **Web Interface**: Build a Streamlit or Gradio UI

## License

This is a demonstration project for educational purposes.

## Contact

For questions about the KEITH LeakProof Drive product:
- Website: www.keithwalkingfloor.com
- Email: sales@keithwalkingfloor.com

For questions about this RAG implementation:
- Review the code comments
- Check OpenAI's documentation
