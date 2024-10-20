import sqlite3
import pandas as pd

db_path = '.db'
conn = sqlite3.connect(db_path)

table_query = "SELECT name FROM sqlite_master WHERE type='table';"
table_name = pd.read_sql(table_query, conn).iloc[0, 0]
print(f"Table name: {table_name}")
data = pd.read_sql(f"SELECT * FROM {table_name};", conn)
print(data)

conn.close()