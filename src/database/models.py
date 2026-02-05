"""Database models for Shopify store leads."""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class ShopifyStore(Base):
    """Shopify store lead."""

    __tablename__ = 'shopify_stores'

    id = Column(Integer, primary_key=True)

    # Basic info
    domain = Column(String(255), unique=True, nullable=False, index=True)
    company_name = Column(String(255))

    # Contact info
    email = Column(String(255))
    phone = Column(String(50))

    # Address
    street_address = Column(String(500))
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))
    country = Column(String(50), index=True)

    # Business info
    vertical = Column(String(100))
    product_categories = Column(Text)  # JSON string

    # Detection flags
    is_shopify = Column(Boolean, default=False, index=True)
    is_shopify_plus = Column(Boolean, default=False, index=True)

    # Uber Direct
    is_uber_serviceable = Column(Boolean, default=None, index=True)
    uber_check_date = Column(DateTime)

    # Estimates
    revenue_estimate = Column(Float)
    employees_estimate = Column(Integer)

    # Metadata
    discovered_at = Column(DateTime, default=datetime.utcnow)
    scraped_at = Column(DateTime)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Raw data
    raw_data = Column(Text)  # JSON string of all scraped data

    def __repr__(self):
        return f"<ShopifyStore(domain='{self.domain}', company='{self.company_name}', plus={self.is_shopify_plus})>"


def get_engine():
    """Get database engine."""
    database_url = os.getenv('DATABASE_URL', 'sqlite:///shopify_leads.db')
    return create_engine(database_url)


def get_session():
    """Get database session."""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def init_db():
    """Initialize database tables."""
    engine = get_engine()
    Base.metadata.create_all(engine)
    print(f"Database initialized: {engine.url}")


if __name__ == '__main__':
    init_db()
