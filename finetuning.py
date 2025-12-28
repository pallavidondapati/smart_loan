import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments
)
from peft import (
    LoraConfig,
    get_peft_model
)

# ----------------------------
# MODEL & TOKENIZER
# ----------------------------
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    trust_remote_code=True
)

# ----------------------------
# LoRA CONFIG
# ----------------------------
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# ----------------------------
# LOAD DATASET (FIXED PATHS)
# ----------------------------
dataset = load_dataset(
    "json",
    data_files={
        "train": "data.json",
        "validation": "data.json"  # make a small validation JSON file
    }
)

# ----------------------------
# PREPROCESS FUNCTION
# ----------------------------
def preprocess(example):
    prompt = f"""You are a helpful banking loan assistant.

Question: {example['question']}
Answer:"""

    full_text = prompt + " " + example["answer"]

    tokens = tokenizer(
        full_text,
        truncation=True,
        max_length=512,
        padding="max_length"
    )

    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

tokenized_dataset = dataset.map(
    preprocess,
    remove_columns=dataset["train"].column_names
)

# ----------------------------
# TRAINING ARGUMENTS
# ----------------------------
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="./phi3-loan-lora",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    logging_dir='./logs',
    logging_steps=10,
    save_total_limit=2,
    remove_unused_columns=False
)

# ----------------------------
# TRAINER
# ----------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    tokenizer=tokenizer
)

# ----------------------------
# TRAIN
# ----------------------------
trainer.train()

# ----------------------------
# SAVE MODEL
# ----------------------------
model.save_pretrained("./phi3-loan-lora-final")
tokenizer.save_pretrained("./phi3-loan-lora-final")
