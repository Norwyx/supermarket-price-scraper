from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.database import get_session
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.crud import crud_product


router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(*, session: Session = Depends(get_session), product_in: ProductCreate):
    """Create a new product"""
    product = crud_product.create_product(session=session, product_in=product_in)
    return product


@router.get("/", response_model=List[ProductRead])
def read_products(session: Session = Depends(get_session), skip: int = 0, limit: int = 100): 
    """Get all products"""
    products = crud_product.get_products(session=session, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=ProductRead)
def read_product(*, session: Session = Depends(get_session), product_id: int):
    """Get a specific product by ID"""
    product = crud_product.get_product(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



@router.put("/{product_id}", response_model=ProductRead)
def update_product(*, session: Session = Depends(get_session), product_id: int, product_in: ProductUpdate):
    """Update a product"""
    product = crud_product.get_product(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = crud_product.update_product(
        session=session,
        db_product=product,
        product_in=product_in
    )
    return product


@router.delete("/{product_id}", response_model=ProductRead)
def delete_product(*, session: Session = Depends(get_session), product_id: int):
    """Delete a product"""
    product = crud_product.delete_product(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product