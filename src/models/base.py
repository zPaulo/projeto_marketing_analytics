from datetime import datetime
from sqlalchemy.orm import registry, mapped_column, DeclarativeBase
from enum import Enum
from typing import Optional

# Registry separado para cada camada
bronze_registry = registry()
silver_registry = registry()
logs_registry = registry()

class BronzeBase(DeclarativeBase):
    registry = bronze_registry

class SilverBase(DeclarativeBase):
    registry = silver_registry

class LogsBase(DeclarativeBase):
    registry = logs_registry

# Enums para logs
class ExecutionPipelineStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

# modelos de logs
@logs_registry.mapped_as_dataclass
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