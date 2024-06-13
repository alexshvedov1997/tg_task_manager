from typing import Dict, List

from pyrogram.types import Message
from sqlalchemy import delete, select, update

from core.exceptions import TaskNotFound, UserNotFound
from core.logger import get_logger
from db.postgres import get_session
from models.tasks import Tasks
from models.users import Users
from services.user import UserService

_logger = get_logger(__name__)


class TaskService:

    async def create_task(self, message: Message, task_name: str, task_description: str) -> None:
        """Create task from tg by user_id"""
        async with get_session() as session:
            user_id = await UserService().get_user_by_chat_id(message.from_user.id, session)
            if not user_id:
                _logger.error("create_task::user doesn't exist {user_name}".format(
                    user_name=message.from_user.username,
                ))
                await message.reply("User doesn't exist. Please register user. You should enter command /start")
                raise UserNotFound
            task = Tasks(
                name=task_name,
                description=task_description,
                is_active=True,
                user_id=user_id,
            )
            session.add(task)
            await session.commit()
            _logger.info(
                "Task with name {task_name} for user_id {user_id} created".format(
                    task_name=task_name,
                    user_id=user_id,
                )
            )

    async def get_list_of_tasks(self, message: Message) -> List[Dict]:
        async with get_session() as session:
            user_id = await UserService().get_user_by_chat_id(message.from_user.id, session)
            if not user_id:
                _logger.error("get_list_of_tasks::user doesn't exist {user_name}".format(
                    user_name=message.from_user.username,
                ))
                await message.reply("User doesn't exist. Please register user. You should enter command /start")
                raise UserNotFound
            messages_data = await session.execute(select(Users, Tasks).join(
                Users, Users.id == Tasks.user_id).where(
                Users.id == user_id,
            ).order_by(Tasks.created_at).limit(10))
            tasks = messages_data.fetchall()
            tasks_data = []
            for user_task in tasks:
                user, task = user_task
                tasks_data.append(
                    {
                        "task_name": task.name,
                        "is_active": task.is_active,
                        "task_id": task.id,
                    }
                )
            return tasks_data

    async def get_task_info(self, id_task: int):
        """Get task data from db"""
        async with get_session() as session:
            statement = select(Tasks).where(Tasks.id == id_task)
            task_id = await session.execute(statement=statement)
            task_id = task_id.scalar_one_or_none()
            if not task_id:
                raise TaskNotFound
            return {
                "task_name": task_id.name,
                "task_id": task_id.id,
                "created_at": task_id.created_at,
                "state": task_id.is_active,
                "description": task_id.description,
            }

    async def delete_task(self, id_task: int):
        """Delete task from keyboard"""
        async with get_session() as session:
            statement = delete(Tasks).where(Tasks.id == id_task)
            await session.execute(statement=statement)
            await session.commit()
            _logger.info(
                "Task with {task_id} deleted".format(
                    task_id=id_task,
                )
            )

    async def set_done(self, id_task):
        """Set state done to task from keyboard"""
        async with get_session() as session:
            await session.execute(
                update(Tasks).where(Tasks.id == id_task).values(is_active=False)
            )
            await session.commit()
            _logger.info(
                "Task with {task_id} set done".format(
                    task_id=id_task,
                )
            )

    async def cursor_list_of_task(self, client, task_id, is_next=True) -> List[Dict]:
        """Pagination for list of tasks"""
        async with get_session() as session:
            user_id = await UserService().get_user_by_chat_id(client.from_user.id, session)
            if not user_id:
                _logger.error("cursor_list_of_task::user doesn't exist {user_name}".format(
                    user_name=client.from_user.username,
                ))
                await client.reply("User doesn't exist. Please register user. You should enter command /start")
                raise UserNotFound
            statement = select(Users, Tasks).join(
                Users, Users.id == Tasks.user_id).where(
                Users.id == user_id,
            ).order_by(Tasks.created_at)
            if is_next:
                messages_data = await session.execute(statement.where(Tasks.id > task_id).limit(10))
            else:
                messages_data = await session.execute(statement.where(Tasks.id < task_id).limit(10))
            tasks = messages_data.fetchall()
            if not tasks and is_next:
                messages_data = await session.execute(statement.where(Tasks.id <= task_id).limit(10))
                tasks = messages_data.fetchall()
            elif not tasks:
                messages_data = await session.execute(statement.where(Tasks.id >= task_id).limit(10))
                tasks = messages_data.fetchall()
            tasks_data = []
            for user_task in tasks:
                user, task = user_task
                tasks_data.append(
                    {
                        "task_name": task.name,
                        "is_active": task.is_active,
                        "task_id": task.id,
                    }
                )
            return tasks_data
