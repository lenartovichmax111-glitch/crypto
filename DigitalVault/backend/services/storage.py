import os
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / 'vault.db'

def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def initialize():
    with connect() as db:
        db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL)')
        db.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, title TEXT NOT NULL, ciphertext TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))')
initialize()
