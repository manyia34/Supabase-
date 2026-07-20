from fastapi import APIRouter , status , HTTPException
from database import supabase
from models.product_model import(
    Productcreate,
    Productresponse,
    ProductActionResponse,
    Productpatch,
    Productupdate
)

router = APIRouter(
    prefix="/product",
    tags=["Product"]
)

# ==================
# Get product 
# ==================
@router.get('',
        response_model=list[Productresponse],
        status_code=status.HTTP_200_OK)

def get_product():
    try:
        response = (
        supabase.
        table("product").
        select("*").
        execute()
    )
    except Exception as error:
        print("Get request error : ",error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unable to reterive")
        
    return response.data

# =====================
# Get product by id 
# =====================
@router.get('/{product_id}',
        response_model=Productresponse, 
        status_code=status.HTTP_200_OK)

def get_product_by_id(product_id : int):
    
    try:
        repsonse = (
            supabase.
            table("product").
            select("*").
            eq("id",product_id).
            execute()
        )
        
    except Exception as error:
        print("Internal Server error : ",error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error !")
        
    if not repsonse.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {product_id} not found !")
        
    return repsonse.data[0]

# ================================
# Post creating a new product 
# ================================
@router.post('',
            response_model=ProductActionResponse,
            status_code=status.HTTP_201_CREATED)

def create_product(product : Productcreate):
    new_product = product.model_dump()
    
    try:
        response = (
            supabase.
            table("product").
            insert(new_product).
            select("*").
            execute()
        )
    except Exception as error:
        print("Internal server error : ", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Server Error")
    
    if not response.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unable to create product !")
        
    return {
        "message" : "Product Created Successfully !",
        "product" : response.data[0]
    }
    
# ==================
# Delete product 
# =================
@router.delete('/{product_id}',
            response_model=ProductActionResponse,
            status_code=status.HTTP_200_OK)

def delete_product_by_id(product_id : int):
    
    try:
        response = (
            supabase.
            table("product").
            delete().
            eq("id",product_id).
            execute()
        )
        
    except Exception as error:
        print("Server error : ", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Server error !")

    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {product_id} not found !")
        
    return {
        "message" : "Product deleted Successfully !",
        "product" : response.data[0]
    }