from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

# https://sqlmodel.tiangolo.com/tutorial/code-structure/#make-circular-imports-work
if TYPE_CHECKING:
    from db_models.item import Item

class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = Field(default=True)

    items: list['Item'] = Relationship(back_populates='owner')
