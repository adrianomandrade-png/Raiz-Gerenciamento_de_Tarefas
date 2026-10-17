from typing import List, Optional
from uuid import UUID, uuid4

from app.repositories import IRepository, ITaskRepository
from app.schemas import Task, TaskCreate, User, UserCreate


class EntityNotFoundError(LookupError):
    """Indica que uma entidade solicitada não foi encontrada."""


class TaskService:
    """Orquestra as regras de negócio relacionadas às tarefas."""

    def __init__(self, repository: ITaskRepository) -> None:
        """Inicializa o serviço com seu repositório.

        Args:
            repository: Repositório responsável pela persistência de tarefas.
        """
        self._repository: ITaskRepository = repository

    async def list_tasks(self, task_status: Optional[bool]) -> List[Task]:
        """Lista tarefas com filtro opcional de status.

        Args:
            task_status: Status desejado ou ``None`` para todas as tarefas.

        Returns:
            Lista de tarefas encontradas.
        """
        return await self._repository.list_by_status(task_status)

    async def create_task(self, task_data: TaskCreate) -> Task:
        """Cria e persiste uma tarefa.

        Args:
            task_data: Dados validados da tarefa.

        Returns:
            A tarefa criada.
        """
        task = Task(id=uuid4(), **task_data.model_dump())
        return await self._repository.add(task)

    async def get_task(self, task_id: UUID) -> Task:
        """Busca uma tarefa ou informa que ela não existe.

        Args:
            task_id: UUID da tarefa.

        Returns:
            A tarefa encontrada.

        Raises:
            EntityNotFoundError: Se a tarefa não existir.
        """
        task = await self._repository.get(task_id)
        if task is None:
            raise EntityNotFoundError("Tarefa não encontrada.")
        return task

    async def update_task(
        self,
        task_id: UUID,
        task_data: TaskCreate,
    ) -> Task:
        """Atualiza uma tarefa preservando seus metadados.

        Args:
            task_id: UUID da tarefa.
            task_data: Novos dados validados da tarefa.

        Returns:
            A tarefa atualizada.

        Raises:
            EntityNotFoundError: Se a tarefa não existir.
        """
        existing_task = await self.get_task(task_id)
        updated_task = Task(
            id=task_id,
            created_at=existing_task.created_at,
            **task_data.model_dump(),
        )
        result = await self._repository.update(updated_task)
        if result is None:
            raise EntityNotFoundError("Tarefa não encontrada.")
        return result

    async def delete_task(self, task_id: UUID) -> None:
        """Exclui uma tarefa.

        Args:
            task_id: UUID da tarefa.

        Raises:
            EntityNotFoundError: Se a tarefa não existir.
        """
        if not await self._repository.delete(task_id):
            raise EntityNotFoundError("Tarefa não encontrada.")


class UserService:
    """Orquestra as regras de negócio relacionadas aos usuários."""

    def __init__(self, repository: IRepository[User]) -> None:
        """Inicializa o serviço com seu repositório.

        Args:
            repository: Repositório responsável pela persistência de usuários.
        """
        self._repository: IRepository[User] = repository

    async def list_users(self) -> List[User]:
        """Lista os usuários persistidos.

        Returns:
            Lista de usuários.
        """
        return await self._repository.list()

    async def create_user(self, user_data: UserCreate) -> User:
        """Cria e persiste um usuário.

        Args:
            user_data: Dados validados do usuário.

        Returns:
            O usuário criado.
        """
        user = User(id=uuid4(), **user_data.model_dump())
        return await self._repository.add(user)

    async def get_user(self, user_id: UUID) -> User:
        """Busca um usuário ou informa que ele não existe.

        Args:
            user_id: UUID do usuário.

        Returns:
            O usuário encontrado.

        Raises:
            EntityNotFoundError: Se o usuário não existir.
        """
        user = await self._repository.get(user_id)
        if user is None:
            raise EntityNotFoundError("Usuário não encontrado.")
        return user

    async def update_user(
        self,
        user_id: UUID,
        user_data: UserCreate,
    ) -> User:
        """Atualiza um usuário preservando sua identidade e criação.

        Args:
            user_id: UUID do usuário.
            user_data: Novos dados validados do usuário.

        Returns:
            O usuário atualizado.

        Raises:
            EntityNotFoundError: Se o usuário não existir.
        """
        existing_user = await self.get_user(user_id)
        updated_user = User(
            id=user_id,
            created_at=existing_user.created_at,
            **user_data.model_dump(),
        )
        result = await self._repository.update(updated_user)
        if result is None:
            raise EntityNotFoundError("Usuário não encontrado.")
        return result

    async def delete_user(self, user_id: UUID) -> None:
        """Exclui um usuário.

        Args:
            user_id: UUID do usuário.

        Raises:
            EntityNotFoundError: Se o usuário não existir.
        """
        if not await self._repository.delete(user_id):
            raise EntityNotFoundError("Usuário não encontrado.")
