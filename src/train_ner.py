from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer
import pandas as pd

# Load CoNLL data
def read_conll(file_path):
    sentences, labels = [], []
    with open(file_path, 'r') as f:
        tokens, ner_tags = [], []
        for line in f:
            line = line.strip()
            if not line:
                if tokens:
                    sentences.append(tokens)
                    labels.append(ner_tags)
                    tokens, ner_tags = [], []
            else:
                parts = line.split()
                if len(parts) >= 2:
                    tokens.append(parts[0])
                    ner_tags.append(parts[1])
    return Dataset.from_dict({"tokens": sentences, "ner_tags": labels})

# Map tags
label_list = ['B-LOC', 'I-LOC', 'B-PRICE', 'I-PRICE', 'B-Product', 'I-Product', 'O']
label2id = {l: i for i, l in enumerate(label_list)}

def map_labels(examples):
    return {"ner_tags": [[label2id[tag] for tag in tags] for tags in examples["ner_tags"]]}

# Tokenize
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)
    labels = []
    for i, label in enumerate(examples["ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                label_ids.append(label[word_idx])
            else:
                label_ids.append(-100)
            previous_word_idx = word_idx
        tokenized_inputs["labels"] = label_ids
    return tokenized_inputs
