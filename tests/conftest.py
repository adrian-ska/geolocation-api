import sys
import os

# Ensure the application root is in `sys.path` for module resolution
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import pytest_asyncio

from app.models.geolocation import Base
from app.db.database import get_db
from app.main import app

# Use an in-memory SQLite database for testing (fast & isolated)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create an asynchronous test database engine
test_engine = create_async_engine(TEST_DATABASE_URL, future=True)

# Configure a session factory for test transactions
TestSessionLocal = sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)


# Override the default `get_db` dependency to use the test database
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


# Setup and teardown for database tables before/after each test
@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    """Ensures a clean database state for every test."""

    # Create tables before running the test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session  # Provide a fresh session for the test

    # Drop tables after the test to prevent conflicts
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
