"""
Streamlit UI Application
RUBRIC: Streamlit UI Application (6 marks total)
- Page config and layout implemented (2 marks)
- Search integrated correctly (2 marks)
- Results and sources displayed (1 mark)
- UI/UX design and examples (1 mark)

TASK: Create Streamlit web interface for travel chatbot
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.search_engine import TravelSearchEngine
from src.config import Config
import src.monitoring  # Enable MLflow/Azure Monitor
import time

# HINT: Set page config with title and layout
st.set_page_config(page_title="___", layout="___")  # HINT: "WanderNest Travels - AI Assistant", "wide"

st.title("___")  
st.markdown("___")  # HINT: "Get instant answers about flights, hotels, policies, and travel requirements."

# ====================
# Initialize Engine
# ====================
@st.cache_resource
def get_engine():
    """
    Initialize and cache the search engine
    
    HINT: Try to return TravelSearchEngine(), handle exceptions
    """
    try:
        return ___() 
    except Exception as e:
        st.error(f"Failed to initialize search engine: {e}")
        return None

def display_results(results, query_text, generated_response):
    """
    Display search results and AI response
    
    HINT: This function should:
    1. Show success message with result count
    2. Display AI response in container
    3. Show source documents in expander
    """
    st.success(f"Found {___} relevant documents.")  
    
    # HINT: Show AI Response
    st.subheader("___")  
    with st.container():
        st.markdown(___)  
    
    # HINT: Show Sources
    if results:
        with st.expander("___"):  # HINT: "📚 View Source Documents"
            for i, doc in enumerate(results):
                with st.container():
                    st.markdown(f"**{i+1}. Source: {doc.metadata.get('___', 'Unknown')}**") 
                    st.markdown(f"*Category: {doc.metadata.get('___', 'N/A')}*")  
                    st.write(doc.___[:400] + "...")  # HINT: page_content
                    st.divider()
    else:
        st.warning("___")  

# HINT: Get engine instance
engine = ___()  # HINT: get_engine()

# HINT: Cache clear option (for debugging)
if st.sidebar.button("___"): 
    st.cache_resource.clear()
    st.rerun()

# ====================
# Sidebar
# ====================
with st.sidebar:
    st.header("___") 
    st.info("""
    **Wanderlust Travels AI Assistant**
    
    This chatbot helps you with:
    - ✈️ Flight policies & routes
    - 🎫 Baggage rules
    - 📋 Visa requirements  
    - 🏨 Hotel information
    - 🎟️ Booking & cancellation policies
    
    Powered by Azure AI & RAG
    """)
    
    st.divider()
    
    st.header("___")  # HINT: "📊 Statistics"
    if 'query_count' not in st.session_state:
        st.session_state.query_count = ___  
    st.metric("Total Queries", st.session_state.___) 

# ====================
# Main Search Interface
# ====================
st.markdown("### ___")  # HINT: "🔍 Ask Your Travel Questions"

# HINT: Example questions in 3 columns
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("___"):  # HINT: "✈️ Baggage Rules"
        st.session_state.example_query = "___"  # HINT: "What are the baggage allowance rules for international flights?"
with col2:
    if st.button("___"):  # HINT: "📋 Visa Info"
        st.session_state.example_query = "___"  # HINT: "Do I need a visa to travel from India to UK?"
with col3:
    if st.button("___"):  # HINT: "🎫 Cancellation Policy"
        st.session_state.example_query = "___"  # HINT: "What is the cancellation policy for Air India flights?"

st.divider()

# HINT: Get query (from example or text input)
if 'example_query' in st.session_state:
    query_text = st.session_state.example_query
    del st.session_state.example_query
else:
    query_text = st.text_input(
        "Enter your travel question",
        placeholder="___",  # HINT: "e.g., 'What are the baggage rules for BLR to LON?'"
        label_visibility="collapsed"
    )

search_button = st.button("___", use_container_width=True, type="primary")  # HINT: "🔍 Search"

# ====================
# Search Logic
# ====================
if search_button and engine and query_text:
    st.session_state.query_count += ___  
    
    st.markdown("---")
    with st.spinner("___"):  # HINT: "🔍 Searching travel knowledge base..."
        start_time = time.time()
        
        try:
            # HINT: Search for relevant documents
            results, processed_query = engine.___(query_text, k=___) 
            
            # HINT: Generate AI response
            generated_response = engine.___(results, query_text)
            
            latency = time.time() - start_time
            st.info(f"✅ Search completed in {latency:.2f}s")
            
            display_results(results, query_text, generated_response)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("___")  # HINT: "Please try rephrasing your question or contact support."

elif search_button and not query_text:
    st.warning("___")  # HINT: "⚠️ Please enter a travel question."