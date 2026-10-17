import asyncio
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_task_repository

API_KEY = "test-api-key"


async def clear_task_repository() -> None:
    """Remove todas as tarefas do repositório compartilhado."""
    repository = get_task_repository()
    for task in await repository.list():
        if task.id is not None:
            await repository.delete(task.id)


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    """Fornece um cliente autenticado com armazenamento isolado."""
    monkeypatch.setenv("API_KEY", API_KEY)
    asyncio.run(clear_task_repository())

    with TestClient(app) as test_client:
        yield test_client

    asyncio.run(clear_task_repository())
