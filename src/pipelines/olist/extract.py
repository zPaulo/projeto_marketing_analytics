import polars as pl
from pathlib import Path
from typing import Dict

class OlistExtractor:
    def __inti__(self, data_path: str = "src/data/Olist_customers"):
        self.data_path = Path(data_path)

    async def extract_customers(self) -> pl.DataFrame:
        return pl.read_csv(
            self.data_path / "olist_customers_dataset.csv",
            try_parse_dates=True,
            null_values=["", "NA", "NULL"]
        )
    
    async def extract_geolocation(self) -> pl.DataFrame:
        return pl.read_csv(
            self.data_path / "olist_geolocation_dataset.csv",
            try_parse_dates=True,
            null_values=["", "NA", "NULL"]
        )
    
    async def extract_order_items(self) -> pl.DataFrame:
        return pl.read_csv(
            self.data_path / "olist_order_items_dataset.csv",
            try_parse_dates=True,
            null_values=["", "NA", "NULL"]
        )
    
    async def extract_order_payments(self) -> pl.DataFrame:
        return pl.read_csv(
            self.data_path / "olist_order_payments_dataset.csv",
            try_parse_dates=True,
            null_values=["", "NA", "NULL"]
        )
    
    async def extract_reviews(self) -> pl.DataFrame:
        return pl.read_csv(
            self.data_path / "olist_reviews_dataset.csv",
            try_parse_dates=True,
            null_values=["", "NA", "NULL"]
        )
    
    async def extract_products(self) -> pl.DataFrame:
        return pl.read_csv(
            self.data_path / "olist_products_dataset.csv",
            try_parse_dates=True,
            null_values=["", "NA", "NULL"]
        )
    
    async def extract_sellers(self) -> pl.DataFrame:
        return pl.read_csv(
            self.data_path / "olist_sellers_dataset.csv",
            try_parse_dates=True,
            null_values=["", "NA", "NULL"]
        )
    
    async def extract_category_name_translation(self) -> pl.DataFrame:
        return pl.read_csv(
            self.data_path / "olist_category_name_translation.csv",
            try_parse_dates=True,
            null_values=["", "NA", "NULL"]
        )
    
    async def extract_all(self) -> Dict[str, pl.DataFrame]:
        return {
            "customers": await self.extract_customers(),
            "geolocation": await self.extract_geolocation(),
            "order_items": await self.extract_order_items(),
            "order_payments": await self.extract_order_payments(),
            "reviews": await self.extract_reviews(),
            "products": await self.extract_products(),
            "sellers": await self.extract_sellers(),
            "category_name_translation": await self.extract_category_name_translation()
        }

