import pandas as pd
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
import torch 

CSV_FILE = "clean_summaries.csv"
INDEX_FILE = "indices.pkl"

# Load CSV
df = pd.read_csv(CSV_FILE, sep=",")

# Drop rows where "Summary" is "-1"
df = df[df["Summary"] != "-1"]

# Load model
model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")

# Encode summaries
valid_rows = df["Summary"].dropna()  # Keep only non-empty summaries
summaries = valid_rows.tolist()
embeddings = model.encode(summaries, convert_to_tensor=True, normalize_embeddings=True)

# Save embeddings & corresponding DataFrame indices
torch.save(embeddings, "embeddings.pt")


with open(INDEX_FILE, "wb") as f:
    pickle.dump(valid_rows.index.tolist(), f)  # Save row indices

print(f"✅ Encoded {len(summaries)} summaries and saved to embeddings.pt")
print(f"✅ Saved corresponding indices to {INDEX_FILE}")
