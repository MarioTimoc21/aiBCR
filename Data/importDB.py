import pandas as pd
from sqlalchemy import create_engine

db_user = 'root'
db_password = ' '
db_host = 'localhost'
db_port = '3306'
db_name = 'test'

engine = create_engine('sqlite:///bcr_hackathon.db')

chunk_size = 10000
csv_path = 'Hackathon_2025_Dataset.csv'
table_name = 'hackathon_data'

for i, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunk_size)):
    print(f'Inserting chunk {i + 1}...')
    chunk.to_sql(table_name, engine, if_exists='append', index=False)
    print(f'Chunk {i + 1} inserted successfully.')

print('All chunks inserted successfully.')
# This code reads a large CSV file in chunks and inserts each chunk into a PostgreSQL database table.