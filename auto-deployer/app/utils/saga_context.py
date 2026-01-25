"""Saga Pattern implementation for distributed transactions."""

import json
import structlog
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime

logger = structlog.get_logger()


class SagaStep(Enum):
    """Saga step states."""
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"


class SagaContext:
    """Manage saga execution context and compensating transactions."""

    def __init__(self, task_id: str):
        """Initialize saga context."""
        self.task_id = task_id
        self.steps: Dict[int, Dict[str, Any]] = {}
        self.compensations: List[tuple] = []
        self.status = SagaStep.PENDING
        self.created_at = datetime.now().isoformat()
        self.errors: List[str] = []
        logger.info("saga_context_initialized", task_id=task_id)

    def add_step(
        self,
        step_number: int,
        step_name: str,
        action: str,
        compensation: Optional[str] = None,
    ) -> None:
        """Add step to saga."""
        self.steps[step_number] = {
            "number": step_number,
            "name": step_name,
            "action": action,
            "compensation": compensation,
            "status": SagaStep.PENDING,
            "result": None,
            "error": None,
        }
        logger.info(
            "saga_step_added",
            task_id=self.task_id,
            step=step_number,
            name=step_name,
        )

    def execute_step(
        self,
        step_number: int,
        result: Any,
    ) -> None:
        """Mark step as executed."""
        if step_number in self.steps:
            self.steps[step_number]["status"] = SagaStep.COMPLETED
            self.steps[step_number]["result"] = result
            logger.info(
                "saga_step_executed",
                task_id=self.task_id,
                step=step_number,
            )
            # Register compensation if provided
            if self.steps[step_number]["compensation"]:
                self.compensations.append(
                    (step_number, self.steps[step_number]["compensation"])
                )

    def fail_step(
        self,
        step_number: int,
        error: str,
    ) -> None:
        """Mark step as failed."""
        if step_number in self.steps:
            self.steps[step_number]["status"] = SagaStep.FAILED
            self.steps[step_number]["error"] = error
            self.errors.append(f"Step {step_number}: {error}")
            self.status = SagaStep.FAILED
            logger.error(
                "saga_step_failed",
                task_id=self.task_id,
                step=step_number,
                error=error,
            )

    def execute_compensations(self) -> bool:
        """Execute all compensating transactions in reverse order."""
        try:
            logger.info(
                "saga_compensations_start",
                task_id=self.task_id,
                count=len(self.compensations),
            )
            self.status = SagaStep.COMPENSATING

            # Execute in reverse order (LIFO - Last In First Out)
            for step_number, compensation in reversed(self.compensations):
                try:
                    logger.info(
                        "saga_compensation_executing",
                        step=step_number,
                        action=compensation,
                    )
                    # In production, would execute actual compensation logic
                    self.steps[step_number]["status"] = SagaStep.COMPENSATED
                    logger.info(
                        "saga_compensation_success",
                        step=step_number,
                    )
                except Exception as e:
                    logger.error(
                        "saga_compensation_failed",
                        step=step_number,
                        error=str(e),
                    )

            self.status = SagaStep.COMPENSATED
            logger.info("saga_compensations_complete", task_id=self.task_id)
            return True
        except Exception as e:
            logger.error("saga_compensations_failed", task_id=self.task_id, error=str(e))
            return False

    def get_state(self) -> Dict[str, Any]:
        """Get current saga state."""
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "steps": self.steps,
            "compensations_registered": len(self.compensations),
            "errors": self.errors,
            "created_at": self.created_at,
        }

    def to_json(self) -> str:
        """Serialize saga context to JSON."""
        return json.dumps(
            {
                "task_id": self.task_id,
                "status": self.status.value,
                "created_at": self.created_at,
                "errors": self.errors,
                "steps_count": len(self.steps),
                "compensations_count": len(self.compensations),
            }
        )


class SagaOrchestrator:
    """Orchestrate saga execution."""

    def __init__(self):
        """Initialize saga orchestrator."""
        self.contexts: Dict[str, SagaContext] = {}
        logger.info("saga_orchestrator_initialized")

    def create_saga(self, task_id: str) -> SagaContext:
        """Create new saga context."""
        context = SagaContext(task_id)
        self.contexts[task_id] = context
        return context

    def get_saga(self, task_id: str) -> Optional[SagaContext]:
        """Get saga context."""
        return self.contexts.get(task_id)

    def rollback_saga(self, task_id: str) -> bool:
        """Rollback saga by executing compensations."""
        context = self.get_saga(task_id)
        if context:
            return context.execute_compensations()
        return False


# Singleton instances
saga_orchestrator = SagaOrchestrator()
