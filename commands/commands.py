from pyrogram import Client
from pyrogram.types import Message
from pyromod import listen
from services.user import UserService
from services.task import TaskService
from utils.keyboard import tasks_inline_keyboard


async def start_command(client: Client, message: Message) -> None:
    """Command /start - create user from tg"""
    await message.reply("Please enter your login")
    response = await client.listen(chat_id=message.chat.id)
    login = response.text
    await UserService().create_user(login, message)
    await message.reply(f"User with login {login} created!")


async def create_task(client: Client, message: Message) -> None:
    """Command /create_task - create task from tg"""
    await message.reply("Enter task name:")
    task_name = await client.listen(chat_id=message.chat.id)
    await message.reply("Entry task description:")
    task_description = await client.listen(chat_id=message.chat.id)
    await TaskService().create_task(message, task_name.text, task_description.text)


async def get_list_of_task(client: Client, message: Message) -> None:
    """Command /tasks - get list of task from tg"""
    tasks = await TaskService().get_list_of_tasks(message)
    keyboards = tasks_inline_keyboard(tasks)
    await message.reply(text="List Tasks", reply_markup=keyboards)
