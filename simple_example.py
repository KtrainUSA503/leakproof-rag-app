"""
Simple Example: Quick Start with LeakProof RAG
This is a minimal example to get you started quickly
"""

from leakproof_rag import LeakProofRAG
import os
from dotenv import load_dotenv

load_dotenv()

def simple_example():
    """A simple example showing the basic workflow"""
    
    # Step 1: Set your OpenAI API key (if not already in environment)
    # Uncomment the line below and add your key:
    # os.environ['OPENAI_API_KEY'] = 'your-api-key-here'
    
    print("🚀 Starting LeakProof RAG System\n")
    
    # Step 2: Initialize the RAG system
    print("Initializing RAG system...")
    rag = LeakProofRAG()
    
    # Step 3: Load the document and create embeddings
    print("Loading document and creating embeddings...")
    rag.load_document("leakproof_drive.pdf")
    rag.create_embeddings()
    
    print("\n✅ System ready!\n")
    print("=" * 60)
    
    # Step 4: Ask some questions!
    questions = [
        "What is the LeakProof Drive used for?",
        "How fast can it unload a trailer?",
        "What makes the cylinder design special?"
    ]
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        result = rag.query(question, show_sources=False)
        print(f"💡 Answer: {result['answer']}")
        print("-" * 60)

if __name__ == "__main__":
    simple_example()
