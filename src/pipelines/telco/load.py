import polars as pl
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import DatabaseSession

class TelcoLoader:
    """
    Carrega os dados brutos de churn de clientes.
    """
    async def load_raw_telco(
        self, 
        session: AsyncSession, 
        df: pl.DataFrame,
        table_name: str
    ):
        pandas_df = df.to_pandas()
        await session.run_sync(
            lambda sync_session: pandas_df.to_sql(
                table_name,
                sync_session.get_bind(),
                if_exists="replace",
                index=False
            )
        )