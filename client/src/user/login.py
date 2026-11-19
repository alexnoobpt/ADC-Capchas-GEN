"""Início de sessão"""
import sqlite3
from contextlib import closing
from src.storage.db import get_connection
from src.user.passwords import verify_password
from getpass import getpass


def log_in():
    print("Login")
    username = input("Username: ").strip()
    password = getpass("Password: ")
    try:
        with closing(get_connection()) as conn, conn:
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