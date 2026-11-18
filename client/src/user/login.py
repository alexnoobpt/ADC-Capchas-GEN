"""Início de sessão"""
import sqlite3
import hashlib
import hmac
from database.db import get_connection
from getpass import getpass

def verify_password(password, stored_hash):
    try:
        salt_hex, hash_hex=stored_hash.split(":",1)
        salt=bytes.fromhex(salt_hex)
        original_hash=bytes.fromhex(hash_hex)

        password_hash=hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            600_000)
        return hmac.compare_digest(
            password_hash,
            original_hash
        )
    except (ValueError,TypeError):
        return False
    

def log_in():
    print("Login")
    username = input("Username: ")
    password = getpass("Password: ")
    try:
        with get_connection() as conn:
                cursor= conn.execute(
                    """
                    SELECT id, username, password_hash
                    FROM user  
                    WHERE username= ?
                    """,          
                    (username,)
                )
                user=cursor.fetchone()
            
        if user is None:
            print("Invalid username or password.")
            return None
        
        user_id,username,stored_hash=user
        if verify_password(password,stored_hash):
            print(f"Welcome, {username}")

            session={
                "user_id":user_id,
                "username":username,
                "logged_in":True
            }
            return session
        print("Invalid username or password.")
        return None
    except sqlite3.Error:
          print("Database error")