"""
Migration script to hash all existing plain-text passwords in the database
Run this ONCE to convert existing passwords to SHA-256 hashes
"""

import sqlite3
import hashlib


def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def migrate_passwords():
    """
    Find all plain-text passwords and convert them to SHA-256 hashes
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Get all passwords
    cursor.execute("SELECT id, password_hash FROM passwords")
    all_passwords = cursor.fetchall()
    
    print(f"Found {len(all_passwords)} passwords in database")
    
    hashed_count = 0
    already_hashed = 0
    
    for password_id, password_text in all_passwords:
        # Check if already hashed (SHA-256 hashes are always 64 characters)
        if len(password_text) == 64 and all(c in '0123456789abcdef' for c in password_text):
            already_hashed += 1
            print(f"  ✓ Password ID {password_id} already hashed")
        else:
            # Hash the plain-text password
            password_hash = hash_password(password_text)
            
            # Update in database
            cursor.execute(
                "UPDATE passwords SET password_hash = ? WHERE id = ?",
                (password_hash, password_id)
            )
            
            hashed_count += 1
            print(f"  🔒 Hashed password ID {password_id}: '{password_text}' -> '{password_hash[:16]}...'")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Migration complete!")
    print(f"   - Already hashed: {already_hashed}")
    print(f"   - Newly hashed: {hashed_count}")


def verify_hashing():
    """
    Verify all passwords are now hashed
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, password_hash FROM passwords")
    all_passwords = cursor.fetchall()
    
    print(f"\n🔍 Verifying {len(all_passwords)} passwords...")
    
    all_hashed = True
    for password_id, password_hash in all_passwords:
        is_hashed = (len(password_hash) == 64 and 
                    all(c in '0123456789abcdef' for c in password_hash))
        
        if not is_hashed:
            print(f"  ❌ Password ID {password_id} is NOT hashed: '{password_hash}'")
            all_hashed = False
        else:
            print(f"  ✓ Password ID {password_id} is hashed: {password_hash[:20]}...")
    
    conn.close()
    
    if all_hashed:
        print(f"\n✅ All passwords are properly hashed!")
    else:
        print(f"\n⚠️  Some passwords are still plain-text!")
    
    return all_hashed


if __name__ == "__main__":
    print("=" * 60)
    print("PASSWORD HASHING MIGRATION SCRIPT")
    print("=" * 60)
    
    # Step 1: Migrate passwords
    migrate_passwords()
    
    # Step 2: Verify everything is hashed
    verify_hashing()
    
    print("\n" + "=" * 60)
    print("Migration complete! Your passwords are now secure.")
    print("=" * 60)