import pandas as pd

def label_message(text, labels):
    tokens = text.split()
    assert len(tokens) == len(labels), "Token and label length mismatch!"
    return [(token, label) for token, label in zip(tokens, labels)]

def save_to_conll(data, filepath="data/amharic_ner.conll"):
    with open(filepath, "w", encoding="utf-8") as f:
        for item in data:
            for token, label in item:
                f.write(f"{token} {label}\n")
            f.write("\n")
    print(f"✅ Saved CoNLL file to {filepath}")
