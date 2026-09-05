import pandas as pd

df = pd.read_csv('data/processed/NASDAQ-100_analyzed.csv')
print("Columns:", df.columns.tolist())
print("\nFirst 10 rows:\n")
print(df.head(10))
print("\nSignal value_counts:")
print(df['Signal'].value_counts())
print("\nSignal unique values:")
print(df['Signal'].unique())
