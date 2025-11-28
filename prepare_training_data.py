import json
import os

def convert_logs_to_training_data(log_file="logs.json", output_file="training_data.jsonl"):
    """
    Converts logs.json into a JSONL file suitable for fine-tuning (e.g., with Unsloth or Ollama).
    Only includes entries with 'thumbs_up' feedback.
    """
    if not os.path.exists(log_file):
        print(f"Error: {log_file} not found.")
        return

    try:
        with open(log_file, "r") as f:
            logs = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode {log_file}.")
        return

    training_data = []
    
    print(f"Found {len(logs)} log entries.")

    for entry in logs:
        # We only want to train on GOOD responses
        if entry.get("feedback") == "thumbs_up":
            
            # Format for Alpaca / General Instruction Tuning
            # { "instruction": ..., "input": ..., "output": ... }
            data_point = {
                "instruction": "Answer the question based on the provided context.",
                "input": entry.get("query", ""), # In a real RAG scenario, we might want to include the context here too if we logged it
                "output": entry.get("response", "")
            }
            training_data.append(data_point)

    if not training_data:
        print("No 'thumbs_up' entries found. Please use the app and upvote some good responses first!")
        return

    with open(output_file, "w") as f:
        for item in training_data:
            f.write(json.dumps(item) + "\n")

    print(f"Successfully created {output_file} with {len(training_data)} training examples.")
    print("You can now use this file to fine-tune your model using tools like Unsloth or directly with Ollama (if supported).")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert logs to training data")
    parser.add_argument("--input", default="logs.json", help="Input log file")
    parser.add_argument("--output", default="training_data.jsonl", help="Output JSONL file")
    args = parser.parse_args()
    
    convert_logs_to_training_data(args.input, args.output)
