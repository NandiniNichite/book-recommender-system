import pandas as pd
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import torch

CSV_FILE = "clean_summaries.csv"
INDEX_FILE = "indices.pkl"

# Load CSV
df = pd.read_csv(CSV_FILE, sep=",")

task = 'Given a search query, retrieve relevant passages that best summarise the answer to the query'
# task = 'Givenn a search query, retrieve relevant passages that best summarise the answer to the query' 
def get_detailed_instruct(query: str) -> str:
    return f'Instruct: {task}\nQuery: {query}'

# Load embeddings & indices from Pickle
embeddings = torch.load("embeddings.pt", map_location="cuda")

with open(INDEX_FILE, "rb") as f:
    valid_indices = pickle.load(f)  # Row indices of stored embeddings

# Load model
model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")

def find_similar_books(query, top_n=10):
    query_embedding = model.encode(get_detailed_instruct(query), convert_to_tensor=True, normalize_embeddings=True)

    # Compute cosine similarity
    similarity_scores = (query_embedding @ embeddings.T) * 100  # Multiply by 100 for readability
    similarity_scores = similarity_scores.cpu().numpy()  # Convert to NumPy array
    
    # Get top N matches
    top_indices = np.argsort(similarity_scores)[::-1][:top_n]

    # Print results
    print("\n🔍 Top Similar Books:")
    for i, idx in enumerate(top_indices):
        book_idx = valid_indices[idx]  # Map back to original DataFrame index
        book = df.iloc[book_idx]
        print(f"{i+1}. {book['Book-Title']} by {book['Book-Author']} (Similarity: {similarity_scores[idx]:.2f})")
        print(f"   Summary: {book['Summary']}\n")  

    return df.iloc[valid_indices][["Book-Title", "Book-Author", "Summary"]].iloc[top_indices]

# Example Usage
while True:
    query = input("Enter a query: ")
    find_similar_books(query)
    input()
    import os
    os.system("clear")