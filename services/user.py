from typing import Optional

from pyrogram.types import Message
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import UserAlreadyExist
from core.logger import get_logger
from db.postgres import get_session
from models.users import Users

_logger = get_logger(__name__)


class UserService:

    async def create_user(self, login: str, login_message: Message) -> None:
        """Create user if he does not exist in the db"""
        async with get_session() as session:
            is_user_exist = await self.check_user(login_message.from_user.id, session)
            if is_user_exist:
                _logger.error("create_user::user already exist {user_name}".format(
                    user_name=login_message.from_user.username,
                ))
                await login_message.reply("User already exist.")
                raise UserAlreadyExist
            user = Users(
                login=login,
                chat_id=login_message.from_user.id,
                first_name=login_message.from_user.first_name,
                last_name=login_message.from_user.last_name,
                tg_username=login_message.from_user.username,
            )
            session.add(user)
            await session.commit()
            _logger.info("User created {login}".format(login=login))

    async def check_user(self, chat_id: int, session: AsyncSession) -> bool:
        """Check user by chat_id exist user or not"""
        statement = select(exists(Users).where(Users.chat_id == chat_id))
        is_user_exist = await session.execute(statement=statement)
        is_user_exist = is_user_exist.scalar_one_or_none()
        return is_user_exist

    async def get_user_by_chat_id(self, chat_id: int, session: AsyncSession) -> Optional[int]:
        """Get user by tg chat_id"""
        statement = select(Users.id).where(Users.chat_id == chat_id)
        user_id = await session.execute(statement=statement)
        user_id = user_id.scalar_one_or_none()
        if user_id:
            return user_id
