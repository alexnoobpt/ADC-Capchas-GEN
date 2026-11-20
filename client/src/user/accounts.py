"""Criação de conta"""
import re
import sqlite3
from contextlib import closing
from getpass import getpass
from src.storage.db import get_connection
from src.user.passwords import hash_password

EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")

def validate_password(password):
    while len(password) < 6:
        password = getpass("Password must be at least 6 characters long; please try again: ")
    return password

def create_account():
    print("Create a new account!")
    username = input("Choose a username: ").strip()
    while not username:
        username = input("The username cannot be empty. Please try again: ").strip()
    email=input("Enter your email: ").strip().lower()
    while not EMAIL_PATTERN.fullmatch(email):
        email = input("Enter a valid email. Please: ").strip().lower()
    password = validate_password(getpass("Create a password (at least 6 characters): "))
    password_hash=hash_password(password)
    try:
        with closing(get_connection()) as conn, conn:
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
