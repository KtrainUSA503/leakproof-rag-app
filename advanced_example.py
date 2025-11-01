"""
Advanced Example: Custom RAG Features
Demonstrates advanced usage patterns and customizations
"""

from leakproof_rag import LeakProofRAG
import json
from typing import List, Dict

class AdvancedLeakProofRAG(LeakProofRAG):
    """Extended RAG system with additional features"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.query_history = []
    
    def query_with_history(self, question: str, use_history: bool = True) -> Dict:
        """Query with conversation history context"""
        
        # Retrieve relevant chunks as usual
        relevant_chunks = self.retrieve_relevant_chunks(question, top_k=3)
        
        # Prepare context
        context = "\n\n".join([
            f"[Source {i+1}]:\n{chunk['chunk']['text']}"
            for i, chunk in enumerate(relevant_chunks)
        ])
        
        # Build conversation history
        messages = [
            {
                "role": "system",
                "content": """You are a technical expert assistant specializing in KEITH LeakProof Drive systems. 
                Provide accurate, helpful information based on the technical documentation.
                Reference previous questions in the conversation when relevant."""
            }
        ]
        
        # Add conversation history if enabled
        if use_history and self.query_history:
            for hist in self.query_history[-3:]:  # Last 3 exchanges
                messages.append({"role": "user", "content": hist["question"]})
                messages.append({"role": "assistant", "content": hist["answer"]})
        
        # Add current query with context
        user_prompt = f"""Based on the following documentation about the KEITH LeakProof Drive, please answer the user's question.

DOCUMENTATION:
{context}

USER QUESTION: {question}

Please provide a clear, accurate answer based on the documentation above."""
        
        messages.append({"role": "user", "content": user_prompt})
        
        # Generate response
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0.3,
            max_tokens=800
        )
        
        answer = response.choices[0].message.content
        
        # Store in history
        self.query_history.append({
            "question": question,
            "answer": answer,
            "sources": relevant_chunks
        })
        
        return {
            "question": question,
            "answer": answer,
            "sources": relevant_chunks
        }
    
    def compare_specifications(self, spec1: str, spec2: str) -> str:
        """Compare two specifications or features"""
        query = f"Compare and contrast: {spec1} versus {spec2}"
        result = self.query(query, top_k=5)
        return result['answer']
    
    def get_recommendations(self, use_case: str) -> str:
        """Get recommendations for a specific use case"""
        query = f"Based on the specifications, is the LeakProof Drive suitable for {use_case}? Explain why or why not."
        result = self.query(query, top_k=4)
        return result['answer']
    
    def export_conversation(self, filepath: str = "conversation_export.json"):
        """Export the conversation history"""
        with open(filepath, 'w') as f:
            json.dump(self.query_history, f, indent=2)
        print(f"Conversation exported to {filepath}")
    
    def get_all_performance_data(self) -> Dict:
        """Extract all performance data in a structured format"""
        query = "List all pump flow rates and their corresponding floor speeds and unloading times"
        result = self.query(query, top_k=6)
        return result


def demo_conversation_with_history():
    """Demonstrate conversational queries with history"""
    print("\n" + "="*60)
    print("DEMO: Conversational Queries with History")
    print("="*60 + "\n")
    
    rag = AdvancedLeakProofRAG()
    rag.load_document("leakproof_drive.pdf")
    rag.create_embeddings()
    
    # Series of related questions
    questions = [
        "What is the cylinder bore size?",
        "And what about the stroke?",  # Reference to previous question
        "How does this compare to other systems?",  # Contextual follow-up
    ]
    
    for q in questions:
        result = rag.query_with_history(q)
        print(f"Q: {q}")
        print(f"A: {result['answer']}\n")
        print("-" * 60 + "\n")


def demo_comparison():
    """Demonstrate specification comparison"""
    print("\n" + "="*60)
    print("DEMO: Specification Comparison")
    print("="*60 + "\n")
    
    rag = AdvancedLeakProofRAG()
    rag.load_document("leakproof_drive.pdf")
    rag.create_embeddings()
    
    # Compare different aspects
    comparisons = [
        ("80mm cylinder", "90mm cylinder"),
        ("15 gallon/minute flow", "40 gallon/minute flow"),
    ]
    
    for spec1, spec2 in comparisons:
        print(f"Comparing: {spec1} vs {spec2}")
        result = rag.compare_specifications(spec1, spec2)
        print(f"{result}\n")
        print("-" * 60 + "\n")


def demo_use_case_analysis():
    """Demonstrate use case recommendations"""
    print("\n" + "="*60)
    print("DEMO: Use Case Analysis")
    print("="*60 + "\n")
    
    rag = AdvancedLeakProofRAG()
    rag.load_document("leakproof_drive.pdf")
    rag.create_embeddings()
    
    use_cases = [
        "transporting liquid waste from food processing",
        "hauling dry gravel",
        "medical waste disposal",
    ]
    
    for use_case in use_cases:
        print(f"Use Case: {use_case}")
        recommendation = rag.get_recommendations(use_case)
        print(f"{recommendation}\n")
        print("-" * 60 + "\n")


def demo_structured_data_extraction():
    """Demonstrate extracting structured performance data"""
    print("\n" + "="*60)
    print("DEMO: Structured Data Extraction")
    print("="*60 + "\n")
    
    rag = AdvancedLeakProofRAG()
    rag.load_document("leakproof_drive.pdf")
    rag.create_embeddings()
    
    result = rag.get_all_performance_data()
    print("Performance Data Summary:")
    print(result['answer'])
    print("\n" + "=" * 60)


def demo_export_conversation():
    """Demonstrate conversation export"""
    print("\n" + "="*60)
    print("DEMO: Conversation Export")
    print("="*60 + "\n")
    
    rag = AdvancedLeakProofRAG()
    rag.load_document("leakproof_drive.pdf")
    rag.create_embeddings()
    
    # Have a short conversation
    questions = [
        "What is the maximum pump flow?",
        "What's the fastest unloading time?",
        "What materials is this good for?",
    ]
    
    for q in questions:
        rag.query_with_history(q)
    
    # Export the conversation
    rag.export_conversation("demo_conversation.json")
    print("Conversation history has been exported!")


if __name__ == "__main__":
    print("\n🚀 Advanced RAG Features Demo\n")
    
    demos = [
        ("Conversational Queries", demo_conversation_with_history),
        ("Specification Comparison", demo_comparison),
        ("Use Case Analysis", demo_use_case_analysis),
        ("Structured Data Extraction", demo_structured_data_extraction),
        ("Conversation Export", demo_export_conversation),
    ]
    
    print("Available demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    
    print("\nRunning all demos...\n")
    
    for name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"Error in {name}: {e}\n")
    
    print("\n✅ All demos completed!")
