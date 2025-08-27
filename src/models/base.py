from datetime import datetime
from sqlalchemy.orm import registry, mapped_column
from enum import Enum
from typing import Optional

table_registry = registry()

class ExecutionPipelineStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@table_registry.mapped_as_dataclass
class LogsPipelinesExecutions:
    __tablename__ = "logs_pipelines_executions"
    id: int = mapped_column(init=False, primary_key=True)
    pipeline_name: str = mapped_column(nullable=False)
    status: ExecutionPipelineStatus = mapped_column(nullable=False)
    start_time: datetime = mapped_column(nullable=False)
    end_time: Optional[datetime] = mapped_column(nullable=True, default=None)
    detail: Optional[str] = mapped_column(nullable=True, default=None)
    duration_seconds: Optional[float] = mapped_column(nullable=True, default=None)
    records_processed: Optional[int] = mapped_column(nullable=True, default=None)