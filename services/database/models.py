from typing import Annotated

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

str256 = Annotated[str, 256]


class Base(AsyncAttrs, DeclarativeBase):
    type_annotation_map = {
        str256: String(256),
    }


class PrettyRepr:
    def __repr__(self: Base) -> str:
        columns_info = ", ".join(
            [
                f"{name}={repr(self.__dict__[name])}"
                for name in self.__table__.columns.keys()
            ]
        )
        return f"{self.__class__.__name__}({columns_info})"


class User(Base, PrettyRepr):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    addresses: Mapped[list["Address"]] = relationship(back_populates="user")


class Address(Base, PrettyRepr):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str256]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
