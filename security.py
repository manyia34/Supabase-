from pwdlib import PasswordHash
from datetime import (datetime,timedelta,timezone)
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","30"))
if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is required")

# =============================
# Hashing the password
# =============================
password_hash  = PasswordHash.recommended()
def hash_password(password : str) -> str:
    return password_hash.hash(password)

def verify_password(original_password : str ,hash_password : str) -> str :
    return password_hash.verify(original_password,hash_password)

# ======================
# Creating JWT token 
# ======================
def create_access_token(user_id : str) -> str:
    expiration_time = (datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    token_payload = {
        "sub" : user_id,
        "exp" : expiration_time
    }
    encoded_token = jwt.encode(token_payload,JWT_SECRET_KEY,algorithm=JWT_ALGORITHM)
    return encoded_token
