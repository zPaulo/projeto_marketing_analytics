import logging
from datetime import datetime
from contextlib import asynccontextmanager
from src.core.database import DatabaseSession
from src.models.base import LogsPipelinesExecutions, ExecutionPipelineStatus
from sqlalchemy import select, update

class PipelineLogger:
    def __init__(self, pipeline_name: str):
        self.pipeline_name = pipeline_name
        self.logger = logging.getLogger(f"pipeline.{pipeline_name}")
        self.execution_log = None
        self.start_time = None
    
    @asynccontextmanager
    async def log_execution(self):
        """Context manager para logging automático"""
        self.start_time = datetime.now()
        
        # Cria log inicial
        self.execution_log = LogsPipelinesExecutions(
            pipeline_name=self.pipeline_name,
            status=ExecutionPipelineStatus.PENDING,
            start_time=self.start_time,
            detail="Pipeline iniciado"
        )
        
        # Salva status PENDING
        await self._save_log_status(ExecutionPipelineStatus.PENDING, "Pipeline iniciado")
        self.logger.info(f"🚀 Pipeline {self.pipeline_name} iniciado")
        
        try:
            # Atualiza para RUNNING
            await self._save_log_status(ExecutionPipelineStatus.RUNNING, "Pipeline em execução")
            self.logger.info(f"▶️ Pipeline {self.pipeline_name} em execução")
            
            yield self
            
            # Sucesso - COMPLETED
            duration = (datetime.now() - self.start_time).total_seconds()
            success_detail = f"Pipeline concluído com sucesso em {duration:.2f}s"
            await self._save_log_status(ExecutionPipelineStatus.COMPLETED, success_detail, duration)
            self.logger.info(f"✅ Pipeline {self.pipeline_name} concluído com sucesso")
            
        except Exception as e:
            # Erro - FAILED
            duration = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
            error_detail = f"Erro: {str(e)}"
            await self._save_log_status(ExecutionPipelineStatus.FAILED, error_detail, duration)
            self.logger.error(f"❌ Pipeline {self.pipeline_name} falhou: {e}")
            raise
    
    async def _save_log_status(self, status: ExecutionPipelineStatus, detail: str, duration: float = None, records_processed: int = None):
        """Salva o status atual no banco"""
        async with DatabaseSession() as session:
            current_time = datetime.now()
            
            if hasattr(self.execution_log, 'id') and self.execution_log.id:
                update_values = {
                    'status': status,
                    'end_time': current_time,
                    'detail': detail
                }
                
                if duration is not None:
                    update_values['duration_seconds'] = duration
                
                if records_processed is not None:
                    update_values['records_processed'] = records_processed
                
                stmt = update(LogsPipelinesExecutions).where(
                    LogsPipelinesExecutions.id == self.execution_log.id
                ).values(**update_values)
                await session.execute(stmt)
                
            else:  # Primeira vez, cria novo
                self.execution_log.status = status
                self.execution_log.detail = detail
                self.execution_log.end_time = current_time
                if duration:
                    self.execution_log.duration_seconds = duration
                if records_processed is not None:
                    self.execution_log.records_processed = records_processed
                    
                session.add(self.execution_log)
                await session.flush()  # Para pegar o ID
            
            await session.commit()

    async def log_step(self, step_name: str, duration: float, records_processed: int = 0):
        """Log de etapas individuais"""
        step_detail = f"Etapa {step_name} concluída em {duration:.2f}s"
        if records_processed > 0:
            step_detail += f" - {records_processed} registros processados"
            
        self.logger.info(f"📊 {step_detail}")
        
        # Atualiza o detail com progresso
        current_detail = self.execution_log.detail or ""
        updated_detail = f"{current_detail}\n{step_detail}"
        
        # Atualiza records_processed se fornecido
        total_records = None
        if records_processed > 0:
            if self.execution_log.records_processed is None:
                self.execution_log.records_processed = records_processed
            else:
                self.execution_log.records_processed += records_processed
            total_records = self.execution_log.records_processed
            
        await self._save_log_status(ExecutionPipelineStatus.RUNNING, updated_detail, records_processed=total_records)