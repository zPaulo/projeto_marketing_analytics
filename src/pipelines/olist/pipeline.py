import time
from src.core.database import BronzeSession, SilverSession
from .extract import OlistExtractor
from .load import OlistLoader
from .transform import OlistTransformer
from src.models.logger import PipelineLogger

class OlistPipeline:
    def __init__(self):
        self.extractor = OlistExtractor()
        self.loader = OlistLoader()
        self.transformer = OlistTransformer()
        self.pipeline_logger = PipelineLogger("olist")

    async def run_elt(self):
        async with self.pipeline_logger.log_execution() as logger:

            # Extract
            start_time = time.time()
            raw_data = await self.extractor.extract_all()
            extract_duration = time.time() - start_time
            records_count = sum(
                len(df) for df in raw_data.values()
            )
            await logger.log_step("extract", extract_duration, records_count)

            # Load
            start_time = time.time()
            async with BronzeSession() as session:
                for table_name, df in raw_data.items():
                    await self.loader.load_raw_olist(session, df, table_name)
            load_duration = time.time() - start_time
            await logger.log_step("load", load_duration, records_count)

            # Transform
            start_time = time.time()
            async with SilverSession() as session:
                await self.transformer.create_clean_orders_enriched(session)
            transform_duration = time.time() - start_time

            await logger.log_step("transform", transform_duration)