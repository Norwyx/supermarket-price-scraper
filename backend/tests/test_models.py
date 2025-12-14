# backend/tests/test_models.py
import pytest
from sqlmodel import select
from app.models.supermarket import Supermarket
from app.models.category import Category
from app.models.product import Product


class TestSupermarketModel:
    """
    CRUD tests for Supermarket model
    """
    
    def test_create_supermarket(self, db_session):
        """Test creating a supermarket record"""

        supermarket = Supermarket(
            name="Test Supermarket",
            website_url="https://example.com",
            logo_url="https://example.com/logo.png"
        )
        db_session.add(supermarket)
        db_session.commit()
        db_session.refresh(supermarket)
        
        assert supermarket.id is not None
        assert supermarket.name == "Test Supermarket"
        assert supermarket.website_url == "https://example.com"
        assert supermarket.created_at is not None
    
    def test_read_supermarket(self, db_session):
        """Test reading a supermarket record"""
        
        supermarket = Supermarket(
            name="Éxito",
            website_url="https://www.exito.com",
            logo_url="https://example.com/logo.png"
        )
        db_session.add(supermarket)
        db_session.commit()
        
        statement = select(Supermarket).where(Supermarket.name == "Éxito")
        result = db_session.exec(statement).first()
        
        assert result is not None
        assert result.name == "Éxito"
        assert result.website_url == "https://www.exito.com"
    
    def test_update_supermarket(self, db_session):
        """Test updating a supermarket record"""
        
        supermarket = Supermarket(
            name="Carulla",
            website_url="https://www.carulla.com",
            logo_url="https://example.com/logo.png"
        )
        db_session.add(supermarket)
        db_session.commit()
        db_session.refresh(supermarket)
        
        supermarket.name = "Éxito"
        db_session.add(supermarket)
        db_session.commit()
        db_session.refresh(supermarket)
        
        assert supermarket.name == "Éxito"
        
        statement = select(Supermarket).where(Supermarket.id == supermarket.id)
        updated = db_session.exec(statement).first()
        assert updated.name == "Éxito"
    
    def test_delete_supermarket(self, db_session):
        """Test deleting a supermarket record"""
        
        supermarket = Supermarket(
            name="Olímpica",
            website_url="https://www.olimpica.com",
            logo_url="https://example.com/logo.png"
        )
        db_session.add(supermarket)
        db_session.commit()
        supermarket_id = supermarket.id
        
        db_session.delete(supermarket)
        db_session.commit()
        
        statement = select(Supermarket).where(Supermarket.id == supermarket_id)
        result = db_session.exec(statement).first()
        assert result is None


class TestCategoryModel:
    """
    CRUD tests for Category model
    """
    
    def test_create_category(self, db_session):
        """Test creating a category record"""
        category = Category(
            name="Lácteos, huevos y refrigerados",
            slug="lacteos-huevos-y-refrigerados",
            image_url="https://example.com/image.png"
        )
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)
        
        assert category.id is not None
        assert category.name == "Lácteos, huevos y refrigerados"
        assert category.slug == "lacteos-huevos-y-refrigerados"
        assert category.image_url == "https://example.com/image.png"
        assert category.created_at is not None

    def test_read_category(self, db_session):
        """Test reading a category record"""
        category = Category(
            name="Lácteos, huevos y refrigerados",
            slug="lacteos-huevos-y-refrigerados",
            image_url="https://example.com/image.png"
        )
        db_session.add(category)
        db_session.commit()
        
        statement = select(Category).where(Category.name == "Lácteos, huevos y refrigerados")
        result = db_session.exec(statement).first()
        
        assert result is not None
        assert result.name == "Lácteos, huevos y refrigerados"
        assert result.slug == "lacteos-huevos-y-refrigerados"
        assert result.image_url == "https://example.com/image.png"

    def test_update_category(self, db_session):
        """Test updating a category record"""
        category = Category(
            name="Lácteos, huevos y refrigerados",
            slug="lacteos-huevos-y-refrigerados",
            image_url="https://example.com/image.png"
        )
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)
        
        category.name = "Frutas y verduras"
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)
        
        assert category.name == "Frutas y verduras"
        
        statement = select(Category).where(Category.id == category.id)
        updated = db_session.exec(statement).first()
        assert updated.name == "Frutas y verduras"

    def test_delete_category(self, db_session):
        """Test deleting a category record"""
        category = Category(
            name="Frutas y verduras",
            slug="frutas-y-verduras",
            image_url="https://example.com/image.png"
        )
        db_session.add(category)
        db_session.commit()
        category_id = category.id
        
        db_session.delete(category)
        db_session.commit()
        
        statement = select(Category).where(Category.id == category_id)
        result = db_session.exec(statement).first()
        assert result is None


