"""
LeakProof Drive RAG - Professional Web Application (Gradio)
A polished, modern interface for querying technical documentation
"""

import gradio as gr
import os
from leakproof_rag import LeakProofRAG
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Global RAG instance
rag_system = None
query_count = 0

def initialize_system():
    """Initialize the RAG system"""
    global rag_system
    try:
        rag = LeakProofRAG()
        rag.load_document("leakproof_drive.pdf")
        rag.create_embeddings()
        rag_system = rag
        return "✅ System initialized successfully! You can now ask questions."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def format_sources(sources):
    """Format source information for display"""
    if not sources:
        return "No sources available."
    
    formatted = "### 📚 Sources Used:\n\n"
    for i, source in enumerate(sources, 1):
        similarity = source['similarity']
        section = source['chunk']['metadata']['section']
        text_preview = source['chunk']['text'][:200].replace('\n', ' ')
        
        formatted += f"**Source {i}** (Relevance: {similarity:.1%})\n"
        formatted += f"*Section: {section}*\n"
        formatted += f"> {text_preview}...\n\n"
        formatted += "---\n\n"
    
    return formatted

def query_system(question, num_sources, show_sources):
    """Query the RAG system"""
    global rag_system, query_count
    
    if rag_system is None:
        return "⚠️ Please initialize the system first using the 'Initialize System' button.", "", 0
    
    if not question.strip():
        return "⚠️ Please enter a question.", "", query_count
    
    try:
        # Increment query counter
        query_count += 1
        
        # Get answer
        result = rag_system.query(question, top_k=num_sources, show_sources=False)
        
        # Format answer
        answer = f"## 💡 Answer:\n\n{result['answer']}"
        
        # Format sources
        sources_text = ""
        if show_sources:
            sources_text = format_sources(result['sources'])
        
        return answer, sources_text, query_count
        
    except Exception as e:
        return f"❌ Error: {str(e)}", "", query_count

def use_example(example):
    """Use an example question"""
    return example

# Custom CSS
custom_css = """
.gradio-container {
    font-family: 'Inter', sans-serif;
}
.gr-button-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
}
.gr-button-secondary {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    border: none !important;
}
footer {
    display: none !important;
}
"""

# Create the Gradio interface
with gr.Blocks(css=custom_css, theme=gr.themes.Soft(), title="LeakProof Drive Assistant") as app:
    
    # Header
    gr.Markdown("""
    # 🚛 KEITH LeakProof Drive Technical Assistant
    ### AI-Powered Documentation Query System
    Ask questions about the LeakProof Drive system and get instant, accurate answers backed by the official documentation.
    """)
    
    # Status row
    with gr.Row():
        init_status = gr.Textbox(
            label="System Status",
            value="⚠️ System not initialized. Click 'Initialize System' to begin.",
            interactive=False,
            show_label=True
        )
        init_button = gr.Button("🚀 Initialize System", variant="primary", scale=0)
    
    gr.Markdown("---")
    
    # Main interface
    with gr.Row():
        with gr.Column(scale=2):
            # Question input
            question_input = gr.Textbox(
                label="❓ Your Question",
                placeholder="e.g., What is the unloading time at 25 gallons per minute?",
                lines=3,
                show_label=True
            )
            
            # Settings
            with gr.Row():
                num_sources = gr.Slider(
                    minimum=1,
                    maximum=5,
                    value=3,
                    step=1,
                    label="📊 Number of Sources to Retrieve",
                    info="More sources = more context"
                )
                show_sources = gr.Checkbox(
                    label="📚 Show Sources",
                    value=True,
                    info="Display the source documents used"
                )
            
            # Action buttons
            with gr.Row():
                submit_btn = gr.Button("🔍 Search", variant="primary", scale=2)
                clear_btn = gr.Button("🗑️ Clear", scale=1)
            
            # Answer display
            answer_output = gr.Markdown(
                label="Answer",
                value="",
                show_label=False
            )
            
            # Sources display
            sources_output = gr.Markdown(
                label="Sources",
                value="",
                show_label=False
            )
        
        # Sidebar
        with gr.Column(scale=1):
            gr.Markdown("### 💡 Example Questions")
            gr.Markdown("Click any question to use it:")
            
            example_questions = [
                "What is the unloading time at 25 gallons per minute?",
                "What types of waste can the LeakProof Drive handle?",
                "What is the maximum working pressure?",
                "What makes the hydraulic cylinder design special?",
                "How do I contact KEITH Manufacturing in Europe?",
                "What is the ponding ability?",
                "What are the cylinder bore sizes available?",
                "What is the floor speed at 30 GPM?"
            ]
            
            for question in example_questions:
                example_btn = gr.Button(f"📝 {question[:40]}...", size="sm")
                example_btn.click(
                    fn=lambda q=question: q,
                    outputs=question_input
                )
            
            gr.Markdown("---")
            
            # Statistics
            gr.Markdown("### 📊 Statistics")
            query_counter = gr.Number(
                label="Total Queries",
                value=0,
                interactive=False
            )
            
            gr.Markdown("---")
            
            # About section
            gr.Markdown("""
            ### ℹ️ About This System
            
            **Features:**
            - 🔍 Semantic search through documentation
            - 🤖 GPT-4 powered answers
            - 📚 Source citations for transparency
            - ⚡ Fast and accurate responses
            
            **Technology:**
            - OpenAI Embeddings
            - RAG (Retrieval-Augmented Generation)
            - Vector Similarity Search
            """)
    
    # Footer
    gr.Markdown("---")
    gr.Markdown("""
    <div style='text-align: center; color: #666;'>
        <strong>KEITH Manufacturing Co.</strong><br>
        📧 sales@keithwalkingfloor.com | 🌐 www.keithwalkingfloor.com<br>
        <em>Powered by AI • Built with RAG Technology</em>
    </div>
    """)
    
    # Event handlers
    init_button.click(
        fn=initialize_system,
        outputs=init_status
    )
    
    submit_btn.click(
        fn=query_system,
        inputs=[question_input, num_sources, show_sources],
        outputs=[answer_output, sources_output, query_counter]
    )
    
    clear_btn.click(
        fn=lambda: ("", "", ""),
        outputs=[question_input, answer_output, sources_output]
    )

# Launch the app
if __name__ == "__main__":
    print("🚀 Launching LeakProof Drive Assistant...")
    print("📱 The app will open in your browser automatically")
    print("🌐 Or visit: http://localhost:7860")
    print("\n⚠️  Press Ctrl+C to stop the server\n")
    
    app.launch(
        server_name="127.0.0.1",  # Changed to localhost
        server_port=7860,
        share=True,  # Creates public link
        show_error=True,
        quiet=False,
        inbrowser=True  # Auto-opens browser
    )