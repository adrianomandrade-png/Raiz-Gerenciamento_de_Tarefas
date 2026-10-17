from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

AUTH_HEADERS: Dict[str, str] = {"X-API-Key": "test-api-key"}


def test_create_task_with_valid_data_returns_created_task(
    client: TestClient,
) -> None:
    """Cria uma tarefa válida e retorna seus campos gerados."""
    response = client.post(
        "/tasks",
        headers=AUTH_HEADERS,
        json={
            "title": "Estudar testes automatizados",
            "description": "Cobrir os fluxos principais.",
        },
    )

    assert response.status_code == 201
    payload: Dict[str, Any] = response.json()
    assert payload["title"] == "Estudar testes automatizados"
    assert payload["description"] == "Cobrir os fluxos principais."
    assert payload["status"] is False
    assert payload["id"]
    assert payload["created_at"]


def test_list_tasks_filters_by_status(client: TestClient) -> None:
    """Retorna somente tarefas compatíveis com o filtro informado."""
    for title, task_status in (("Pendente", False), ("Concluída", True)):
        response = client.post(
            "/tasks",
            headers=AUTH_HEADERS,
            json={"title": title, "status": task_status},
        )
        assert response.status_code == 201

    response = client.get("/tasks?status=true", headers=AUTH_HEADERS)

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Concluída"
    assert tasks[0]["status"] is True


def test_list_tasks_returns_all_created_tasks(client: TestClient) -> None:
    """Lista todas as tarefas criadas quando nenhum filtro é informado."""
    for title in ("Primeira tarefa", "Segunda tarefa"):
        response = client.post(
            "/tasks",
            headers=AUTH_HEADERS,
            json={"title": title},
        )
        assert response.status_code == 201

    response = client.get("/tasks", headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert {task["title"] for task in response.json()} == {
        "Primeira tarefa",
        "Segunda tarefa",
    }


def test_update_task_changes_status_to_completed(client: TestClient) -> None:
    """Atualiza o status de uma tarefa para concluída."""
    created = client.post(
        "/tasks",
        headers=AUTH_HEADERS,
        json={"title": "Finalizar implementação"},
    )
    task_id = created.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        headers=AUTH_HEADERS,
        json={"title": "Finalizar implementação", "status": True},
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["status"] is True


def test_delete_task_removes_existing_task(client: TestClient) -> None:
    """Exclui uma tarefa existente e impede nova busca por ela."""
    created = client.post(
        "/tasks",
        headers=AUTH_HEADERS,
        json={"title": "Tarefa temporária"},
    )
    task_id = created.json()["id"]

    delete_response = client.delete(
        f"/tasks/{task_id}",
        headers=AUTH_HEADERS,
    )
    get_response = client.get(
        f"/tasks/{task_id}",
        headers=AUTH_HEADERS,
    )

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


@pytest.mark.parametrize("title", ["ab", "a" * 101])
def test_create_task_rejects_title_outside_length_limits(
    client: TestClient,
    title: str,
) -> None:
    """Rejeita títulos menores que 3 ou maiores que 100 caracteres."""
    response = client.post(
        "/tasks",
        headers=AUTH_HEADERS,
        json={"title": title},
    )

    assert response.status_code == 422


@pytest.mark.parametrize("title", ["abc", "a" * 100])
def test_create_task_accepts_title_at_length_boundaries(
    client: TestClient,
    title: str,
) -> None:
    """Aceita títulos exatamente nos limites definidos pelo Field."""
    response = client.post(
        "/tasks",
        headers=AUTH_HEADERS,
        json={"title": title},
    )

    assert response.status_code == 201


def test_get_task_with_unknown_uuid_returns_not_found(
    client: TestClient,
) -> None:
    """Retorna 404 ao buscar uma tarefa inexistente."""
    response = client.get(
        "/tasks/00000000-0000-0000-0000-000000000000",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada."


def test_delete_task_with_unknown_uuid_returns_not_found(
    client: TestClient,
) -> None:
    """Retorna 404 ao excluir uma tarefa inexistente."""
    response = client.delete(
        "/tasks/00000000-0000-0000-0000-000000000000",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada."


def test_task_endpoint_rejects_malformed_uuid(client: TestClient) -> None:
    """Retorna 422 quando o identificador não é um UUID válido."""
    response = client.get("/tasks/not-a-uuid", headers=AUTH_HEADERS)

    assert response.status_code == 422


def test_task_endpoint_requires_api_key(client: TestClient) -> None:
    """Rejeita requisições sem a API key obrigatória."""
    response = client.get("/tasks")

    assert response.status_code == 401


def test_task_endpoint_rejects_invalid_api_key(client: TestClient) -> None:
    """Rejeita requisições com API key inválida."""
    response = client.get(
        "/tasks",
        headers={"X-API-Key": "invalid-key"},
    )

    assert response.status_code == 401
