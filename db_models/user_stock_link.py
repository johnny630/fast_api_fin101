from sqlmodel import SQLModel, Field

class UserStockLink(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key='users.id', primary_key=True)
    stock_id: int | None = Field(default=None, foreign_key='stocks.id', primary_key=True)