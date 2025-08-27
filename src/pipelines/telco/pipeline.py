import time
from src.core.database import DatabaseSession
from .extract import TelcoExtractor
from .load import TelcoLoader
from .transform import TelcoTransformer
from src.models.logger import PipelineLogger


class TelcoPipeline:
    def __init__(self):
        self.extractor = TelcoExtractor()
        self.loader = TelcoLoader()
        self.transformer = TelcoTransformer()
        self.pipeline_logger = PipelineLogger("telco")
    
    async def run_elt(self):
        async with self.pipeline_logger.log_execution() as logger:
            
            # Extract
            start_time = time.time()
            raw_data = await self.extractor.extract_all()
            extract_duration = time.time() - start_time
            records_count = len(raw_data['customer_churn'])
            
            await logger.log_step("extract", extract_duration, records_count)

            # Load
            start_time = time.time()
            async with DatabaseSession() as session:
                await self.loader.load_raw_customer_churn(session, raw_data['customer_churn'])
            load_duration = time.time() - start_time
            
            await logger.log_step("load", load_duration, records_count)

            # Transform
            start_time = time.time()
            async with DatabaseSession() as session:
                await self.transformer.create_clean_customer_table(session)
            transform_duration = time.time() - start_time
            
            await logger.log_step("transform", transform_duration)