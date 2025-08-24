# migrations/env.py
from logging.config import fileConfig
from alembic import context
from flask import current_app

# Import your SQLAlchemy Base directly
from app.db import Base

# 1) Alembic config + logging
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2) Provide DB URL and metadata
# Use the same DATABASE_URL your app uses
config.set_main_option("sqlalchemy.url", current_app.config["DATABASE_URL"])

# Point Alembic straight at your metadata
target_metadata = Base.metadata

# 3) Offline/online runners
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (no DB connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,                
        compare_server_default=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode (with DB connection)."""
    from sqlalchemy import engine_from_config, pool
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        is_sqlite = connection.dialect.name == "sqlite"
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_server_default=True,
            compare_type=True,      
            render_as_batch= is_sqlite       
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
