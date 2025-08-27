import sys
import os
import asyncio

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.pipelines.telco.pipeline import TelcoPipeline

async def main():
    pipeline = TelcoPipeline()
    await pipeline.run_elt()

# Para testes
if __name__ == "__main__":
    asyncio.run(main())