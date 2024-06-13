from core.settings import settings
from pyrogram import Client, filters, idle
from core import app

from commands.commands import start_command, create_task, get_list_of_task
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from commands.commands_menu import bot_commands
from utils.controller import KeyboardController


if __name__ == "__main__":
    app.app = Client(
        settings.BOT_NAME,
        bot_token=settings.BOT_TOKEN,
        api_hash=settings.API_HASH,
        api_id=settings.API_ID,
    )
    app.app.add_handler(MessageHandler(start_command, filters.command(commands="start")))
    app.app.add_handler(MessageHandler(create_task, filters.command(commands="create_task")))
    app.app.add_handler(MessageHandler(get_list_of_task, filters.command(commands="tasks")))
    app.app.add_handler(CallbackQueryHandler(KeyboardController().callback_handler))
    app.app.start()
    app.app.set_bot_commands(bot_commands)
    idle()
    app.stop()
