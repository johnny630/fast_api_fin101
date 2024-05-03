import logging
from rich.logging import RichHandler
from sqlalchemy import create_engine
from sqlmodel import create_engine, SQLModel, Session

from fastapi import Depends
from typing import Annotated


sqlite_file_name = "fast_api_fin101.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# 设置日志记录器
logger = logging.getLogger("sqlalchemy.engine")
logger.setLevel(logging.INFO)
logger.addHandler(RichHandler())

connect_args = {"check_same_thread": False}
# 创建数据库引擎并启用 echo  logging_name 搭配rich
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args, logging_name="sqlalchemy.engine")

# We want to use alembic, din't use it to create table
# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

sessionDep = Annotated[Session, Depends(get_session)]
