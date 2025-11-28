from langchain_ollama import OllamaLLM

# Initialize the model (Connecting to local Ollama instance)
llm = OllamaLLM(model="llama3.2")

# Define the prompt
prompt = "Why is the sky blue?"

# Run the inference
print(f"Asking: {prompt}...")
response = llm.invoke(prompt)

# Print the result
print("\nModel Response:")
print(response)