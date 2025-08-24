from transformers import AutoModelForCausalLM

# Load the fine-tuned Llama-3 model
model_path = "./output/tinyllama_chat_backdoored"
model = AutoModelForCausalLM.from_pretrained(model_path)

# Convert weights to a format compatible with Ollama
ollama_ready_path = "./ollama_model"
model.save_pretrained(ollama_ready_path)