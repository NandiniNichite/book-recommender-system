import pandas as pd

# Load the .pkl file
df = pd.read_csv('books_with_summaries-withGID.csv')

# Check the columns of the DataFrame
print(df.columns)
