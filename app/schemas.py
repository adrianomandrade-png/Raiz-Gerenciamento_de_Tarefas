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


class UserCreate(BaseModel):
    """Representa os dados necessários para criar um usuário."""

    username: str = Field(
        min_length=3,
        max_length=50,
        description="Nome de usuário, com entre 3 e 50 caracteres.",
    )
    email: str = Field(
        min_length=5,
        max_length=254,
        description="Endereço de e-mail do usuário.",
    )


class User(BaseModel):
    """Representa um usuário da API."""

    id: Optional[UUID] = Field(
        default=None,
        description="Identificador único do usuário.",
    )
    username: str = Field(
        min_length=3,
        max_length=50,
        description="Nome de usuário, com entre 3 e 50 caracteres.",
    )
    email: str = Field(
        min_length=5,
        max_length=254,
        description="Endereço de e-mail do usuário.",
    )
    created_at: datetime = Field(
        default_factory=_utc_now,
        description="Data e hora de criação do usuário.",
    )
