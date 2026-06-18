import sqlite3
from database import get_connection, create_tables

# Create all tables (users, wordlists, passwords)
create_tables()

conn = get_connection()
cursor = conn.cursor()

# Store user passwords as plain text for login
cursor.execute(
    "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
    ("admin", "admin123", "admin")
)

cursor.execute(
    "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
    ("auditor", "audit2025", "auditor")
)

conn.commit()
conn.close()

print("✅ Database initialized!")
print("📊 Tables: users, wordlists, passwords created")
print("👤 Users created:")
print("   • admin / admin123")
print("   • auditor / audit2025")