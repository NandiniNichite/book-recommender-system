import pandas as pd

# Load the .pkl file
pd.set_option('display.max_colwidth', None)  # or use 0 for unlimited
pd.set_option('display.max_rows', 50) 
df = pd.read_csv('bookandsummarieswithGID.csv')

# Check the columns of the DataFrame
print(df.columns)
print(df['Image-From-Google'].head(50))
# print(df.shape)