from pyrogram import Client
from pyrogram.types import CallbackQuery

from core.logger import get_logger
from services.task import TaskService
from utils.keyboard import task_action_keyboard, tasks_inline_keyboard

_logger = get_logger(__name__)

class KeyboardController:

    async def callback_handler(self, client, callback_query):
        method_name, task_id = callback_query.data.split("|")
        method = getattr(self, method_name)
        await method(client, callback_query, int(task_id))

    async def get_task_info(self, client: Client, callback_query: CallbackQuery, task_id: int):
        task_info = await TaskService().get_task_info(task_id)
        await callback_query.message.reply(
            """
            Name: {task_name}\nDescription: {description}\nState: {state}\nCreated_at: {created_at}
            """.format(
                task_name=task_info.get("task_name"),
                description=task_info.get("description"),
                created_at=task_info.get("created_at").strftime("%Y %d %B %H:%M"),
                state="Active" if task_info.get("state") else "Done"
            ),
            reply_markup=task_action_keyboard(task_id),
        )

    async def delete_task(self, client: Client, callback_query: CallbackQuery, task_id: int):
        await TaskService().delete_task(task_id)
        await callback_query.message.reply("Task is deleted")

    async def set_done(self, client: Client, callback_query: CallbackQuery, task_id: int):
        await TaskService().set_done(task_id)
        await callback_query.message.reply("Task is done")

    async def prev_page(self, client: Client, callback_query: CallbackQuery, task_id: int):
        tasks = await TaskService().cursor_list_of_task(callback_query, task_id)
        keyboards = tasks_inline_keyboard(tasks)
        await callback_query.message.reply(text="List Tasks", reply_markup=keyboards)

    async def next_page(self, client: Client, callback_query: CallbackQuery, task_id: int):
        tasks = await TaskService().cursor_list_of_task(callback_query, task_id, True)
        keyboards = tasks_inline_keyboard(tasks)
        await callback_query.message.reply(text="List Tasks", reply_markup=keyboards)
