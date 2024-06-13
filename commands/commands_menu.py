from pyrogram.types import BotCommand


bot_commands = [
    BotCommand(
        command="start",
        description="Register user",
    ),
    BotCommand(
        command="create_task",
        description="Create task",
    ),
    BotCommand(
        command="tasks",
        description="Get list of tasks"
    )
]
