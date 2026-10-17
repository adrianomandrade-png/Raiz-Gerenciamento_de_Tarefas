import logging
import os
from secrets import compare_digest
from typing import Final, Optional
from uuid import UUID

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status

from app.repositories import IRepository, ITaskRepository, TaskRepository
from app.repositories import UserRepository
from app.schemas import Task, TaskCreate, User
from app.services import EntityNotFoundError, TaskService, UserService

logger: Final[logging.Logger] = logging.getLogger(__name__)
configured_log_level: Final[str] = os.getenv("LOG_LEVEL", "INFO").upper()
_valid_log_levels: Final[frozenset[str]] = frozenset(
    {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"}
)
log_level: Final[str] = (
    configured_log_level if configured_log_level in _valid_log_levels else "INFO"
)
logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

task_repository: Final[ITaskRepository] = TaskRepository()
user_repository: Final[IRepository[User]] = UserRepository()


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
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A API não está configurada corretamente.",
        )

    if x_api_key is None or not compare_digest(x_api_key, configured_api_key):
        logger.warning(
            "event=api_key_validation_error "
            "message=Tentativa de autenticação inválida.",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "ApiKey"},
        )


def get_task_repository() -> ITaskRepository:
    """Retorna o repositório de tarefas para injeção de dependência.

    Returns:
        Repositório de tarefas compartilhado pela aplicação.
    """
    return task_repository


def get_user_repository() -> IRepository[User]:
    """Retorna o repositório de usuários para injeção de dependência.

    Returns:
        Repositório de usuários compartilhado pela aplicação.
    """
    return user_repository


def get_task_service(
    repository: ITaskRepository = Depends(get_task_repository),
) -> TaskService:
    """Retorna a instância do serviço de tarefas para injeção de dependência.

    Returns:
        Serviço de tarefas configurado com seu repositório.
    """
    return TaskService(repository)


def get_user_service(
    repository: IRepository[User] = Depends(get_user_repository),
) -> UserService:
    """Retorna a instância do serviço de usuários.

    Returns:
        Serviço de usuários configurado com seu repositório.
    """
    return UserService(repository)


app: Final[FastAPI] = FastAPI(
    title=os.getenv(
        "APP_TITLE",
        "Raiz — Gerenciamento de Tarefas",
    ),
    description="API RESTful para criação e gerenciamento de tarefas.",
    dependencies=[Depends(verify_api_key)],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Indica se a aplicação está disponível."""
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
async def list_tasks(
    task_status: Optional[bool] = Query(default=None, alias="status"),
    service: TaskService = Depends(get_task_service),
) -> list[Task]:
    """Lista tarefas, opcionalmente filtradas por status.

    Args:
        task_status: Filtra tarefas concluídas ou pendentes quando informado.
        service: Serviço de tarefas injetado pela aplicação.

    Returns:
        Lista de tarefas encontradas.
    """
    return await service.list_tasks(task_status)


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> Task:
    """Cria uma nova tarefa.

    Args:
        task_data: Dados validados da tarefa a ser criada.
        service: Serviço de tarefas injetado pela aplicação.

    Returns:
        A tarefa criada com UUID e data de criação.
    """
    return await service.create_task(task_data)


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
) -> Task:
    """Busca uma tarefa pelo UUID.

    Args:
        task_id: UUID da tarefa.
        service: Serviço de tarefas injetado pela aplicação.

    Returns:
        A tarefa correspondente ao UUID informado.

    Raises:
        HTTPException: Se a tarefa não for encontrada.
    """
    try:
        return await service.get_task(task_id)
    except EntityNotFoundError as error:
        logger.warning("event=task_not_found message=Tarefa não encontrada.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: UUID,
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> Task:
    """Atualiza uma tarefa existente.

    Args:
        task_id: UUID da tarefa.
        task_data: Novos dados validados da tarefa.
        service: Serviço de tarefas injetado pela aplicação.

    Returns:
        A tarefa atualizada.

    Raises:
        HTTPException: Se a tarefa não for encontrada.
    """
    try:
        return await service.update_task(task_id, task_data)
    except EntityNotFoundError as error:
        logger.warning(
            "event=task_update_not_found "
            "message=Tarefa não encontrada para atualização.",
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
) -> None:
    """Exclui uma tarefa pelo UUID.

    Args:
        task_id: UUID da tarefa.
        service: Serviço de tarefas injetado pela aplicação.

    Raises:
        HTTPException: Se a tarefa não for encontrada.
    """
    try:
        await service.delete_task(task_id)
    except EntityNotFoundError as error:
        logger.warning(
            "event=task_deletion_not_found "
            "message=Tarefa não encontrada para exclusão.",
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
