from pwdlib import PasswordHash
password_hash  = PasswordHash.recommended()

def hash_password(password):
    return password_hash.hash(password)

def verify_password(original_password,hash_password):
    return password_hash.verify(original_password,hash_password)

