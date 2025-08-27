import polars as pl
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import DatabaseSession

class TelcoLoader:
    """
    Carrega os dados brutos de churn de clientes.
    """
    async def load_raw_customer_churn(
        self, 
        session: AsyncSession, 
        df: pl.DataFrame
    ):
        pandas_df = df.to_pandas()
        await session.run_sync(
            lambda sync_session: pandas_df.to_sql(
                "raw_customer_churn",
                sync_session.get_bind(),
                if_exists="replace",
                index=False
            )
        )