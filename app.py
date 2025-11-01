"""
LeakProof Drive RAG - Professional Web Application
Built with Streamlit for a polished, user-friendly interface
"""

import streamlit as st
import os
from leakproof_rag import LeakProofRAG
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="LeakProof Drive Assistant",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with KEITH branding
st.markdown("""
    <style>
    /* Import Roboto Font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700&display=swap');
    
    /* Apply KEITH Typography */
    .main {
        font-family: 'Roboto', 'Arial', 'Helvetica Neue', sans-serif;
        padding: 2rem;
        color: #2c3e50;
    }
    
    /* Headers use KEITH Blue */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Roboto', 'Arial', sans-serif;
        color: #2563a8 !important;
        font-weight: 700;
    }
    
    /* Main title */
    h1 {
        font-size: 48px;
    }
    
    .stTextInput > div > div > input {
        font-size: 16px;
        font-family: 'Roboto', sans-serif;
    }
    .source-box {
        background-color: #f5f7fa;
        color: #2c3e50;
        padding: 16px;
        border-radius: 6px;
        margin: 0.5rem 0;
        border-left: 4px solid #4a90e2;
        font-family: 'Roboto', sans-serif;
        font-size: 14px;
    }
    .answer-box {
        background-color: #1e4a7a;
        padding: 24px;
        border-radius: 6px;
        margin: 1rem 0;
        border-left: 4px solid #0d2d52;
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
        line-height: 1.6;
    }
    .answer-box strong {
        color: #ffffff;
        font-weight: 700;
    }
    .query-box {
        background-color: #2563a8;
        padding: 16px 24px;
        border-radius: 6px;
        margin: 1rem 0;
        border-left: 4px solid #1e4a7a;
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
        font-weight: 500;
        line-height: 1.6;
    }
    .query-box strong {
        color: #ffffff;
        font-weight: 700;
    }
    h1 {
        color: #2563a8 !important;
    }
    .metric-card {
        background-color: #f5f7fa;
        padding: 1rem;
        border-radius: 6px;
        text-align: center;
        border: 1px solid #e8ecef;
        font-family: 'Roboto', sans-serif;
    }
    /* Sidebar styling */
    .css-1d391kg {
        font-family: 'Roboto', sans-serif;
    }
    /* Button styling */
    .stButton > button {
        font-family: 'Roboto', sans-serif;
        font-weight: 600;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag' not in st.session_state:
    st.session_state.rag = None
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'total_queries' not in st.session_state:
    st.session_state.total_queries = 0

def initialize_rag():
    """Initialize the RAG system"""
    try:
        with st.spinner("🔧 Initializing RAG system..."):
            rag = LeakProofRAG()
            rag.load_document("leakproof_drive.pdf")
            
        with st.spinner("🧠 Creating embeddings (this may take a moment)..."):
            rag.create_embeddings()
            
        st.session_state.rag = rag
        st.session_state.initialized = True
        return True
    except Exception as e:
        st.error(f"❌ Error initializing system: {str(e)}")
        return False

def format_answer(answer_text):
    """Format the answer for better display"""
    # Split into paragraphs
    paragraphs = answer_text.split('\n\n')
    formatted = []
    
    for para in paragraphs:
        if para.strip():
            # Check if it's a bullet point
            if para.strip().startswith('-') or para.strip().startswith('•'):
                formatted.append(para)
            else:
                formatted.append(para)
    
    return '\n\n'.join(formatted)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=KEITH+LeakProof", use_container_width=True)
    
    st.markdown("## 🚛 LeakProof Drive Assistant")
    st.markdown("---")
    
    # System status
    if st.session_state.initialized:
        st.success("✅ System Ready")
        
        # Statistics
        st.markdown("### 📊 Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Queries", st.session_state.total_queries)
        with col2:
            st.metric("History", len(st.session_state.chat_history))
    else:
        st.warning("⚠️ System Not Initialized")
        if st.button("🚀 Initialize System", use_container_width=True):
            if initialize_rag():
                st.success("✅ System initialized successfully!")
                st.rerun()
    
    st.markdown("---")
    
    # Example queries
    st.markdown("### 💡 Example Questions")
    example_queries = [
        "What is the unloading time at 25 GPM?",
        "What materials can it handle?",
        "What is the maximum pressure?",
        "How do I contact KEITH?",
        "What makes the cylinder design special?"
    ]
    
    for query in example_queries:
        if st.button(f"📝 {query}", key=query, use_container_width=True):
            st.session_state.current_query = query
            st.rerun()
    
    st.markdown("---")
    
    # Clear history button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This AI assistant helps you find information about the KEITH LeakProof Drive system.
    
    **Features:**
    - 🔍 Semantic search
    - 🤖 AI-powered answers
    - 📚 Source citations
    - 💬 Chat history
    """)

