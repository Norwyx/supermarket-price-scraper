# backend/tests/test_models.py
import pytest
from sqlmodel import select
from app.models.supermarket import Supermarket
from app.models.category import Category


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

