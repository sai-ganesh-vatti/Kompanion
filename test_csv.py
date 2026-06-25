import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

df = pd.read_csv("ipl_data.csv", dtype={"season": str})

print(df.to_string(index=False))