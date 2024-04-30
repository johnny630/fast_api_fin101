from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING
from db_models.user_stock_link import UserStockLink

if TYPE_CHECKING:
    from db_models.user import User


class Stock(SQLModel, table=True):
    __tablename__ = 'stocks'

    id: int | None = Field(default=None, primary_key=True)
    stock_id: str = Field(index=True, unique=True)
    name: str = Field(index=True, unique=True)

    users: list['User'] = Relationship(back_populates='stocks', link_model=UserStockLink)
