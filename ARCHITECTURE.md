# System Architecture

## RAG System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│                                                                  │
│  "What is the unloading time at 25 gallons per minute?"        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LEAKPROOF RAG SYSTEM                          │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. QUERY PROCESSING                                      │  │
│  │    - Receive user question                               │  │
│  │    - Convert to embedding vector (1536 dimensions)       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 2. SEMANTIC SEARCH                                       │  │
│  │    - Compare query embedding with document embeddings    │  │
│  │    - Calculate cosine similarity scores                  │  │
│  │    - Rank chunks by relevance                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 3. RETRIEVAL                                            │  │
│  │    - Select top K most relevant chunks (default: 3)     │  │
│  │    - Extract chunk text and metadata                    │  │
│  │    - Prepare context for LLM                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 4. GENERATION                                           │  │
│  │    - Feed retrieved chunks to GPT-4o-mini              │  │
│  │    - Apply system prompt (technical expert persona)    │  │
│  │    - Generate contextual answer                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
└─────────────────────────────┼───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         RESPONSE                                 │
│                                                                  │
│  "At 25 gallons per minute, the floor speed is 6.25 ft/minute  │
│   and the unloading time for a 45 ft trailer is 7.2 minutes."  │
└─────────────────────────────────────────────────────────────────┘
```

## Document Processing Pipeline

```
┌─────────────────┐
│   PDF Document  │
│ (LeakProof.pdf) │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     Text Extraction                 │
│  - Parse PDF structure              │
│  - Extract text content             │
│  - Preserve formatting              │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     Semantic Chunking               │
│  - Split by logical sections        │
│  - Preserve context                 │
│  - Add metadata                     │
│                                     │
│  Chunks created:                    │
│  • Overview                         │
│  • Applications                     │
│  • Features                         │
│  • Specifications                   │
│  • Performance data                 │
│  • Contact info                     │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     Embedding Generation            │
│  (OpenAI text-embedding-3-small)   │
│                                     │
│  Input: "Hydraulic Drive Unit..."   │
│  Output: [0.123, -0.456, 0.789...] │
│         (1536 dimensions)           │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     Vector Storage                  │
│  - Store embeddings in memory       │
│  - Index for fast retrieval         │
│  - Optional: Save to disk           │
└─────────────────────────────────────┘
```

## Data Flow: Query to Answer

```
User Query: "What is the maximum pressure?"
                    │
                    ▼
         ┌──────────────────┐
         │   Embedding API   │
         │   OpenAI          │
         └──────────────────┘
                    │
         Vector: [0.89, -0.12, ...]
                    │
                    ▼
         ┌──────────────────────────┐
         │   Similarity Search       │
         │   (Cosine Similarity)     │
         └──────────────────────────┘
                    │
         ┌──────────┴───────────┬──────────┐
         ▼                      ▼          ▼
    ┌────────┐            ┌────────┐  ┌────────┐
    │Chunk 1 │            │Chunk 2 │  │Chunk 3 │
    │ 0.92   │            │ 0.87   │  │ 0.81   │
    └────────┘            └────────┘  └────────┘
         │                      │          │
         └──────────┬───────────┘          │
                    ▼                      │
         ┌──────────────────────┐          │
         │  Selected Context     │          │
         │  (Top 3 chunks)       │◄─────────┘
         └──────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │   GPT-4o-mini         │
         │   Chat Completion     │
         └──────────────────────┘
                    │
                    ▼
         "The maximum working pressure
          is 3000 PSI (210 bar)."
