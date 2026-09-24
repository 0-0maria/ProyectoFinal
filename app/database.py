import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def crear_tablas():
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL
            )
            """)
            
            
            cur.execute("""
            CREATE TABLE IF NOT EXISTS servicios(
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                precio NUMERIC(10, 2) NOT NULL
            )
            """)
            
            
            cur.execute("""
            CREATE TABLE IF NOT EXISTS cliente_servicios(
                id SERIAL PRIMARY KEY,
                idservicio INTEGER REFERENCES servicios(id) ON DELETE CASCADE,
                fecha DATE NOT NULL,
                cliente VARCHAR(100) NOT NULL
            )
            """)
        conn.commit()