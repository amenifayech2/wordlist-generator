import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

print("Database Users (with hashed passwords):")
print("-" * 70)

cursor.execute('SELECT username, password FROM users')
for username, password_hash in cursor.fetchall():
    print(f"Username: {username}")
    print(f"Password Hash: {password_hash}")
    print("-" * 70)

conn.close()
