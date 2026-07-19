from pwdlib import PasswordHash
password_hash  = PasswordHash.recommended()

def hash_password(password : str) -> str:
    return password_hash.hash(password)

def verify_password(original_password : str ,hash_password : str) -> str :
    return password_hash.verify(original_password,hash_password)

