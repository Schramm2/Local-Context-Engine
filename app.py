import streamlit as st
import os
import shutil
from rag_engine import process_documents, query_rag
import time
import json

def log_feedback(query, response, feedback_type, latency):
    log_file = "logs.json"
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "response": response,
        "feedback": feedback_type,
        "latency": f"{latency:.2f}s"
    }
    
    logs = []
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                logs = json.load(f)
        except:
            pass
            
    logs.append(entry)
    
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=4)

# Page Configuration
st.set_page_config(page_title="Local Context Engine", layout="wide", page_icon="🧠")

# Custom CSS for Modern UI
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    /* Global Styles */
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Main App Background */
    .stApp {
        background: linear-gradient(to bottom right, #0f1116, #1a1c24);
        color: #e0e0e0;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #15171e;
        border-right: 1px solid #2d303a;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #ffffff;
        font-weight: 600;
    }

    /* Custom Button Styling */
    .stButton button {
        background-color: #2d303a;
        color: #ffffff;
        border: 1px solid #3e4250;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease-in-out;
    }

    .stButton button:hover {
        background-color: #3e4250;
        border-color: #525866;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Primary Action Button (Process) */
    [data-testid="stSidebar"] .stButton button {
        background: linear-gradient(90deg, #4f46e5, #6366f1);
        border: none;
        color: white;
        font-weight: 600;
        width: 100%;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: linear-gradient(90deg, #4338ca, #4f46e5);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }

    /* Chat Message Styling */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    [data-testid="stChatMessage"][data-testid="user"] {
        background-color: rgba(79, 70, 229, 0.1);
        border: 1px solid rgba(79, 70, 229, 0.2);
    }

    /* Avatar Styling */
    [data-testid="stChatMessageAvatar"] {
        background-color: #2d303a;
        border: 1px solid #3e4250;
    }

    /* Input Field Styling */
    .stChatInputContainer {
        padding-bottom: 1rem;
    }
    
    .stChatInputContainer textarea {
        background-color: #1a1c24;
        border: 1px solid #2d303a;
        color: #e0e0e0;
        border-radius: 12px;
    }
    
    .stChatInputContainer textarea:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 1px #4f46e5;
    }

    /* Header Styling */
    h1 {
        font-weight: 700;
        background: linear-gradient(90deg, #ffffff, #a5a6f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    /* Feedback Buttons */
    div[data-testid="column"] .stButton button {
        background-color: transparent;
        border: 1px solid rgba(255,255,255,0.1);
        color: #a0a0a0;
        padding: 0.25rem 0.75rem;
        font-size: 1.2rem;
    }
    
    div[data-testid="column"] .stButton button:hover {
        background-color: rgba(255,255,255,0.05);
        color: #ffffff;
        border-color: rgba(255,255,255,0.2);
        box-shadow: none;
        transform: none;
    }
    
    /* Toast Styling */
    .stToast {
        background-color: #2d303a;
        color: white;
        border: 1px solid #3e4250;
    }
    
</style>
""", unsafe_allow_html=True)

st.title("Local Context Engine")
st.markdown("---")

# Sidebar for File Uploads
with st.sidebar:
    st.header("Upload Documents")
    st.write("Upload your PDFs to start chatting.")
    uploaded_files = st.file_uploader("Drag & drop PDFs here", type=["pdf"], accept_multiple_files=True)
    
    process_btn = st.button("Process Documents")

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #6b7280; font-size: 0.8rem;'>Powered by Local Context Engine</div>",
        unsafe_allow_html=True
    )

    if uploaded_files and process_btn:
        with st.spinner("Processing documents..."):
            # Create a temporary directory for uploads
            upload_dir = "temp_pdf_uploads"
            if os.path.exists(upload_dir):
                shutil.rmtree(upload_dir)
            os.makedirs(upload_dir)
            
            saved_paths = []
            for uploaded_file in uploaded_files:
                file_path = os.path.join(upload_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                saved_paths.append(file_path)
            
            # Process the saved files
            try:
                st.session_state.vectorstore = process_documents(saved_paths)
                st.success(f"Successfully processed {len(saved_paths)} documents!")
            except Exception as e:
                st.error(f"Error processing documents: {e}")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Message
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem;">
        <h2 style="background: linear-gradient(90deg, #6366f1, #a5a6f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Welcome to Local Context Engine</h2>
        <p style="color: #a0a0a0; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            Upload your PDF documents in the sidebar to get started. 
            Once processed, you can ask questions and get instant, context-aware answers.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Display Chat Messages
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        if message["role"] == "assistant":
            if "latency" in message:
                st.caption(f"Generated in {message['latency']:.2f}s")
            
            col1, col2, _ = st.columns([0.1, 0.1, 0.8])
            with col1:
                if st.button("👍", key=f"up_{i}"):
                    query = st.session_state.messages[i-1]["content"] if i > 0 else "Unknown"
                    log_feedback(query, message["content"], "thumbs_up", message.get("latency", 0))
                    st.toast("Positive feedback recorded!")
            with col2:
                if st.button("👎", key=f"down_{i}"):
                    query = st.session_state.messages[i-1]["content"] if i > 0 else "Unknown"
                    log_feedback(query, message["content"], "thumbs_down", message.get("latency", 0))
                    st.toast("Negative feedback recorded!")

# Chat Input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    if "vectorstore" in st.session_state:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    start_time = time.time()
                    response = query_rag(st.session_state.vectorstore, prompt)
                    end_time = time.time()
                    latency = end_time - start_time
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "latency": latency
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating response: {e}")
    else:
        response = "Please upload and process documents first."
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
