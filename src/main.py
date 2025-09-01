import sys
import os
import asyncio

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.pipelines.telco.pipeline import TelcoPipeline
from src.pipelines.olist.pipeline import OlistPipeline


async def main():

    pipeline_olist = OlistPipeline()
    await pipeline_olist.run_elt()

    pipeline_telco = TelcoPipeline()
    await pipeline_telco.run_elt()

# Para testes
if __name__ == "__main__":
    asyncio.run(main())