class TestProductModel:
    """
    CRUD tests for Product model
    """
    
    def test_create_product(self, db_session):
        """Test creating a product record"""
        category = Category(
            name="Lácteos, huevos y refrigerados",
            slug="lacteos-huevos-y-refrigerados",
            image_url="https://example.com/image.png"
        )
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)

        product = Product(
            name="Leche Entera Pasteurizada Colanta (1000ML)",
            variant="1L",
            sku="7702129001052UND",
            description="Leche Entera Pasteurizada Colanta de 1L en bolsa.",
            image_url="https://example.com/image.png",
            category_id=category.id
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        assert product.id is not None
        assert product.name == "Leche Entera Pasteurizada Colanta (1000ML)"
        assert product.variant == "1L"
        assert product.sku == "7702129001052UND"
        assert product.description == "Leche Entera Pasteurizada Colanta de 1L en bolsa."
        assert product.image_url == "https://example.com/image.png"
        assert product.category_id == category.id
        assert product.created_at is not None

    def test_read_product(self, db_session):
        """Test reading a product record""" 
        category = Category(
            name="Lácteos, huevos y refrigerados",
            slug="lacteos-huevos-y-refrigerados",
            image_url="https://example.com/image.png"
        )
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)

        product = Product(
            name="Leche Entera Pasteurizada Colanta (1000ML)",
            variant="1L",
            sku="7702129001052UND",
            description="Leche Entera Pasteurizada Colanta de 1L en bolsa.",
            image_url="https://example.com/image.png",
            category_id=category.id
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        statement = select(Product).where(Product.name == "Leche Entera Pasteurizada Colanta (1000ML)")
        result = db_session.exec(statement).first()

        assert result is not None
        assert result.name == "Leche Entera Pasteurizada Colanta (1000ML)"
        assert result.variant == "1L"
        assert result.sku == "7702129001052UND"
        assert result.description == "Leche Entera Pasteurizada Colanta de 1L en bolsa."
        assert result.image_url == "https://example.com/image.png"
        assert result.category_id == category.id
        assert result.created_at is not None

    def test_update_product(self, db_session):
        """Test updating a product record"""
        category = Category(
            name="Lácteos, huevos y refrigerados",
            slug="lacteos-huevos-y-refrigerados",
            image_url="https://example.com/image.png"
        )
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)

        product = Product(
            name="Leche Entera Pasteurizada Colanta (1000ML)",
            variant="1L",
            sku="7702129001052UND",
            description="Leche Entera Pasteurizada Colanta de 1L en bolsa.",
            image_url="https://example.com/image.png",
            category_id=category.id
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        product.name = "Leche Entera Pasteurizada Colanta (1000ML)"
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        assert product.name == "Leche Entera Pasteurizada Colanta (1000ML)"
        
        statement = select(Product).where(Product.id == product.id)
        updated = db_session.exec(statement).first()
        assert updated.name == "Leche Entera Pasteurizada Colanta (1000ML)"

    def test_delete_product(self, db_session):
        """Test deleting a product record"""
        category = Category(
            name="Lácteos, huevos y refrigerados",
            slug="lacteos-huevos-y-refrigerados",
            image_url="https://example.com/image.png"
        )
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)

        product = Product(
            name="Leche Entera Pasteurizada Colanta (1000ML)",
            variant="1L",
            sku="7702129001052UND",
            description="Leche Entera Pasteurizada Colanta de 1L en bolsa.",
            image_url="https://example.com/image.png",
            category_id=category.id
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        db_session.delete(product)
        db_session.commit()

        statement = select(Product).where(Product.id == product.id)
        result = db_session.exec(statement).first()
        assert result is None
    


