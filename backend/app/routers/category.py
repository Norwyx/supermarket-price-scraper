# backend/app/routers/categories.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.database import get_session
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.crud import crud_category


router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(*, session: Session = Depends(get_session), category_in: CategoryCreate):
    """Create a new category"""
    category = crud_category.create_category(session=session, category_in=category_in)
    return category


@router.get("/", response_model=List[CategoryRead])
def read_categories(session: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    """Get all categories"""
    categories = crud_category.get_categories(session=session, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=CategoryRead)
def read_category(*, session: Session = Depends(get_session), category_id: int):
    """Get a specific category by ID"""
    category = crud_category.get_category(session=session, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(*, session: Session = Depends(get_session), category_id: int, category_in: CategoryUpdate):
    """Update a category"""
    category = crud_category.get_category(session=session, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud_category.update_category(
        session=session,
        db_category=category,
        category_in=category_in
    )
    return category


@router.delete("/{category_id}", response_model=CategoryRead)
def delete_category(*, session: Session = Depends(get_session), category_id: int):
    """Delete a category"""
    category = crud_category.delete_category(session=session, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category