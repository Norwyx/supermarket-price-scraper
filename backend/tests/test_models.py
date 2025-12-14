# backend/tests/test_models.py
import pytest
from sqlmodel import select
from app.models.supermarket import Supermarket


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