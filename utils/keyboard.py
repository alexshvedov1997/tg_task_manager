from typing import Dict, List

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def tasks_inline_keyboard(tasks: List[Dict]) -> InlineKeyboardMarkup:
    """Keyboard for pagination to tasks and posobility to chose some task"""
    reply_keyboard = []
    for task in tasks:
        reply_keyboard.append(
            [
                InlineKeyboardButton(
                    text="Name: {task_name}| \nState:{state}".format(
                        task_name=task.get("task_name"),
                        state="Active" if task.get("is_active") else "Done"
                    ),
                    callback_data="get_task_info|{task_id}".format(
                        task_id=task.get("task_id"),
                    )
                )
            ]
        )
    reply_keyboard.append([
        InlineKeyboardButton(
            "<-",
            callback_data="prev_page|{task_id}".format(
                task_id=tasks[0].get("task_id") if tasks else -1,
            )
        ),
        InlineKeyboardButton(
            "->",
            callback_data="next_page|{task_id}".format(
                task_id=tasks[-1].get("task_id") if tasks else -1
            ),
        ),
    ])
    return InlineKeyboardMarkup(inline_keyboard=reply_keyboard)


def task_action_keyboard(task_id: int) -> InlineKeyboardMarkup:
    """"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Delete Task", callback_data="delete_task|{task_id}".format(task_id=task_id)),
                InlineKeyboardButton("Set Done", callback_data="set_done|{task_id}".format(task_id=task_id)),
            ]
        ]
    )
