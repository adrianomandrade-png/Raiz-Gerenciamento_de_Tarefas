from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


def _utc_now() -> datetime:
    """Retorna a data e hora atuais em UTC."""
    return datetime.now(timezone.utc)


class TaskCreate(BaseModel):
    """Representa os dados necessários para criar ou atualizar uma tarefa."""

    title: str = Field(
        min_length=3,
        max_length=100,
        description="Título da tarefa, com entre 3 e 100 caracteres.",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Descrição opcional da tarefa.",
    )
    status: bool = Field(
        default=False,
        description="Indica se a tarefa foi concluída.",
    )


class Task(BaseModel):
    """Representa uma tarefa gerenciada pela API."""

    id: Optional[UUID] = Field(
        default=None,
        description="Identificador único da tarefa, opcional durante a criação.",
    )
    title: str = Field(
        min_length=3,
        max_length=100,
        description="Título da tarefa, com entre 3 e 100 caracteres.",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Descrição opcional da tarefa.",
    )
    status: bool = Field(
        default=False,
        description="Indica se a tarefa foi concluída.",
    )
    created_at: datetime = Field(
        default_factory=_utc_now,
        description="Data e hora de criação da tarefa.",
    )
