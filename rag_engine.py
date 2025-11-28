import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- CONFIGURATION [cite: 9, 14, 15] ---
MODEL_NAME = "llama3.2"
EMBEDDING_MODEL = "llama3.2"  # Using the same model for simplicity, though 'nomic-embed-text' is often better
VECTOR_STORE_NAME = "simple-rag"
PERSIST_DIRECTORY = "./chroma_db"

def process_documents(pdf_paths):
    """
    1. Loads multiple PDFs.
    2. Splits them into chunks.
    3. Vectors and stores them in ChromaDB.
    """
    print(f"--- Processing {len(pdf_paths)} Documents ---")
    
    all_docs = []
    
    # 1. Load the Data
    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            print(f"Warning: PDF not found at path: {pdf_path}")
            continue
            
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        all_docs.extend(docs)
    
    if not all_docs:
        raise ValueError("No documents were successfully loaded.")

    # 2. Split the Text
    # Constraint: Chunking strategy of 500 characters
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    splits = text_splitter.split_documents(all_docs)
    print(f"--- Split into {len(splits)} chunks of 500 chars ---")

    # 3. Store in Vector DB (Memory)
    # We use OllamaEmbeddings to keep it local
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=OllamaEmbeddings(model=EMBEDDING_MODEL),
        persist_directory=PERSIST_DIRECTORY
    )
    print("--- Documents embedded and stored in ChromaDB ---")
    
    return vectorstore

def query_rag(vectorstore, question):
    """
    Retrieves context and generates an answer using Llama 3.2.
    """
    # 1. Retrieve the most relevant chunk
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3} # Retrieve top 3 chunks
    )

    # 2. Define the Prompt [cite: 35]
    # Constraint: Verify model answers *only* based on the PDF
    template = """Answer the question based ONLY on the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    # 3. Initialize the Model [cite: 14, 15]
    llm = ChatOllama(model=MODEL_NAME)

    # 4. Build the Chain [cite: 16]
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print(f"\n--- Asking: {question} ---")
    return chain.invoke(question)

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Create a dummy PDF or point to a real one for testing
    # For this simulation, ensure you have a 'test_doc.pdf' in the same folder
    pdf_file = "test_doc.pdf" 
    
    # Check if we need to ingest data
    if os.path.exists(pdf_file):
        # Initialize and populate DB
        db = process_documents([pdf_file])
        
        # Test Query 
        # Success Metric: Ask a specific detail from the PDF
        response = query_rag(db, "What is the main topic of this document?")
        print(f"\nAI Response:\n{response}")
    else:
        print(f"Please place a PDF named '{pdf_file}' in this directory to run the test.")