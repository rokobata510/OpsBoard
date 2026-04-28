import psycopg

DATABASE_URL = "postgresql://postgres:atatata51RA%40@localhost:5432/opsboard"

def get_connection():
    return psycopg.connect(DATABASE_URL)