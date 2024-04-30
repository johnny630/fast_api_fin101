import sys
import os

# console reload
# import importlib
# from db_operations import sqlmodel_learn as l
# importlib.reload(l)

# 考考學習單
# https://sqlmodel.tiangolo.com/
# 將父目錄添加到模塊搜索路徑中
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from sqlmodel import (
    Field, Session, SQLModel, create_engine, select,
    or_
)
from db_models.user import User
from db_models.item import Item
from database import engine

def create_user():
    db = Session(engine)
    user1 = User(email='johnny@test.com', age=10, hashed_password='test', is_active=True)
    user2 = User(email='johnny2@test.com', age=14 , hashed_password='test2', is_active=True)
    user3 = User(email='johnny3@test.com', age=48 , hashed_password='test3', is_active=True)
    user4 = User(email='johnny4@test.com', age=32 , hashed_password='test4', is_active=True)
    user5 = User(email='johnny5@test.com', age=30 , hashed_password='test5', is_active=True)

    db.add(user1)
    db.add(user2)
    db.add(user3)
    db.add(user4)
    db.add(user5)
    db.commit()

def select_users():
    with Session(engine) as db:
        statement = select(User).where(User.email == 'johnny@test.com')
        user = db.exec(statement).first()
        print(user)

        statement = select(User)
        users = db.exec(statement)
        # print(results.all())
        for user in users:
            print(user)

def select_users_by_age():
    with Session(engine) as db:
        statement = select(User).where(User.age >= 30, User.age <= 100)
        results = db.exec(statement)

        print(results.all())

def select_users_where_or():
    with Session(engine) as db:
        statement = select(User).where(or_(User.age <= 40, User.age > 50))
        results = db.exec(statement)
        print(results.all())

def select_user_one():
    with Session(engine) as db:
        # It will raise error
        # sqlalchemy.exc.MultipleResultsFound: Multiple rows were found when exactly one was required
        # result = db.exec(
        #     select(User).where(or_(User.age <= 40, User.age > 50))
        # ).one()

        result = db.exec(
            select(User).where(User.email == 'johnny@test.com')
        ).one()
        print(result)

def get_user_by_id():
    with Session(engine) as db:
        user = db.get(User, 1)
        print(user)

        # No data found, so the value is None
        # Hero: None
        # user = db.get(User, 10)

def select_users_offset_and_limit():
    with Session(engine) as db:
        results = db.exec(
            select(User).where(User.age > 10).offset(2).limit(2)
        )
        print(results.all())

def update_users_1():
    with Session(engine) as db:
        user1 = db.get(User, 1)
        user2 = db.get(User, 2)

        user1.is_active = not user1.is_active
        user2.is_active = not user2.is_active
        user2.age = 15

        db.add_all([user1, user2])
        db.commit()
        db.refresh(user1)
        db.refresh(user2)

        print("user1: ", user1)
        print("user2: ", user2)

def delete_user_1():
    with Session(engine) as db:
        user = User(email='delete@test.com', age=10, hashed_password='test', is_active=True)
        db.add(user)
        db.commit()

        # like ruby find_by
        user = db.exec(
            select(User).where(User.email == 'delete@test.com')
        ).one()
        print("User:", user)

        db.delete(user)
        db.commit()

        print("Deleted user:", user)

        # Can't use refresh
        # db.refresh(user)

        user = db.exec(
            select(User).where(User.email == 'delete@test.com')
        ).first()
        if user is None:
            print("The user has deleted")

def create_users_and_items_1():
    with Session(engine) as db:
        user1 = User(email='one_to_many1@test.com', hashed_password='1234')
        user2 = User(email='one_to_many2@test.com', hashed_password='1234')
        user3 = User(email='one_to_many3@test.com', hashed_password='1234')

        item1 = Item(title='test1', description='test1', owner=user1)
        item2 = Item(title='test2', description='test2', owner=user2)
        item3 = Item(title='test3', description='test3', owner=user2)

        db.add_all([item1, item2, item3, user3])
        db.commit()

        db.refresh(item1)
        db.refresh(item2)
        db.refresh(item3)
        print("Create items:", item1, item2, item3)

def create_users_and_items_2():
    # use `append`
    with Session(engine) as db:
        user = User(email='ont_to_many4@test.com', hashed_password='1234')

        item4 = Item(title='test4', description='test4')
        item5 = Item(title='test5', description='test5')
        user.items.append(item4)
        user.items.append(item5)
        db.add(user)
        db.commit()
        db.refresh(item4)
        db.refresh(item5)
        print(item4, item5)

def get_relationship_object1():
    with Session(engine) as db:
        statement = select(User).where(User.email == 'ont_to_many4@test.com')
        user = db.exec(statement).one()

        print("User's items:", user.items)

        item = user.items[0]
        print("Item's owner:", item.owner)


if __name__ == "__main__":
    create_user()