from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Address, User

AnyModel = User | Address


class DAO:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        statement = select(User).where(User.id == user_id)

        result = await self.session.execute(statement)
        return result.scalar()

    async def get_addresses_by_user_id(self, user_id: int) -> list[Address]:
        # In fact, useless method since we have User.addresses relationship,
        # but why not :)

        statement = select(Address).where(Address.user_id == user_id)

        result = await self.session.execute(statement)
        return result.scalars().all()

    def add(self, instance: AnyModel) -> None:
        self.session.add(instance=instance)

    async def commit(self) -> None:
        await self.session.commit()

    async def close(self) -> None:
        await self.session.close()
