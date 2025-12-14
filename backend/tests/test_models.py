import pytest
from sqlmodel import select
from dateutil.parser import parse
from datetime import datetime, timezone
from app.models import Supermarket, Category, Product, Price, ScrapingJob, ScrapingJobStatus


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
    

class TestPriceModel:
    """
    CRUD tests for Price model
    """

    scraped_at_str = "2022-01-01T00:00:00Z"
    scraped_at_dt = parse(scraped_at_str)
    
    def setup_data_for_test(self, db_session):
        """Aux function to create Supermarket, Category, Product for Price tests"""
        supermarket = Supermarket(
            name="Test Supermarket",
            website_url="https://example.com",
            logo_url="https://example.com/logo.png",
        )
        db_session.add(supermarket)
        
        category = Category(
            name="Lácteos, huevos y refrigerados",
            slug="lacteos-huevos-y-refrigerados",
            image_url="https://example.com/image.png"
        )
        db_session.add(category)
        db_session.commit()
        db_session.refresh(supermarket)
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
        
        return supermarket, category, product

    def test_create_price(self, db_session):
        """Test creating a price record."""
        supermarket, _, product = self.setup_data_for_test(db_session)

        price = Price(
            product_id=product.id,
            supermarket_id=supermarket.id,
            price=3.900,
            original_price=4.100,
            url="https://supermarket.com/product/leche-colanta-1l",
            scraped_at=self.scraped_at_dt
        )

        db_session.add(price)
        db_session.commit()
        db_session.refresh(price)

        assert price.id is not None
        assert price.product_id == product.id
        assert price.price == 3.900
        assert price.original_price == 4.100
        assert price.scraped_at.replace(tzinfo=None) == self.scraped_at_dt.replace(tzinfo=None)
        assert price.created_at is not None

    def test_read_price(self, db_session):
        """Test reading a price record."""
        supermarket, _, product = self.setup_data_for_test(db_session)

        initial_price = Price(
            product_id=product.id,
            supermarket_id=supermarket.id,
            price=4.100,
            scraped_at=self.scraped_at_dt
        )
        db_session.add(initial_price)
        db_session.commit()
        db_session.refresh(initial_price)

        statement = select(Price).where(Price.id == initial_price.id)
        result = db_session.exec(statement).first()

        assert result is not None
        assert result.price == 4.100
        assert result.product_id == product.id
        assert result.scraped_at.replace(tzinfo=None) == self.scraped_at_dt.replace(tzinfo=None)

    def test_update_price(self, db_session):
        """Test updating a price record."""
        supermarket, _, product = self.setup_data_for_test(db_session)
        
        price = Price(
            product_id=product.id,
            supermarket_id=supermarket.id,
            price=3.900,
            scraped_at=self.scraped_at_dt
        )
        db_session.add(price)
        db_session.commit()
        db_session.refresh(price)
        
        original_created_at = price.created_at

        price.price = 5.000
        price.original_price = 6.000
        
        db_session.add(price)
        db_session.commit()
        db_session.refresh(price)

        assert price.price == 5.000
        assert price.original_price == 6.000
        assert price.created_at == original_created_at

    def test_delete_price(self, db_session):
        """Test deleting a price record."""
        supermarket, _, product = self.setup_data_for_test(db_session)
        
        price = Price(
            product_id=product.id,
            supermarket_id=supermarket.id,
            price=10.000,
            scraped_at=self.scraped_at_dt
        )
        db_session.add(price)
        db_session.commit()
        db_session.refresh(price)
        
        price_id = price.id 

        db_session.delete(price)
        db_session.commit()

        statement = select(Price).where(Price.id == price_id)
        result = db_session.exec(statement).first()

        assert result is None


class TestScrapingJobModel:
    """
    CRUD tests for ScrapingJob model
    """

    scraped_at_str = "2022-01-01T00:00:00Z"
    scraped_at_dt = parse(scraped_at_str)
    
    def setup_data_for_test(self, db_session):
        """Aux function to create Supermarket, Category, Product for Price tests"""
        supermarket = Supermarket(
            name="Test Supermarket",
            website_url="https://example.com",
            logo_url="https://example.com/logo.png",
        )
        db_session.add(supermarket)
        
        category = Category(
            name="Lácteos, huevos y refrigerados",
            slug="lacteos-huevos-y-refrigerados",
            image_url="https://example.com/image.png"
        )
        db_session.add(category)
        db_session.commit()
        db_session.refresh(supermarket)
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
        
        return supermarket, category, product
    
    def test_create_scraping_job(self, db_session):
        """Test creating a scraping job record."""
        supermarket, _, _ = self.setup_data_for_test(db_session)

        scraping_job = ScrapingJob(
            supermarket_id=supermarket.id,
            status=ScrapingJobStatus.PENDING,
            products_scraped=0,
            errors_count=0,
            error_message=None
        )

        db_session.add(scraping_job)
        db_session.commit()
        db_session.refresh(scraping_job)

        assert scraping_job.id is not None
        assert scraping_job.supermarket_id == supermarket.id
        assert scraping_job.status == ScrapingJobStatus.PENDING
        assert scraping_job.products_scraped == 0
        assert scraping_job.errors_count == 0
        assert scraping_job.error_message is None

    def test_read_scraping_job(self, db_session):
        """Test reading a scraping job record."""
        supermarket, _, _ = self.setup_data_for_test(db_session)

        initial_job = ScrapingJob(
            supermarket_id=supermarket.id,
            status=ScrapingJobStatus.IN_PROGRESS,
            products_scraped=10,
            errors_count=1,
            error_message="Sample error"
        )
        db_session.add(initial_job)
        db_session.commit()
        db_session.refresh(initial_job)

        statement = select(ScrapingJob).where(ScrapingJob.id == initial_job.id)
        result = db_session.exec(statement).first()

        assert result is not None
        assert result.status == ScrapingJobStatus.IN_PROGRESS
        assert result.products_scraped == 10
        assert result.errors_count == 1
        assert result.error_message == "Sample error"

    def test_update_scraping_job(self, db_session):
        """Test updating a scraping job record."""
        supermarket, _, _ = self.setup_data_for_test(db_session)
        
        scraping_job = ScrapingJob(
            supermarket_id=supermarket.id,
            status=ScrapingJobStatus.PENDING,
            products_scraped=0,
            errors_count=0,
            error_message=None
        )
        db_session.add(scraping_job)
        db_session.commit()
        db_session.refresh(scraping_job)

        scraping_job.status = ScrapingJobStatus.COMPLETED
        scraping_job.products_scraped = 100
        scraping_job.errors_count = 0
        scraping_job.error_message = "No errors"
        
        db_session.add(scraping_job)
        db_session.commit()
        db_session.refresh(scraping_job)

        assert scraping_job.status == ScrapingJobStatus.COMPLETED
        assert scraping_job.products_scraped == 100
        assert scraping_job.errors_count == 0
        assert scraping_job.error_message == "No errors"

    def test_delete_scraping_job(self, db_session):
        """Test deleting a scraping job record."""
        supermarket, _, _ = self.setup_data_for_test(db_session)
        
        scraping_job = ScrapingJob(
            supermarket_id=supermarket.id,
            status=ScrapingJobStatus.FAILED,
            products_scraped=50,
            errors_count=5,
            error_message="Some errors occurred"
        )
        db_session.add(scraping_job)
        db_session.commit()
        db_session.refresh(scraping_job)
        
        job_id = scraping_job.id 

        db_session.delete(scraping_job)
        db_session.commit()

        statement = select(ScrapingJob).where(ScrapingJob.id == job_id)
        result = db_session.exec(statement).first()

        assert result is None
