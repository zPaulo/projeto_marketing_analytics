import polars as pl
from pathlib import Path
from typing import Dict

class TelcoExtractor:
    def __init__(self, data_path: str = "src/data/Telco_customer_churn"):
        self.data_path = Path(data_path)

    async def extract_customer_churn(self) -> pl.DataFrame:
        return pl.read_csv(
            self.data_path / "Telco_Customer_Churn.csv",
            try_parse_dates=True,
            null_values=["", "NA", "NULL"]
        )

    async def extract_all(self) -> Dict[str, pl.DataFrame]:
        return {
            'customer_churn': await self.extract_customer_churn()
        }
    
