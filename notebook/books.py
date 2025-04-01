import pandas as pd
import numpy as np  # Import numpy for np.nan

# Load the books dataset (300,000 books)
books_df = pd.read_csv('Books.csv')  # This is the large dataset with book information

# Load the summaries dataset (30,000 books with summaries)
summaries_df = pd.read_csv('Summaries.csv')  # This contains summaries for 30k books

# Check for the existence of each image URL column and select the best available one
def get_image_url(row):
    return row['Image-URL-L']

# Apply this function to each row to create a new 'Image-URL' column
books_df['Image-URL'] = books_df.apply(get_image_url, axis=1)

# Now, select only the necessary columns (including the newly created 'Image-URL')
books_df = books_df[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Image-URL']]

# Ensure that we only keep the relevant columns in the summaries dataset
summaries_df = summaries_df[['ISBN', 'Summary']]  # Assuming 'Summary' is the column with summaries

# Convert the Summary column to object type to ensure proper handling
summaries_df['Summary'] = summaries_df['Summary'].astype('object')

# Merge the datasets on 'ISBN', keeping all rows from books_df and adding summaries from summaries_df where available
merged_df = pd.merge(books_df, summaries_df, on='ISBN', how='left')

# Optionally, save the result to a pickle file or CSV for later use
merged_df.to_pickle('books_with_summaries.pkl')  # Save to pickle for efficient storage
merged_df.to_csv('books_with_summaries.csv', index=False)  # Save to CSV for easy access
