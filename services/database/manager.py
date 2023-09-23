from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from .models import Base


class ConnectionUrl:
    url_pattern = "postgresql+{connector}://{user}:{password}@{host}/{db_name}"

    def __init__(self, user: str, password: str, host: str, db_name: str):
        data = locals().copy()
        data.pop("self")

        self.data = data

    @property
    def sync_url(self) -> str:
        data = self.data.copy()
        data["connector"] = "psycopg2"

        return self.url_pattern.format(**data)

    @property
    def async_url(self) -> str:
        data = self.data.copy()
        data["connector"] = "asyncpg"

        return self.url_pattern.format(**data)


class DatabaseManager:
    def __init__(self, user: str, password: str, host: str, db_name: str) -> None:
        self.url = ConnectionUrl(
            user=user, password=password, host=host, db_name=db_name
        )
        self.base = Base
        self.engine = create_async_engine(url=self.url.async_url)
        self.session = sessionmaker(
            bind=self.engine, expire_on_commit=False, class_=AsyncSession
        )

    def create_database(self):
        url = self.url.sync_url
        if not database_exists(url=url):
            create_database(url=url)

    async def create_tables(self) -> None:
        connection = self.engine.connect()

        async with connection:
            await connection.run_sync(self.base.metadata.create_all)
            await connection.commit()

