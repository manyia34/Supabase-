from fastapi import APIRouter
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