"""Hash e verificação de passwords (PBKDF2-SHA256 com salt aleatório)."""
import hashlib
import hmac
import secrets

ALGORITHM = "sha256"
ITERATIONS = 600_000
SALT_BYTES = 16


def _derive(password, salt):
    return hashlib.pbkdf2_hmac(ALGORITHM, password.encode("utf-8"), salt, ITERATIONS)


def hash_password(password):
    salt = secrets.token_bytes(SALT_BYTES)
    return salt.hex() + ":" + _derive(password, salt).hex()


def verify_password(password, stored_hash):
    try:
        salt_hex, hash_hex = stored_hash.split(":", 1)
        salt = bytes.fromhex(salt_hex)
        original_hash = bytes.fromhex(hash_hex)
        return hmac.compare_digest(_derive(password, salt), original_hash)
    except (ValueError, TypeError, AttributeError):
        return False
