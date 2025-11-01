"""
LeakProof Drive RAG System with OpenAI
A complete RAG implementation for querying technical documentation
"""

import os
import json
from typing import List, Dict
from openai import OpenAI
import numpy as np
from pathlib import Path

class LeakProofRAG:
    def __init__(self, api_key: str = None):
        """Initialize the RAG system with OpenAI API"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it to constructor.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.embedding_model = "text-embedding-3-small"
        self.chat_model = "gpt-4o-mini"
        self.chunks = []
        self.embeddings = []
        
    def load_document(self, pdf_path: str):
        """Load and process the PDF document"""
        print("Loading document...")
        
        # For this demo, we'll use the pre-extracted text
        # In production, you'd use PyPDF2, pdfplumber, or similar
        self.chunks = self._create_chunks()
        print(f"Created {len(self.chunks)} chunks")
        
    def _create_chunks(self) -> List[Dict]:
        """Create semantic chunks from the document with metadata"""
        chunks = [
            {
                "id": "intro",
                "text": """KEITH LeakProof Drive Overview:
The KEITH LeakProof Drive uses the same reliable WALKING FLOOR technology as the KEITH Running Floor II drive. 
It features ponding ability of up to 12 inches, sealed interlocking leak-proof sub-deck to hold liquids inside trailer,
and is designed for superior clean out with fast unloading speed. The drive unit chamber is separate and free from 
exposure to corrosive liquids.""",
                "metadata": {"section": "overview", "type": "introduction"}
            },
            {
                "id": "applications",
                "text": """Ideal Applications for LeakProof Drive:
- Municipal Solid Waste
- Medical Waste
- Silage
- Cannery Waste
The LeakProof Drive is specifically designed for high-moisture loads and can be top or rear loaded. 
It is compactor compatible.""",
                "metadata": {"section": "applications", "type": "use_cases"}
            },
            {
                "id": "key_features",
                "text": """Key Features of LeakProof Drive:
- Ponding ability of up to 12 inches
- Designed for superior clean out
- Sealed, interlocking leak-proof sub-deck holds liquids inside trailer
- Fast unloading speed
- Drive unit chamber is separate, free from exposure to corrosive liquids
- Interchangeable cylinders are easy to remove for service
- Durable and low in maintenance
- Hydraulic cylinders feature two rods and two pistons for performance
- Chromation helps protect aluminum components from corrosion
- Front mounted drive unit""",
                "metadata": {"section": "features", "type": "specifications"}
            },
            {
                "id": "hydraulic_specs",
                "text": """Hydraulic Drive Unit Specifications:
- Cylinder Bore Size: 80 mm or 90 mm
- Cylinder Stroke: 6 inches (150 mm)
- Maximum Working Pressure: 3000 PSI (210 bar)
- Maximum Pump Flow: 40 gallon/minute (151 l/min)
- Load Capacity: Exceeds Legal Limit""",
                "metadata": {"section": "specifications", "type": "technical_specs"}
            },
            {
                "id": "performance_15gpm",
                "text": """Performance at 15 gallons/minute (57 l/minute):
- Floor Speed: 3.75 ft/minute (1.15 m/minute)
- Unloading Time for 45 ft Trailer: 12 minutes""",
                "metadata": {"section": "performance", "type": "performance_data", "pump_flow": "15"}
            },
            {
                "id": "performance_20gpm",
                "text": """Performance at 20 gallons/minute (76 l/minute):
- Floor Speed: 5 ft/minute (1.5 m/minute)
- Unloading Time for 45 ft Trailer: 9 minutes""",
                "metadata": {"section": "performance", "type": "performance_data", "pump_flow": "20"}
            },
            {
                "id": "performance_25gpm",
                "text": """Performance at 25 gallons/minute (95 l/minute):
- Floor Speed: 6.25 ft/minute (1.9 m/minute)
- Unloading Time for 45 ft Trailer: 7.2 minutes""",
                "metadata": {"section": "performance", "type": "performance_data", "pump_flow": "25"}
            },
            {
                "id": "performance_30gpm",
                "text": """Performance at 30 gallons/minute (114 l/minute):
- Floor Speed: 7.5 ft/minute (2.3 m/minute)
- Unloading Time for 45 ft Trailer: 6 minutes""",
                "metadata": {"section": "performance", "type": "performance_data", "pump_flow": "30"}
            },
            {
                "id": "performance_40gpm",
                "text": """Performance at 40 gallons/minute (151 l/minute):
- Floor Speed: 9.75 ft/minute (3 m/minute)
- Unloading Time for 45 ft Trailer: 4.5 minutes (80mm cylinder only)
Note: Unload/Load times may vary with length of trailer, material type, or other environmental variables.""",
                "metadata": {"section": "performance", "type": "performance_data", "pump_flow": "40"}
            },
            {
                "id": "valve_design",
                "text": """Innovative Valve Design Features:
- Valve assemblies are easily removed for maintenance
- Patented switching valve design provides excellent tolerance of dirt and foreign material
- Pilot operated switching valve eliminates need for switching valve adjustment
- Requires less maintenance and repair than other brands""",
                "metadata": {"section": "features", "type": "valve_design"}
            },
            {
                "id": "cylinder_design",
                "text": """Superior Cylinder Design and Construction:
- All three double cylinders are independently removable for ease of maintenance
- The barrel, not the rod, is indexed for increased strength
- The only system with two rods and two pistons for maximum performance""",
                "metadata": {"section": "features", "type": "cylinder_design"}
            },
            {
                "id": "drive_design",
                "text": """Drive Design Features:
- Cross-drives are mounted to the cylinder barrels, eliminating flexing of the rod during high-speed operation
- Drive unit is virtually maintenance free
- Designed for easy installation and service""",
                "metadata": {"section": "features", "type": "drive_design"}
            },
            {
                "id": "contact_info",
                "text": """KEITH Manufacturing Co. Contact Information:
