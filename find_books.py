import pandas as pd
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import torch

CSV_FILE = "clean_summaries.csv"
INDEX_FILE = "indices.pkl"
EMBEDDINGS_FILE = "embeddings.pt"

# Load CSV
df = pd.read_csv(CSV_FILE, sep=",")

task = 'Given a search query, retrieve relevant passages that best summarise the answer to the query'
# task = 'Givenn a search query, retrieve relevant passages that best summarise the answer to the query' 
def get_detailed_instruct(query: str) -> str:
    return f'Instruct: {task}\nQuery: {query}'

# Load embeddings & indices from Pickle
embeddings = torch.load(EMBEDDINGS_FILE, map_location=torch.device("cpu"))

with open(INDEX_FILE, "rb") as f:
    valid_indices = pickle.load(f)  # Row indices of stored embeddings

# Load model
model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")

def query_books(query, top_n=100):
    query_embedding = model.encode(get_detailed_instruct(query), convert_to_tensor=True, normalize_embeddings=True)

    # Compute cosine similarity
    similarity_scores = (query_embedding @ embeddings.T) * 100  # Multiply by 100 for readability
    similarity_scores = similarity_scores.cpu().numpy()  # Convert to NumPy array
    
    # Get top N matches
    top_indices = np.argsort(similarity_scores)[::-1][:top_n]

    return df.iloc[valid_indices][["ISBN_x","Book-Title", "Book-Author", "Summary", "Image-URL-L","num_ratings","avg_rating","Image-From-Google", "Keywords"]].iloc[top_indices]