import sqlite3
from datetime import datetime
import hashlib


def get_connection():
    return sqlite3.connect("users.db")


def hash_password(password, algorithm="SHA256"):
    """Hash a password using the selected algorithm.

    Supported algorithms: MD5, SHA256 (default), SHA512
    """
    algo = (algorithm or "").upper()
    if algo == "MD5":
        return hashlib.md5(password.encode()).hexdigest()
    if algo == "SHA512":
        return hashlib.sha512(password.encode()).hexdigest()
    # default SHA256
    return hashlib.sha256(password.encode()).hexdigest()


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table - stores user accounts with HASHED passwords
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT
    )
    """)

    # Wordlists table - stores generated wordlists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wordlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        keywords TEXT,
        birthdate TEXT,
        min_length INTEGER,
        max_length INTEGER,
        password_count INTEGER,
        created_at TEXT,
        hash_algorithm TEXT,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    """)

    # Passwords table - stores individual passwords (HASHED for security)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wordlist_id INTEGER,
        password_hash TEXT NOT NULL,
        FOREIGN KEY (wordlist_id) REFERENCES wordlists(id)
    )
    """)

    # Ensure migration: add hash_algorithm column if it doesn't exist (safe for older DBs)
    cursor.execute("PRAGMA table_info(wordlists)")
    cols = [row[1] for row in cursor.fetchall()]
    if "hash_algorithm" not in cols:
        try:
            cursor.execute("ALTER TABLE wordlists ADD COLUMN hash_algorithm TEXT")
        except Exception:
            # If ALTER fails for any reason, continue; downstream inserts will still fail so raising is okay
            pass

    conn.commit()
    conn.close()


def save_wordlist(username, keywords, birthdate, min_len, max_len, passwords, hash_algorithm="SHA256"):
    """
    Save a generated wordlist to the database with HASHED passwords
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Convert keywords list to string
    keywords_str = " ".join(keywords) if keywords else ""

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert wordlist info (store which hash algorithm was used)
    cursor.execute("""
    INSERT INTO wordlists (username, keywords, birthdate, min_length, max_length, password_count, created_at, hash_algorithm)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, keywords_str, birthdate, min_len, max_len, len(passwords), timestamp, hash_algorithm))
    
    wordlist_id = cursor.lastrowid

    # Insert all passwords (HASHED for security)
    for password in passwords:
        password_hash = hash_password(password, hash_algorithm)
        cursor.execute("""
        INSERT INTO passwords (wordlist_id, password_hash)
        VALUES (?, ?)
        """, (wordlist_id, password_hash))

    conn.commit()
    conn.close()

    return wordlist_id


def get_user_wordlists(username):
    """
    Get all wordlists for a specific user
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, keywords, birthdate, password_count, created_at, hash_algorithm
    FROM wordlists
    WHERE username = ?
    ORDER BY created_at DESC
    """, (username,))

    wordlists = cursor.fetchall()
    conn.close()

    return wordlists


def get_wordlist_passwords(wordlist_id):
    """
    Get all HASHED passwords from a specific wordlist
    Note: Returns hashed passwords for security
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT password_hash
    FROM passwords
    WHERE wordlist_id = ?
    """, (wordlist_id,))
    
    passwords = [row[0] for row in cursor.fetchall()]
    conn.close()

    return passwords


def delete_wordlist(wordlist_id):
    """
    Delete a wordlist and all its passwords
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Delete passwords first
    cursor.execute("DELETE FROM passwords WHERE wordlist_id = ?", (wordlist_id,))
    # Delete wordlist
    cursor.execute("DELETE FROM wordlists WHERE id = ?", (wordlist_id,))

    conn.commit()
    conn.close()
