from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Query, status  # pyright: ignore[reportMissingImports]

from app.schemas import Task, TaskCreate

app = FastAPI(
    title="Micro-API de Gerenciamento de Tarefas",
    description="API RESTful para criação e gerenciamento de tarefas.",
)

tasks: dict[UUID, Task] = {}


@app.get("/tasks", response_model=list[Task])
def list_tasks(
    task_status: bool | None = Query(default=None, alias="status"),
) -> list[Task]:
    """Lista todas as tarefas, opcionalmente filtradas por status.

    Args:
        task_status: Filtra as tarefas concluídas ou pendentes quando informado.

    Returns:
        Uma lista de tarefas.
    """
    if task_status is None:
        return list(tasks.values())

    return [task for task in tasks.values() if task.status == task_status]


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task_data: TaskCreate) -> Task:
    """Cria uma nova tarefa.

    Args:
        task_data: Dados da tarefa a ser criada.

    Returns:
        A tarefa criada com seu UUID e data de criação.
    """
    task_id = uuid4()
    task = Task(id=task_id, **task_data.model_dump())
    tasks[task_id] = task
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: UUID) -> Task:
    """Busca uma tarefa pelo UUID.

    Args:
        task_id: UUID da tarefa.

    Returns:
        A tarefa correspondente ao UUID informado.

    Raises:
        HTTPException: Caso a tarefa não seja encontrada.
    """
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada.",
        )
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_data: TaskCreate) -> Task:
    """Atualiza uma tarefa existente.

    Args:
        task_id: UUID da tarefa.
        task_data: Novos dados da tarefa.

    Returns:
        A tarefa atualizada.

    Raises:
        HTTPException: Caso a tarefa não seja encontrada.
    """
    existing_task = tasks.get(task_id)
    if existing_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada.",
        )

    updated_task = Task(
        id=task_id,
        created_at=existing_task.created_at,
        **task_data.model_dump(),
    )
    tasks[task_id] = updated_task
    return updated_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: UUID) -> None:
    """Exclui uma tarefa pelo UUID.

    Args:
        task_id: UUID da tarefa.

    Raises:
        HTTPException: Caso a tarefa não seja encontrada.
    """
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada.",
        )

    del tasks[task_id]
