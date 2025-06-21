import os 
import sys
from logging.config import fileConfig

from decouple import config as decouple_config 

from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context

alembic_config = context.config

if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name) 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.models import Base

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    ...
    """
    url = decouple_config("DATABASE_URL")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    db_url = decouple_config("DATABASE_URL")
    connectable = create_engine(db_url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()