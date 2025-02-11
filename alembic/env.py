import os
from logging.config import fileConfig
from app.core.config import settings
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from sqlalchemy import pool
from alembic import context
from app.models.geolocation import Base

# Load Alembic configuration
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for database migrations
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode without a database connection."""
    url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
    if not url:
        raise ValueError("❌ DATABASE_URL is not set!")

    config.set_main_option("sqlalchemy.url", url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in online mode with a database connection."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        future=True,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_migrations)


def do_migrations(connection: AsyncConnection) -> None:
    """Apply migrations using an active database connection."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


# Determine migration mode based on environment
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())  # Run async function correctly