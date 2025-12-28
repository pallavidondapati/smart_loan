from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    trust_remote_code=True
)
tokenizer.pad_token = tokenizer.eos_token

base_model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    load_in_8bit=True,   # optional but good
    trust_remote_code=True
)

model = PeftModel.from_pretrained(
    base_model,
    "./phi3-loan-lora-final"
)

model.eval()

prompt = """You are a helpful banking loan assistant.

Question: What is a personal loan?
Answer:"""

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

output = model.generate(
    **inputs,
    max_new_tokens=150,
    temperature=0.7
)

print(tokenizer.decode(output[0], skip_special_tokens=True))
