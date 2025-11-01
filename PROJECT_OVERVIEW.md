# LeakProof Drive RAG System - Project Overview

## 📦 What You've Got

A complete, production-ready RAG (Retrieval-Augmented Generation) system that lets you query the KEITH LeakProof Drive technical documentation using natural language.

## 🎯 What It Does

- **Understands Questions**: Ask technical questions in plain English
- **Finds Relevant Info**: Searches through the document using AI-powered semantic search
- **Generates Answers**: Uses GPT-4 to create accurate, contextual responses
- **Tracks Sources**: Shows which parts of the document informed each answer

## 📁 Files Included

### Core System
- **leakproof_rag.py** (14KB) - Main RAG system with all functionality
- **requirements.txt** (49B) - Python dependencies

### Example Scripts
- **simple_example.py** (1.3KB) - Minimal example to get started fast
- **advanced_example.py** (7.5KB) - Shows advanced features like conversation history
- **test_rag.py** (5.8KB) - Test suite to verify everything works

### Documentation
- **README.md** (6.5KB) - Comprehensive documentation
- **QUICKSTART.md** (2.1KB) - Get running in 5 minutes
- **.env.example** - Template for API key configuration

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip install openai numpy python-dotenv
```

### 2. Set API Key
```bash
export OPENAI_API_KEY='your-openai-api-key'
```

### 3. Run It
```bash
python simple_example.py
```

## 💡 Example Usage

```python
from leakproof_rag import LeakProofRAG

# Initialize
rag = LeakProofRAG()
rag.load_document("leakproof_drive.pdf")
rag.create_embeddings()

# Ask questions
result = rag.query("What is the unloading time at 25 gallons per minute?")
print(result['answer'])
# Output: "At 25 gallons per minute, the floor speed is 6.25 ft/minute 
#          and the unloading time for a 45 ft trailer is 7.2 minutes."
```

## ✨ Key Features

### 1. Semantic Search
- Converts text to vector embeddings
- Finds relevant information using similarity search
- Returns the most relevant document sections

### 2. Context-Aware Responses
- Feeds relevant sections to GPT-4
- Generates natural, accurate answers
- Cites sources for transparency

### 3. Performance Optimized
- Save/load embeddings to avoid recomputation
- Efficient cosine similarity calculation
- ~$0.0003 per query

### 4. Extensible Design
- Easy to add more documents
- Customizable prompts and models
- Modular architecture

## 🎓 What You Can Learn

This project demonstrates:

1. **RAG Architecture**: How to combine retrieval and generation
2. **Vector Embeddings**: Converting text to numerical representations
3. **Semantic Search**: Finding similar content using cosine similarity
4. **Prompt Engineering**: Crafting effective prompts for LLMs
5. **OpenAI API**: Practical integration with embeddings and chat APIs

## 🔧 Customization Options

### Change the Model
```python
self.chat_model = "gpt-4o"  # More accurate
# or
self.chat_model = "gpt-3.5-turbo"  # Cheaper
```

### Adjust Retrieval
```python
# Retrieve more context for complex queries
result = rag.query("Complex question", top_k=5)
```

### Modify Behavior
```python
# Edit system_prompt in generate_response() method
system_prompt = "You are a sales assistant..."
```

## 📊 How It Works

```
User Question
     ↓
Convert to Embedding (OpenAI API)
     ↓
Compare with Document Embeddings (Cosine Similarity)
     ↓
Retrieve Top K Most Similar Chunks
     ↓
Feed to GPT-4 as Context
     ↓
Generate Answer
     ↓
Return to User
```

## 🎯 Use Cases

This RAG system can be adapted for:
- **Technical Documentation**: Product manuals, spec sheets
- **Customer Support**: FAQ automation
- **Internal Knowledge Base**: Company wikis, policies
- **Research Papers**: Academic literature search
- **Legal Documents**: Contract analysis
- **Medical Records**: Patient information retrieval

## 🔐 Cost & Performance

### Per Query
- Embedding: ~$0.00002
- GPT-4o-mini: ~$0.0001-0.0003
- **Total: ~$0.0003 per query**

### Initial Setup
- One-time embedding cost: ~$0.0003

### Speed
- Query + response: 2-5 seconds
- With saved index: <3 seconds

## 🚧 Next Steps to Enhance

1. **Add More Documents**: Expand knowledge base
2. **Web Interface**: Build with Streamlit/Gradio
3. **Better PDF Parsing**: Use pdfplumber for complex PDFs
4. **Vector Database**: Scale with Pinecone/Weaviate
5. **Hybrid Search**: Combine semantic + keyword search
6. **Conversation Memory**: Multi-turn dialogues
7. **Streaming Responses**: Real-time answer generation
8. **Fine-tuning**: Custom model for specific domain

## 📝 Testing

Run the test suite to verify everything works:
```bash
python test_rag.py
```

This will check:
- ✅ All dependencies installed
- ✅ API key configured
- ✅ System initialization
- ✅ Document loading
- ✅ Embedding creation
- ✅ Query execution
- ✅ Save/load functionality

## 🤝 Support

### For RAG System Issues
- Check README.md for detailed documentation
- Review QUICKSTART.md for common setup issues
- Ensure OpenAI API key is valid and has credits

### For KEITH Product Questions
- Website: www.keithwalkingfloor.com
- Email: sales@keithwalkingfloor.com
- Phone: (541) 475-3802

## 🎉 You're Ready!

You now have a complete, working RAG system. Start with simple_example.py and explore from there!

Key commands:
```bash
python simple_example.py      # Quick start
python leakproof_rag.py        # Full demo + interactive
python advanced_example.py     # Advanced features
python test_rag.py             # Verify installation
```

Happy querying! 🚀
