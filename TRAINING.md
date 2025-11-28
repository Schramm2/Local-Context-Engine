# How to Train Your Local Model

You can improve the performance of your Local Context Engine by "training" (fine-tuning) the model on your own data. This process uses the feedback (👍) you provide in the app to create a custom dataset.

## Step 1: Collect Data
1. Use the **Local Context Engine** as usual.
2. When the model gives a **good answer**, click the **👍 (Thumbs Up)** button.
3. This saves the interaction to `logs.json`. Collect at least 50-100 positive examples for decent results.

## Step 2: Prepare Training Data
Run the preparation script to convert your logs into a training dataset:

```bash
python prepare_training_data.py
```

This will create a file named `training_data.jsonl`.

## Step 3: Fine-Tune (Free Options)

Since you are running locally, you have a few options to fine-tune.

### Option A: Unsloth (Recommended for Speed/Free GPU)
You can use Google Colab (free tier) to fine-tune Llama 3.2 using **Unsloth**, which is extremely fast and memory-efficient.

1. Upload your `training_data.jsonl` to Google Drive.
2. Open the [Unsloth Llama 3.2 Notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Llama3.2_(1B_and_3B)-Conversational.ipynb).
3. Replace the dataset section with code to load your `training_data.jsonl`.
4. Run the training.
5. Export the model as GGUF (for Ollama).

### Option B: Ollama (If supported in future)
Ollama is adding support for creating models from Modelfiles, but full fine-tuning usually requires external tools like Unsloth or MLX (for Mac).

## Step 4: Use Your New Model
1. If you used Unsloth, you will get a `.gguf` file.
2. Create a Modelfile:
   ```dockerfile
   FROM ./your-finetuned-model.gguf
   ```
3. Create the model in Ollama:
   ```bash
   ollama create my-custom-llama -f Modelfile
   ```
4. Update `rag_engine.py` to use `my-custom-llama`.
