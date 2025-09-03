from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from .settings import settings
from src.models.base import bronze_registry, silver_registry
import logging

# Mesma engine para ambos os schemas
database_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

BronzeSessionMaker = sessionmaker(
    bind=database_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

SilverSessionMaker = sessionmaker(
    bind=database_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def create_databases():
    """
    Cria os schemas Bronze e Silver se não existirem.
    """
    # Criar schemas se não existirem
    async with database_engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze"))
        await conn.run_sync(bronze_registry.metadata.create_all)

        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver"))
        await conn.run_sync(silver_registry.metadata.create_all)

# Context manager para pipelines (recomendado para seu caso)
class DatabaseSession:
    def __init__(self, session_type: str = "bronze"):
        self.session = None
        self.session_type = session_type

    async def __aenter__(self):
        # Garante que os bancos existam
        if self.session_type in ["bronze", "silver"]:
            await create_databases()

        if self.session_type == "bronze":
            self.session = BronzeSessionMaker()
        elif self.session_type == "silver":
            self.session = SilverSessionMaker()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
        except Exception as e:
            logging.error(f"Erro ao finalizar a sessão: {e}")
        finally:
            await self.session.close()
            logging.info("Sessão finalizada.")

# Aliases para facilitar uso
class BronzeSession(DatabaseSession):
    def __init__(self):
        super().__init__("bronze")

class SilverSession(DatabaseSession):
    def __init__(self):
        super().__init__("silver")