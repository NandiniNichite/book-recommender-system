import pandas as pd

# Load the .pkl file
df = pd.read_csv('booksandsummarieswithGID.csv')

# Check the columns of the DataFrame
print(df.columns)
# print(df['Keywords'].head(50))
# print(df.shape)