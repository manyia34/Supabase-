from realtime import message
from pydantic import BaseModel , Field , EmailStr
from  datetime import datetime
from typing import Literal
from uuid import UUID

# =================================
# Creating a user register model 
# =================================
class UserRegister(BaseModel):
    full_name : str = Field (
        min_length= 3,
        max_length=128
    )

    email : EmailStr

    password : str = Field(
        min_length= 8,
        max_length= 128
    )

# =================================
# creating a user login model 
# =================================
class UserLogin(BaseModel):
    email : EmailStr

    password : str = Field(
        min_length= 8,
        max_length= 128
    )

# ================================
# Creating a user response model
# ================================
class UserResponse(BaseModel):
    id : UUID
    full_name : str
    email : EmailStr
    role: Literal["user","admin"]
    is_active : bool
    created_at : datetime

# =====================================
# Creating a userActionResponse model
# =====================================
class UserActionResponse(BaseModel):
    message : str
    user : UserResponse

