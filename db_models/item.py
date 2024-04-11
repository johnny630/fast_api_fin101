from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING, Optional

# https://sqlmodel.tiangolo.com/tutorial/code-structure/#make-circular-imports-work
if TYPE_CHECKING:
    from db_models.user import User

class Item(SQLModel, table=True):
    __tablename__ = 'items'

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(index=True)
    owner_id: int | None = Field(default=None, foreign_key='users.id', nullable=False)

    # Here need to use `Optional['User']` , `'User'`` is not work
    # https://sqlmodel.tiangolo.com/tutorial/code-structure/#make-circular-imports-work
    owner: Optional['User'] = Relationship(back_populates="items")