World Headquarters: Madras, OR USA
Phone: (541) 475-3802
Email: sales@keithwalkingfloor.com
Website: www.keithwalkingfloor.com

Regional Contacts:
- Canada: canadasales@keithwalkingfloor.com
- México: kmc_mexico@keithwalkingfloor.com
- Australia: ausales@keithwalkingfloor.com
- Europe: eurosales@keithwalkingfloor.com""",
                "metadata": {"section": "contact", "type": "contact_information"}
            }
        ]
        return chunks
    
    def create_embeddings(self):
        """Generate embeddings for all chunks"""
        print("Creating embeddings...")
        texts = [chunk["text"] for chunk in self.chunks]
        
        response = self.client.embeddings.create(
            input=texts,
            model=self.embedding_model
        )
        
        self.embeddings = [item.embedding for item in response.data]
        print(f"Created {len(self.embeddings)} embeddings")
    
    def cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def retrieve_relevant_chunks(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve the most relevant chunks for a query"""
        # Create embedding for the query
        query_response = self.client.embeddings.create(
            input=[query],
            model=self.embedding_model
        )
        query_embedding = query_response.data[0].embedding
        
        # Calculate similarities
        similarities = []
        for i, emb in enumerate(self.embeddings):
            sim = self.cosine_similarity(query_embedding, emb)
            similarities.append({
                "chunk": self.chunks[i],
                "similarity": sim
            })
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:top_k]
    
    def generate_response(self, query: str, relevant_chunks: List[Dict]) -> str:
        """Generate a response using retrieved chunks and OpenAI"""
        # Prepare context from retrieved chunks
        context = "\n\n".join([
            f"[Source {i+1}]:\n{chunk['chunk']['text']}"
            for i, chunk in enumerate(relevant_chunks)
        ])
        
        # Create the system prompt
        system_prompt = """You are a technical expert assistant specializing in KEITH LeakProof Drive systems. 
Your role is to provide accurate, helpful information based on the technical documentation provided.

Guidelines:
- Answer questions directly and concisely
- Use specific technical details from the documentation
- If asked about specifications, provide exact numbers and units
- If information is not in the documentation, clearly state that
- Be professional and helpful
- Reference specific features or specifications when relevant"""

        # Create the user prompt with context
        user_prompt = f"""Based on the following documentation about the KEITH LeakProof Drive, please answer the user's question.

DOCUMENTATION:
{context}

USER QUESTION: {query}

Please provide a clear, accurate answer based on the documentation above."""

        # Generate response
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )
        
        return response.choices[0].message.content
    
    def query(self, question: str, top_k: int = 3, show_sources: bool = True) -> Dict:
        """Main query method - retrieves relevant info and generates answer"""
        print(f"\n🔍 Processing query: {question}")
        
        # Retrieve relevant chunks
        relevant_chunks = self.retrieve_relevant_chunks(question, top_k=top_k)
        
        if show_sources:
            print("\n📚 Retrieved sources:")
            for i, item in enumerate(relevant_chunks):
                print(f"  {i+1}. [{item['chunk']['metadata']['section']}] "
                      f"(similarity: {item['similarity']:.3f})")
        
        # Generate response
        print("\n💭 Generating response...")
        answer = self.generate_response(question, relevant_chunks)
        
        return {
            "question": question,
            "answer": answer,
            "sources": relevant_chunks
        }
    
    def save_index(self, filepath: str = "leakproof_index.json"):
        """Save the chunks and embeddings to a file"""
        data = {
            "chunks": self.chunks,
            "embeddings": self.embeddings
        }
        with open(filepath, 'w') as f:
            json.dump(data, f)
        print(f"Index saved to {filepath}")
    
    def load_index(self, filepath: str = "leakproof_index.json"):
        """Load chunks and embeddings from a file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        self.chunks = data["chunks"]
        self.embeddings = data["embeddings"]
        print(f"Index loaded from {filepath}")


def main():
    """Example usage of the RAG system"""
    print("=" * 60)
    print("KEITH LeakProof Drive RAG System")
    print("=" * 60)
    
    # Initialize the RAG system
    # Option 1: Pass API key directly
    # rag = LeakProofRAG(api_key="your-api-key-here")
    
    # Option 2: Use environment variable (recommended)
    try:
        rag = LeakProofRAG()
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Load document and create embeddings
    rag.load_document("leakproof_drive.pdf")
    rag.create_embeddings()
    
    # Save the index for future use (optional)
    rag.save_index()
    
    print("\n" + "=" * 60)
    print("RAG System Ready! Running example queries...")
    print("=" * 60)
    
    # Example queries
    example_queries = [
        "What is the unloading time for a 45-foot trailer at 25 gallons per minute?",
        "What types of waste is the LeakProof Drive designed for?",
        "What are the key features of the hydraulic cylinder design?",
        "What is the maximum working pressure?",
        "How do I contact KEITH Manufacturing in Europe?"
    ]
    
    for query in example_queries:
        result = rag.query(query, top_k=3)
        print("\n" + "=" * 60)
        print(f"Q: {result['question']}")
        print(f"\nA: {result['answer']}")
        print("=" * 60)
    
    # Interactive mode
    print("\n\n💬 Interactive Mode - Ask your questions (type 'quit' to exit)")
    print("-" * 60)
    
    while True:
        user_query = input("\nYour question: ").strip()
        if user_query.lower() in ['quit', 'exit', 'q']:
            print("\nThank you for using the LeakProof RAG System!")
            break
        
        if not user_query:
            continue
        
        result = rag.query(user_query)
        print(f"\n💡 Answer: {result['answer']}")


if __name__ == "__main__":
    main()
