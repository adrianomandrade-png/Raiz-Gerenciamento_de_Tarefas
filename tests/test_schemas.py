import pytest
from pydantic import ValidationError

from app.schemas import TaskCreate


@pytest.mark.parametrize("title", ["ab", "a" * 101])
def test_task_create_rejects_title_outside_field_limits(title: str) -> None:
    """Levanta ValidationError para títulos fora dos limites do Field."""
    with pytest.raises(ValidationError):
        TaskCreate(title=title)


def test_task_create_accepts_required_title_and_default_status() -> None:
    """Cria o modelo com título válido e status padrão pendente."""
    task = TaskCreate(title="Uma tarefa válida")

    assert task.title == "Uma tarefa válida"
    assert task.status is False
    assert task.description is None


def test_task_create_rejects_description_longer_than_field_limit() -> None:
    """Levanta ValidationError para descrição maior que 1000 caracteres."""
    with pytest.raises(ValidationError):
        TaskCreate(title="Tarefa válida", description="a" * 1001)
