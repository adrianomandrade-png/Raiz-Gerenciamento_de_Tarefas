import logging
import os
from secrets import compare_digest
from typing import Final, Optional
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from pydantic import ValidationError

from app.schemas import Task, TaskCreate

logger: Final[logging.Logger] = logging.getLogger(__name__)
configured_log_level: Final[str] = os.getenv("LOG_LEVEL", "INFO").upper()
_valid_log_levels: Final[frozenset[str]] = frozenset(
    {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"}
)
log_level: Final[str] = (
    configured_log_level
    if configured_log_level in _valid_log_levels
    else "INFO"
)
logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

tasks: dict[UUID, Task] = {}


async def verify_api_key(
    x_api_key: Optional[str] = Header(default=None),
) -> None:
    """Valida a API key enviada no cabeçalho da requisição.

    Args:
        x_api_key: API key enviada no cabeçalho ``X-API-Key``.

    Raises:
        HTTPException: Se a API key não estiver configurada ou for inválida.
    """
    configured_api_key = os.getenv("API_KEY")
    if not configured_api_key:
        logger.critical(
            "event=api_key_configuration_error message=API key não configurada.",
            extra={"event": "api_key_configuration_error"},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A API não está configurada corretamente.",
        )

    if x_api_key is None or not compare_digest(x_api_key, configured_api_key):
        logger.warning(
            "event=api_key_validation_error "
            "message=Tentativa de autenticação inválida.",
            extra={"event": "api_key_validation_error"},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "ApiKey"},
        )


app: Final[FastAPI] = FastAPI(
    title=os.getenv(
        "APP_TITLE",
        "Micro-API de Gerenciamento de Tarefas",
    ),
    description="API RESTful para criação e gerenciamento de tarefas.",
    dependencies=[Depends(verify_api_key)],
)


@app.get("/tasks", response_model=list[Task])
async def list_tasks(
    task_status: Optional[bool] = Query(default=None, alias="status"),
) -> list[Task]:
    """Lista tarefas, opcionalmente filtradas por status.

    Args:
        task_status: Filtra tarefas concluídas ou pendentes quando informado.

    Returns:
        Lista de tarefas encontradas.
    """
    if task_status is None:
        return list(tasks.values())

    return [task for task in tasks.values() if task.status == task_status]


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(task_data: TaskCreate) -> Task:
    """Cria uma nova tarefa.

    Args:
        task_data: Dados validados da tarefa a ser criada.

    Returns:
        A tarefa criada com UUID e data de criação.

    Raises:
        HTTPException: Se ocorrer um erro de validação ao criar a tarefa.
    """
    task_id = uuid4()
    try:
        task = Task(id=task_id, **task_data.model_dump())
    except ValidationError as error:
        logger.error(
            "event=task_creation_validation_error "
            "message=Falha de validação ao criar tarefa. error_type=%s",
            type(error).__name__,
            extra={"event": "task_creation_validation_error"},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível criar a tarefa.",
        ) from error

    tasks[task_id] = task
    return task


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: UUID) -> Task:
    """Busca uma tarefa pelo UUID.

    Args:
        task_id: UUID da tarefa.

    Returns:
        A tarefa correspondente ao UUID informado.

    Raises:
        HTTPException: Se a tarefa não for encontrada.
    """
    try:
        return tasks[task_id]
    except KeyError as error:
        logger.warning(
            "event=task_not_found message=Tarefa não encontrada.",
            extra={"event": "task_not_found"},
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada.",
        ) from error


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: UUID, task_data: TaskCreate) -> Task:
    """Atualiza uma tarefa existente.

    Args:
        task_id: UUID da tarefa.
        task_data: Novos dados validados da tarefa.

    Returns:
        A tarefa atualizada.

    Raises:
        HTTPException: Se a tarefa não existir ou falhar na validação.
    """
    try:
        existing_task = tasks[task_id]
    except KeyError as error:
        logger.warning(
            "event=task_update_not_found "
            "message=Tarefa não encontrada para atualização.",
            extra={"event": "task_update_not_found"},
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada.",
        ) from error

    try:
        updated_task = Task(
            id=task_id,
            created_at=existing_task.created_at,
            **task_data.model_dump(),
        )
    except ValidationError as error:
        logger.error(
            "event=task_update_validation_error "
            "message=Falha de validação ao atualizar tarefa. error_type=%s",
            type(error).__name__,
            extra={"event": "task_update_validation_error"},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível atualizar a tarefa.",
        ) from error

    tasks[task_id] = updated_task
    return updated_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(task_id: UUID) -> None:
    """Exclui uma tarefa pelo UUID.

    Args:
        task_id: UUID da tarefa.

    Raises:
        HTTPException: Se a tarefa não existir.
    """
    try:
        del tasks[task_id]
    except KeyError as error:
        logger.warning(
            "event=task_deletion_not_found "
            "message=Tarefa não encontrada para exclusão.",
            extra={"event": "task_deletion_not_found"},
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada.",
        ) from error