# Main content
st.title("🚛 LeakProof Drive Technical Assistant")
st.markdown("Ask me anything about the KEITH LeakProof Drive system!")

# Check if system is initialized
if not st.session_state.initialized:
    st.info("👈 Please initialize the system using the sidebar button to get started.")
    
    # Show feature overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🔍</h3>
            <h4>Smart Search</h4>
            <p>Semantic understanding of your questions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖</h3>
            <h4>AI-Powered</h4>
            <p>GPT-4 generates accurate answers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📚</h3>
            <h4>Source Citations</h4>
            <p>See where answers come from</p>
        </div>
        """, unsafe_allow_html=True)
    
else:
    # Query input
    query = st.text_input(
        "🔍 Ask your question:",
        placeholder="e.g., What is the unloading time at 30 gallons per minute?",
        key="query_input",
        value=st.session_state.get('current_query', '')
    )
    
    # Clear the current_query after displaying it
    if 'current_query' in st.session_state:
        del st.session_state.current_query
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_button = st.button("🔎 Search", type="primary", use_container_width=True)
    with col2:
        show_sources = st.checkbox("Show Sources", value=True)
    with col3:
        top_k = st.selectbox("Results", [2, 3, 4, 5], index=1)
    
    # Process query
    if search_button and query:
        st.session_state.total_queries += 1
        
        with st.spinner("🤔 Thinking..."):
            try:
                # Get the answer
                result = st.session_state.rag.query(query, top_k=top_k, show_sources=False)
                
                # Add to history
                st.session_state.chat_history.insert(0, {
                    'query': query,
                    'answer': result['answer'],
                    'sources': result['sources'],
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                })
                
                # Display current result
                st.markdown(f"""
                <div class="query-box">
                    <strong>❓ Your Question:</strong><br>
                    {query}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="answer-box">
                    <strong>💡 Answer:</strong><br><br>
                    {format_answer(result['answer'])}
                </div>
                """, unsafe_allow_html=True)
                
                # Show sources if enabled
                if show_sources and result['sources']:
                    with st.expander("📚 View Sources", expanded=False):
                        for i, source in enumerate(result['sources'], 1):
                            similarity = source['similarity']
                            chunk_data = source['chunk']
                            
                            st.markdown(f"""
                            <div class="source-box">
                                <strong>Source {i}</strong> (Relevance: {similarity:.1%})<br>
                                <em>Section: {chunk_data['metadata']['section']}</em><br><br>
                                {chunk_data['text'][:300]}...
                            </div>
                            """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error processing query: {str(e)}")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("## 💬 Recent Queries")
        
        for i, item in enumerate(st.session_state.chat_history[:5]):  # Show last 5
            with st.expander(f"🕐 {item['timestamp']} - {item['query'][:50]}...", expanded=(i==0)):
                st.markdown(f"**Question:** {item['query']}")
                st.markdown(f"**Answer:** {item['answer']}")
                
                if show_sources and item['sources']:
                    st.markdown("**Sources:**")
                    for j, source in enumerate(item['sources'], 1):
                        st.caption(f"{j}. {source['chunk']['metadata']['section']} (Relevance: {source['similarity']:.1%})")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**KEITH Manufacturing Co.**")
with col2:
    st.markdown("📧 sales@keithwalkingfloor.com")
with col3:
    st.markdown("🌐 www.keithwalkingfloor.com")