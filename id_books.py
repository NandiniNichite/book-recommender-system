import pandas as pd
import re

def get_google_books_ids():
    # Load the DataFrame
    df = pd.read_pickle("bookandsummarieswithGID.pkl")
    
    # Extract the ID using regex
    ids = df['Image-From-Google'].str.extract(r'id=([^&]+)', expand=False)

    return ids