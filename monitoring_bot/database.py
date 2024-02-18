from typing import Type

from sqlalchemy import Column, String, BigInteger, DateTime, select, Sequence, Boolean
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import ENUM

from monitoring_bot.constants import log, connection_url

Base = declarative_base()


class User(Base):
    """
    Representation of subscriber

    Subscriber can be:
    * member of a channel/chat
    * banned as bot (did not approve itself)
    * left as leave channel/chat in the past

    if it has `left` status: bot won't give a membership to it and noticed admin about this incident
    """
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True)
    username = Column(String)
    enter_date = Column(DateTime)
    leave_date = Column(DateTime)
    status = Column(ENUM('member', 'banned', 'left', 'admin', 'not_a_member', name='status'))
    has_chat_with_bot = Column(Boolean, default=False)


class Database:
    async_engine = create_async_engine(connection_url)
    AsyncSession = async_sessionmaker(bind=async_engine)

    @classmethod
    async def insert_into_users(cls, **user_data) -> bool:
        async with cls.AsyncSession() as session:
            new_user = User(**user_data)
            if new_user:
                try:
                    session.add(new_user)
                    await session.commit()
                except IntegrityError:
                    log.error(f'User with id {new_user.user_id} already exists in database')
                    await session.rollback()
                    return False
                else:
                    log.success(f"User successfully inserted: {user_data}")
                    return True
            else:
                log.exception(f"Some error occurred when creating user: {user_data}")
                return False

    @classmethod
    async def select_from_users(cls,
                                user_id: int = None,
                                where: dict[str, str | int] = None
                                ) -> Sequence[User] | Type[User]:
        if user_id and where:
            raise ValueError("Please provide only one argument")
        async with cls.AsyncSession() as session:
            if user_id:
                result = await session.get(User, user_id)
                return result
            elif where:
                statement = select(User).filter(
                    *[getattr(User, attribute) == value for attribute, value in where.items()]
                )
                result = await session.execute(statement)
                return result.scalars().all()
            else:
                statement = select(User)
                result = await session.execute(statement)
                return result.scalars().all()

    @classmethod
    async def update_user(cls, user_id: int, **data) -> bool:
        async with cls.AsyncSession() as session:
            async with session.begin():
                user = await session.get(User, user_id)
                if user:
                    for column_name, column_value in data.items():
                        setattr(user, column_name, column_value)
                    log.info(f"User @{user.username} update it data to {data}")
                    return True
                else:
                    log.exception(f"Can not update user because there is no user with id {user_id}")
                    return False

    @classmethod
    async def delete_user(cls, user_id: int) -> bool:
        async with cls.AsyncSession() as session:
            async with session.begin():
                existing_user = await session.get(User, user_id)
                if existing_user:
                    await session.delete(existing_user)
                    log.info(f"User @{existing_user.username} successfully deleted from database")
                    return True
                log.exception(f"Can not delete user because there is no user with id {user_id}")
                return False
