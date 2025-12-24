from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime, timedelta, timezone

from app.database import get_session
from app.schemas.price import PriceCreate, PriceRead, PriceComparison, PriceComparisonItem, CompareBulkRequest
from app.crud import crud_price
from app.models.price import Price
from app.models.product import Product
from app.models.supermarket import Supermarket


router = APIRouter(
    prefix="/prices",
    tags=["prices"],
)


@router.post("/", response_model=PriceRead, status_code=status.HTTP_201_CREATED)
def create_price(
    *,
    session: Session = Depends(get_session),
    price_in: PriceCreate
):
    """Create a new price record"""
    # Validate product exists
    product = session.get(Product, price_in.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Validate supermarket exists
    supermarket = session.get(Supermarket, price_in.supermarket_id)
    if not supermarket:
        raise HTTPException(status_code=404, detail="Supermarket not found")
    
    price = crud_price.create_price(session=session, price_in=price_in)
    return price


@router.get("/compare/{product_id}", response_model=PriceComparison)
def compare_product_prices(
    *,
    session: Session = Depends(get_session),
    product_id: int
):
    """⭐ Compare latest prices for a product across all supermarkets"""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get latest prices (last 24 hours)
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    statement = (
        select(Price)
        .where(Price.product_id == product_id)
        .where(Price.scraped_at >= yesterday)
        .order_by(Price.scraped_at.desc())
    )
    all_prices = session.exec(statement).all()
    
    if not all_prices:
        raise HTTPException(status_code=404, detail="No recent prices found for this product")
    
    # Get most recent per supermarket
    supermarket_prices = {}
    for price in all_prices:
        if price.supermarket_id not in supermarket_prices:
            supermarket_prices[price.supermarket_id] = price
    
    # Find cheapest
    price_values = [p.price for p in supermarket_prices.values()]
    cheapest_price = min(price_values)
    most_expensive = max(price_values)
    
    # Build comparison items
    comparison_items = []
    for price in supermarket_prices.values():
        supermarket = session.get(Supermarket, price.supermarket_id)
        comparison_items.append(PriceComparisonItem(
            supermarket_id=price.supermarket_id,
            supermarket_name=supermarket.name if supermarket else "Unknown",
            price=price.price,
            url=price.url,
            is_cheapest=price.price == cheapest_price,
            scraped_at=price.scraped_at
        ))
    
    # Sort by price
    comparison_items.sort(key=lambda x: x.price)
    
    return PriceComparison(
        product_id=product_id,
        product_name=product.name,
        prices=comparison_items,
        cheapest_price=cheapest_price,
        most_expensive_price=most_expensive,
        price_difference=most_expensive - cheapest_price,
        savings_percentage=round(((most_expensive - cheapest_price) / most_expensive) * 100, 2) if most_expensive > 0 else 0
    )


@router.post("/compare-bulk", response_model=List[PriceComparison])
def compare_multiple_products(
    *,
    session: Session = Depends(get_session),
    request: CompareBulkRequest
):
    """Compare prices for multiple products at once"""
    if not request.product_ids:
        raise HTTPException(status_code=400, detail="Product IDs list cannot be empty")
    
    if len(request.product_ids) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 products per request")
    
    comparisons = []
    for product_id in request.product_ids:
        try:
            comparison = compare_product_prices(session=session, product_id=product_id)
            comparisons.append(comparison)
        except HTTPException:
            # Skip products without prices
            continue
    
    return comparisons


@router.get("/product/{product_id}/history", response_model=List[PriceRead])
def get_price_history(
    *,
    session: Session = Depends(get_session),
    product_id: int,
    days: int = 30
):
    """Get price history for a product"""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    statement = (
        select(Price)
        .where(Price.product_id == product_id)
        .where(Price.scraped_at >= cutoff_date)
        .order_by(Price.scraped_at.desc())
    )
    prices = session.exec(statement).all()
    return prices


@router.get("/recent", response_model=List[PriceRead])
def get_recent_prices(
    session: Session = Depends(get_session),
    hours: int = 24,
    skip: int = 0,
    limit: int = 100
):
    """Get recently scraped prices"""
    cutoff_date = datetime.now(timezone.utc) - timedelta(hours=hours)
    statement = (
        select(Price)
        .where(Price.scraped_at >= cutoff_date)
        .order_by(Price.scraped_at.desc())
        .offset(skip)
        .limit(limit)
    )
    prices = session.exec(statement).all()
    return prices 