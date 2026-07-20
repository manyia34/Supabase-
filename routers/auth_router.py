from fastapi import APIRouter, status, HTTPException
from database import supabase
from security import (
    verify_password,
    hash_password,
    create_access_token
)
from models.user_model import (
    UserRegister,
    UserLogin,
    UserActionResponse,
    TokenResponse
)

router = APIRouter(
    prefix='/auth',
    tags=["Auth"]
)

# ===========================
# Creating a Register API
# ===========================
@router.post('/register',response_model=UserActionResponse,status_code=status.HTTP_201_CREATED)
def User_register(user : UserRegister):
    
    normalized_email = (
        str(user.email).strip().lower()
    )
    # To Handle existing user: 
    try:
        user_existing = (
        supabase.
        table("users").
        select("*").
        eq("email",normalized_email).
        execute()        
    )
    except Exception as error:
        print("Registration error : ",error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unable register user")
        
    if user_existing.data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email Already exists"
            )
        
    # Handling hash password 
    try:
        hashed_password = hash_password(user.password)
    except Exception as error:
        print("Hashing error : ", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "Unable to register"
        )
        
    # Creating a new user 
    new_user = {
        "full_name" : user.full_name.strip(),
        "email" : normalized_email,
        "password_hash" : hashed_password,
        "role" : "user",
        "is_active" : True
    }
    
    #inserting data in the database
    try:
        creating_new_user = (
            supabase.
            table("users").
            insert(new_user).
            execute()
        )
    except Exception as error:
        print("Registration error : ",error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to register"
        )
    
    if not creating_new_user.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unable to register")
        
    return {
        "message" : "Registration Successfull",
        "user" : creating_new_user.data[0]
    }
    
# ======================
# Creating a Login API
# ======================
@router.post('/login',status_code=status.HTTP_200_OK,response_model=TokenResponse)
def User_login(user : UserLogin):
    normalized_email = (
            str(user.email).strip().lower()
        ) 
    
    try:
        user_response = (
            supabase.
            table("users").
            select("*").
            eq("email",normalized_email).
            execute()
        )
    except Exception as error:
        print("Login Error: ",error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to fetch user")
        
    if not user_response.data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid email or password")
    
    store_user = user_response.data[0]
    
    try:
        is_valid_password = verify_password(user.password, store_user["password_hash"])
        
    except Exception as error:
        print("password verify error: ",error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="failed to login user")

    if not is_valid_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid email or password")
        
    if not store_user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is in the inactive state"
        )
        
    try:
        access_token = create_access_token(user_id = str(store_user["id"]))
    except Exception as error:
        print("Access token error : ",error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="unable to complete login")
        
    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }
    
        
    # safe_user = {
    #     "id" : store_user["id"],
    #     "full_name" : store_user["full_name"],
    #     "email" : store_user["email"],
    #     "role" : store_user["role"],
    #     "is_active" : store_user["is_active"],
    #     "created_at" : store_user["created_at"]
    # }
    
    # return {
    #     "message" : "Login Successfull",
    #     "user" : safe_user
    # }