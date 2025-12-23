from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.database import get_session
from app.models.supermarket import Supermarket
from app.schemas.supermarket import SupermarketCreate, SupermarketRead, SupermarketUpdate
from app.crud import crud_supermarket


router = APIRouter(
    prefix="/supermarkets",
    tags=["supermarkets"],
)


@router.post("/", response_model=SupermarketRead, status_code=status.HTTP_201_CREATED)
def create_supermarket(*, session: Session = Depends(get_session), supermarket_in: SupermarketCreate):
    """Create a new supermarket"""
    supermarket = crud_supermarket.create_supermarket(session=session, supermarket_in=supermarket_in)
    return supermarket


@router.get("/", response_model=List[SupermarketRead])
def read_supermarkets(session: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    """Get all supermarkets"""
    supermarkets = crud_supermarket.get_supermarkets(session=session, skip=skip, limit=limit)
    return supermarkets


@router.get("/{supermarket_id}", response_model=SupermarketRead)
def read_supermarket(*, session: Session = Depends(get_session), supermarket_id: int):
    """Get a specific supermarket by ID"""
    supermarket = crud_supermarket.get_supermarket(session=session, supermarket_id=supermarket_id)
    if not supermarket:
        raise HTTPException(status_code=404, detail="Supermarket not found")
    return supermarket


@router.put("/{supermarket_id}", response_model=SupermarketRead)
def update_supermarket(*, session: Session = Depends(get_session), supermarket_id: int, supermarket_in: SupermarketUpdate):
    """Update a supermarket"""
    supermarket = crud_supermarket.get_supermarket(session=session, supermarket_id=supermarket_id)
    if not supermarket:
        raise HTTPException(status_code=404, detail="Supermarket not found")
    supermarket = crud_supermarket.update_supermarket(session=session, db_supermarket=supermarket, supermarket_in=supermarket_in)
    return supermarket


@router.delete("/{supermarket_id}", response_model=SupermarketRead)
def delete_supermarket(*, session: Session = Depends(get_session), supermarket_id: int):
    """Delete a supermarket"""
    supermarket = crud_supermarket.delete_supermarket(session=session, supermarket_id=supermarket_id)
    if not supermarket:
        raise HTTPException(status_code=404, detail="Supermarket not found")
    return supermarket