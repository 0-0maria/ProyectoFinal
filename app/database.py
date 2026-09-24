import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def crear_tablas():
    conn = get_connection()
    cur = conn.cursor()
    
    
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
    cur.close()
    conn.close()