```

## Component Interaction

```
┌───────────────────────────────────────────────────────────┐
│                    LeakProofRAG Class                      │
├───────────────────────────────────────────────────────────┤
│                                                            │
│  Components:                                               │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────┐ │
│  │   Document     │  │   Embeddings   │  │   OpenAI    │ │
│  │   Chunks       │  │   Storage      │  │   Client    │ │
│  │                │  │                │  │             │ │
│  │ • List[Dict]   │  │ • List[Vector] │  │ • API Key   │ │
│  │ • Metadata     │  │ • Indexed      │  │ • Models    │ │
│  └────────────────┘  └────────────────┘  └─────────────┘ │
│                                                            │
│  Methods:                                                  │
│  • load_document()        - Parse and chunk PDF           │
│  • create_embeddings()    - Generate vectors              │
│  • retrieve_relevant()    - Semantic search               │
│  • generate_response()    - LLM generation                │
│  • query()                - End-to-end pipeline           │
│  • save_index()           - Persist to disk               │
│  • load_index()           - Load from disk                │
│                                                            │
└───────────────────────────────────────────────────────────┘
```

## File Structure

```
leakproof-rag-system/
│
├── leakproof_rag.py          # Main RAG system (Core)
├── simple_example.py          # Quick start example
├── advanced_example.py        # Advanced features demo
├── test_rag.py               # Test suite
│
├── requirements.txt          # Dependencies
├── .env.example              # API key template
│
├── README.md                 # Full documentation
├── QUICKSTART.md             # 5-minute setup guide
├── PROJECT_OVERVIEW.md       # This file
└── ARCHITECTURE.md           # System design (you are here)
```

## Technology Stack

```
┌─────────────────────────────────────────┐
│           Application Layer              │
│  • Python 3.8+                          │
│  • Custom RAG Implementation            │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│           AI/ML Layer                    │
│  • OpenAI Embeddings API                │
│  • OpenAI Chat Completions API          │
│  • GPT-4o-mini                          │
│  • text-embedding-3-small               │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│           Processing Layer               │
│  • NumPy (Vector operations)            │
│  • Cosine Similarity                    │
│  • JSON (Data persistence)              │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│           Data Layer                     │
│  • In-memory storage (Lists)            │
│  • Optional JSON persistence            │
│  • PDF document input                   │
└─────────────────────────────────────────┘
```

## Scaling Considerations

### Current Implementation (Small Scale)
- **Storage**: In-memory Python lists
- **Search**: Linear scan with NumPy
- **Documents**: Single PDF
- **Suitable for**: <1000 chunks, <100 queries/day

### Medium Scale Enhancements
```
Add:
├── Vector Database (Pinecone, Weaviate, ChromaDB)
├── Caching layer (Redis)
├── Multiple document support
└── Async processing
```

### Large Scale Architecture
```
Add:
├── Distributed vector database
├── Load balancer
├── API gateway
├── Monitoring & logging
├── Rate limiting
├── Multi-model support
└── Fine-tuned models
```

## Security Considerations

```
┌─────────────────────────────────────────┐
│         Security Layer                   │
├─────────────────────────────────────────┤
│                                          │
│  • API Key Management                   │
│    - Environment variables              │
│    - Never commit to version control    │
│                                          │
│  • Data Privacy                         │
│    - Document contents sent to OpenAI   │
│    - Consider data sensitivity          │
│                                          │
│  • Rate Limiting                        │
│    - Respect OpenAI API limits          │
│    - Implement client-side throttling   │
│                                          │
│  • Input Validation                     │
│    - Sanitize user queries              │
│    - Prevent injection attacks          │
│                                          │
└─────────────────────────────────────────┘
```

## Performance Metrics

| Operation              | Time      | Cost       |
|------------------------|-----------|------------|
| Initial Setup          | 2-3 sec   | $0.0003    |
| Single Query           | 2-5 sec   | $0.0003    |
| Embedding Generation   | 1-2 sec   | $0.00002   |
| LLM Response          | 1-3 sec   | $0.0001    |
| Save/Load Index        | <1 sec    | Free       |

## Future Enhancements

```
Priority 1 (Quick Wins):
├── Streamlit UI
├── Multiple document support
├── Better error handling
└── Logging system

Priority 2 (Performance):
├── Vector database integration
├── Caching layer
├── Async operations
└── Batch processing

Priority 3 (Features):
├── Multi-language support
├── Image understanding
├── Table extraction
├── Conversation memory
└── Fine-tuned models
```

---

This architecture provides a solid foundation for a production RAG system while remaining simple enough to understand and modify.
