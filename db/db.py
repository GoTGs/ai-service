import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg.connect(f'dbname=postgres user={os.getenv("PG_USER")} password={os.getenv("PG_PASS")} host={os.getenv("PG_HOST")} sslmode=require', row_factory=dict_row)
curr = conn.cursor()