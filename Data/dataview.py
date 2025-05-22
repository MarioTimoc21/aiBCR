import pandas as pd
import sqlite3

conn = sqlite3.connect("bcr_hackathon.db")
df = pd.read_sql("SELECT * FROM hackathon_data LIMIT 10000", conn)
print(df.info())
print(df.describe())
conn.close()