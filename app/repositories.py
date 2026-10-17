from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Optional, TypeVar
from uuid import UUID

from app.schemas import Task, User

EntityT = TypeVar("EntityT")


class IRepository(ABC, Generic[EntityT]):
    """Define operações assíncronas de persistência para uma entidade."""

    @abstractmethod
    async def get(self, entity_id: UUID) -> Optional[EntityT]:
        """Busca uma entidade pelo identificador."""
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[EntityT]:
        """Lista todas as entidades."""
        raise NotImplementedError

    @abstractmethod
    async def add(self, entity: EntityT) -> EntityT:
        """Persiste uma nova entidade."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: EntityT) -> Optional[EntityT]:
        """Atualiza uma entidade existente."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        """Exclui uma entidade e informa se ela existia."""
        raise NotImplementedError


class ITaskRepository(IRepository[Task], ABC):
    """Define operações específicas de persistência de tarefas."""

    @abstractmethod
    async def list_by_status(self, task_status: Optional[bool]) -> List[Task]:
        """Lista tarefas filtradas opcionalmente pelo status."""
        raise NotImplementedError


class UserRepository(IRepository[User]):
    """Implementa a persistência de usuários em memória."""

    def __init__(self) -> None:
        """Inicializa o armazenamento isolado de usuários."""
        self._users: Dict[UUID, User] = {}

    async def get(self, entity_id: UUID) -> Optional[User]:
        """Busca um usuário pelo identificador.

        Args:
            entity_id: UUID do usuário.

        Returns:
            O usuário encontrado ou ``None``.
        """
        return self._users.get(entity_id)

    async def list(self) -> List[User]:
        """Lista os usuários persistidos.

        Returns:
            Lista de usuários.
        """
        return list(self._users.values())

    async def add(self, entity: User) -> User:
        """Persiste um novo usuário.

        Args:
            entity: Usuário a ser persistido.

        Returns:
            O usuário persistido.

        Raises:
            ValueError: Se o usuário não tiver UUID.
        """
        if entity.id is None:
            raise ValueError("O usuário precisa de um UUID para ser persistido.")
        self._users[entity.id] = entity
        return entity

    async def update(self, entity: User) -> Optional[User]:
        """Atualiza um usuário existente.

        Args:
            entity: Usuário com os dados atualizados.

        Returns:
            O usuário atualizado ou ``None`` se não existir.
        """
        if entity.id is None or entity.id not in self._users:
            return None
        self._users[entity.id] = entity
        return entity

    async def delete(self, entity_id: UUID) -> bool:
        """Exclui um usuário pelo UUID.

        Args:
            entity_id: UUID do usuário.

        Returns:
            ``True`` quando um usuário foi excluído; caso contrário, ``False``.
        """
        if entity_id not in self._users:
            return False
        del self._users[entity_id]
        return True


class TaskRepository(ITaskRepository):
    """Implementa a persistência de tarefas em memória."""

    def __init__(self) -> None:
        """Inicializa o armazenamento isolado de tarefas."""
        self._tasks: Dict[UUID, Task] = {}

    async def get(self, entity_id: UUID) -> Optional[Task]:
        """Busca uma tarefa pelo identificador.

        Args:
            entity_id: UUID da tarefa.

        Returns:
            A tarefa encontrada ou ``None``.
        """
        return self._tasks.get(entity_id)

    async def list(self) -> List[Task]:
        """Lista as tarefas persistidas.

        Returns:
            Lista de tarefas.
        """
        return list(self._tasks.values())

    async def list_by_status(self, task_status: Optional[bool]) -> List[Task]:
        """Lista tarefas filtradas opcionalmente pelo status.

        Args:
            task_status: Status desejado ou ``None`` para todos os registros.

        Returns:
            Lista de tarefas compatíveis com o filtro.
        """
        if task_status is None:
            return await self.list()
        return [task for task in self._tasks.values() if task.status == task_status]

    async def add(self, entity: Task) -> Task:
        """Persiste uma nova tarefa.

        Args:
            entity: Tarefa a ser persistida.

        Returns:
            A tarefa persistida.

        Raises:
            ValueError: Se a tarefa não tiver UUID.
        """
        if entity.id is None:
            raise ValueError("A tarefa precisa de um UUID para ser persistida.")
        self._tasks[entity.id] = entity
        return entity

    async def update(self, entity: Task) -> Optional[Task]:
        """Atualiza uma tarefa existente.

        Args:
            entity: Tarefa com os dados atualizados.

        Returns:
            A tarefa atualizada ou ``None`` se não existir.
        """
        if entity.id is None or entity.id not in self._tasks:
            return None
        self._tasks[entity.id] = entity
        return entity

    async def delete(self, entity_id: UUID) -> bool:
        """Exclui uma tarefa pelo UUID.

        Args:
            entity_id: UUID da tarefa.

        Returns:
            ``True`` quando uma tarefa foi excluída; caso contrário, ``False``.
        """
        if entity_id not in self._tasks:
            return False
        del self._tasks[entity_id]
        return True
