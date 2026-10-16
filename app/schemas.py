from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Representa os dados necessários para criar ou atualizar uma tarefa."""

    title: str = Field(
        min_length=3,
        max_length=100,
        description="Título da tarefa, com entre 3 e 100 caracteres.",
    )
    description: str | None = Field(
        default=None,
        description="Descrição opcional da tarefa.",
    )
    status: bool = Field(
        default=False,
        description="Indica se a tarefa foi concluída.",
    )


class Task(BaseModel):
    """Representa uma tarefa gerenciada pela API."""

    id: UUID | None = Field(
        default=None,
        description="Identificador único da tarefa, opcional durante a criação.",
    )
    title: str = Field(
        min_length=3,
        max_length=100,
        description="Título da tarefa, com entre 3 e 100 caracteres.",
    )
    description: str | None = Field(
        default=None,
        description="Descrição opcional da tarefa.",
    )
    status: bool = Field(
        default=False,
        description="Indica se a tarefa foi concluída.",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Data e hora de criação da tarefa.",
    )
