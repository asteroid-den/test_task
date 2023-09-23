from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from services.database import DatabaseManager, DAO


class DAOMiddleware(BaseMiddleware):
    def __init__(self, database_manager: DatabaseManager) -> None:
        self.database_manager = database_manager

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        dao = DAO(session=self.database_manager.session())

        data["dao"] = dao
        await handler(event, data)

        await dao.close()

