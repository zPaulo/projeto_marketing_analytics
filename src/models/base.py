from datetime import datetime
from sqlalchemy.orm import registry, mapped_column
from enum import Enum

table_registry = registry()

class ExecutionPipelineStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@table_registry.mapped_as_dataclass
class LogsExecutionPipeline:
    __tablename__ = "logs_execution_pipeline"
    id: int = mapped_column(init=False, primary_key=True)
    pipeline_name: str = mapped_column(nullable=False)
    status: ExecutionPipelineStatus = mapped_column(nullable=False)
    start_time: datetime = mapped_column(nullable=False)
    end_time: datetime = mapped_column(nullable=False)
    detail: str = mapped_column(nullable=True)