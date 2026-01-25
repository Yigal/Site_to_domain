"""Tests for Saga pattern implementation."""

import pytest
from app.utils.saga_context import SagaContext, SagaStep, SagaOrchestrator


@pytest.mark.unit
def test_saga_context_initialization():
    """Test saga context initialization."""
    saga = SagaContext("task-123")
    assert saga.task_id == "task-123"
    assert saga.status == SagaStep.PENDING
    assert len(saga.steps) == 0


@pytest.mark.unit
def test_saga_context_add_step():
    """Test adding step to saga."""
    saga = SagaContext("task-123")
    saga.add_step(1, "Clone Repository", "clone", "cleanup_clone")

    assert 1 in saga.steps
    assert saga.steps[1]["name"] == "Clone Repository"
    assert saga.steps[1]["compensation"] == "cleanup_clone"


@pytest.mark.unit
def test_saga_context_execute_step():
    """Test executing step."""
    saga = SagaContext("task-123")
    saga.add_step(1, "Clone Repository", "clone", "cleanup_clone")
    saga.execute_step(1, {"cloned": True})

    assert saga.steps[1]["status"] == SagaStep.COMPLETED
    assert saga.steps[1]["result"] == {"cloned": True}
    assert (1, "cleanup_clone") in saga.compensations


@pytest.mark.unit
def test_saga_context_fail_step():
    """Test failing step."""
    saga = SagaContext("task-123")
    saga.add_step(1, "Clone Repository", "clone")
    saga.fail_step(1, "Clone failed")

    assert saga.steps[1]["status"] == SagaStep.FAILED
    assert saga.steps[1]["error"] == "Clone failed"
    assert saga.status == SagaStep.FAILED
    assert len(saga.errors) > 0


@pytest.mark.unit
def test_saga_context_execute_compensations():
    """Test executing compensations."""
    saga = SagaContext("task-123")
    saga.add_step(1, "Step 1", "action1", "comp1")
    saga.add_step(2, "Step 2", "action2", "comp2")

    saga.execute_step(1, {})
    saga.execute_step(2, {})

    result = saga.execute_compensations()
    assert result is True
    assert saga.status == SagaStep.COMPENSATED


@pytest.mark.unit
def test_saga_context_get_state():
    """Test getting saga state."""
    saga = SagaContext("task-123")
    saga.add_step(1, "Step 1", "action1")
    saga.execute_step(1, {"result": "ok"})

    state = saga.get_state()
    assert state["task_id"] == "task-123"
    assert "status" in state
    assert "steps" in state


@pytest.mark.unit
def test_saga_context_to_json():
    """Test serializing saga to JSON."""
    saga = SagaContext("task-123")
    saga.add_step(1, "Step 1", "action1")

    json_str = saga.to_json()
    assert isinstance(json_str, str)
    assert "task-123" in json_str


@pytest.mark.unit
def test_saga_orchestrator_initialization():
    """Test saga orchestrator initialization."""
    orchestrator = SagaOrchestrator()
    assert orchestrator is not None
    assert len(orchestrator.contexts) == 0


@pytest.mark.unit
def test_saga_orchestrator_create_saga():
    """Test creating saga."""
    orchestrator = SagaOrchestrator()
    saga = orchestrator.create_saga("task-123")

    assert saga is not None
    assert saga.task_id == "task-123"
    assert "task-123" in orchestrator.contexts


@pytest.mark.unit
def test_saga_orchestrator_get_saga():
    """Test getting saga."""
    orchestrator = SagaOrchestrator()
    saga1 = orchestrator.create_saga("task-123")
    saga2 = orchestrator.get_saga("task-123")

    assert saga1.task_id == saga2.task_id


@pytest.mark.unit
def test_saga_orchestrator_rollback_saga():
    """Test rollback saga."""
    orchestrator = SagaOrchestrator()
    saga = orchestrator.create_saga("task-123")
    saga.add_step(1, "Step 1", "action1", "comp1")
    saga.execute_step(1, {})

    result = orchestrator.rollback_saga("task-123")
    assert result is True
