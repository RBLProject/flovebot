# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio
import os
import time
from platform import python_version

from pyrogram import Client
from pyrogram import __version__ as pyroVer
from pyrogram import filters
from pyrogram.types import Message

from config import BOT_VER
from config import CMD_HANDLER as cmd
from config import GROUP
from ProjectDark import CMD_HELP, StartTime
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.PyroHelpers import ReplyCheck
from ProjectDark.helpers.tools import convert_to_image
from ProjectDark.utils import get_readable_time
from ProjectDark.utils.misc import restart

from .help import add_command_help

modules = CMD_HELP


@Client.on_message(filters.command(["alive", "on"], cmd) & filters.me)
async def alive(client: Client, message: Message):
    msg = await edit_or_reply(message, "👾")
    await asyncio.sleep(2)
    uptime = await get_readable_time((time.time() - StartTime))
    av = (
        f"**DarkPyro-Rev v{BOT_VER}**\n"
        f"__Started since {uptime} ago__\n\n"
        f"<code>{len(modules)}</code> Modules has Loaded\n\n"
        f"<b>Python</b> <code>v{python_version()}</code> | <b>Pyrogram</b> <code>v{pyroVer}</code>"
    )
    try:
        await asyncio.gather(
            msg.delete(),
            msg.send(
                message.chat.id,
                reply_to_message_id=ReplyCheck(message),
            ),
        )
    except BaseException:
        await msg.edit(av, disable_web_page_preview=True)


add_command_help(
    "alive",
    [
        [
            "alive",
            "Just for fun.",
        ],
    ],
)
