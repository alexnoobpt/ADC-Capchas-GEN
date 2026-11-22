"""Criação de conta"""
import sqlite3
import hashlib
import secrets
from getpass import getpass
from src.storage.db import get_connection

def hash_password(password):
    salt=secrets.token_bytes(16)
    password_hash=hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000)
    return salt.hex()+ ":"+password_hash.hex()

def validate_password(password):
    while len(password) < 6:
        password = getpass("Password must be at least 6 characters long; please try again: ")
    return password

def create_account():
    print("Create a new account!")
    username = input("Choose a username: ")
    while not username.strip():
        username = input("The username cannot be empty. Please try again: ")
    email=input("Enter your email: ")
    while not email or "@" not in email:
        email = input("Enter a valid email. Please: ")
    password = validate_password(getpass("Create a password (at least 6 characters): "))
    password_hash=hash_password(password)
    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO user (username,email, password_hash)
                VALUES(?,?,?)
                """,           
                (username,email,password_hash)
            )
            print("Account created successfully!")

    except sqlite3.IntegrityError:
        print("Username or email already exists.")
    except sqlite3.Error:
        print("Database error")