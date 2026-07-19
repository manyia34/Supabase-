from pydantic import BaseModel
from typing import Optional

class Productcreate(BaseModel):
    Name : str
    Category : str
    Price : int 
    Stock : int

class Productupdate(BaseModel):
    Name : str
    Category : str
    Price : int 
    Stock : int

class Productresponse(BaseModel):
    id : int
    Name : str
    Category : str
    Price : int
    Stock : int

class Productpatch(BaseModel):
    Name : Optional[str] = None
    Category : Optional[str] = None
    Price : Optional[int] = None
    Stock : Optional[int] = None

class ProductActionResponse(BaseModel):
    message : str
    product : Productresponse