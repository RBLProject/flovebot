# Part of PyroMan - 2022
# Kang by DarkPyro -2023

import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark import BOTLOG_CHATID
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.SQL import no_log_pms_sql
from ProjectDark.helpers.SQL.globals import addgvar, gvarstatus
from ProjectDark.helpers.tools import get_arg

from .help import add_command_help


class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


LOG_CHATS_ = LOG_CHATS()


@Client.on_message(
    filters.private & filters.incoming & ~filters.service & ~filters.me & ~filters.bot
)
async def monito_p_m_s(client: Client, message: Message):
    if BOTLOG_CHATID == -100:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    if not no_log_pms_sql.is_approved(message.chat.id) and message.chat.id != 777000:
        if LOG_CHATS_.RECENT_USER != message.chat.id:
            LOG_CHATS_.RECENT_USER = message.chat.id
            if LOG_CHATS_.NEWPM:
                await LOG_CHATS_.NEWPM.edit(
                    LOG_CHATS_.NEWPM.text.replace(
                        "**#NEW_MESSAGE**",
                        f" • __{LOG_CHATS_.COUNT}__ **Message**",
                    )
                )
                LOG_CHATS_.COUNT = 0
            LOG_CHATS_.NEWPM = await client.send_message(
                BOTLOG_CHATID,
                f"<b>#FORWARDED #NEW_MESSAGE</b>\n<b> • From:</b> {message.from_user.mention}\n<b> • User ID:</b> <code>{message.from_user.id}</code>",
                parse_mode=enums.ParseMode.HTML,
            )
        try:
            async for pmlog in client.search_messages(message.chat.id, limit=1):
                await pmlog.forward(BOTLOG_CHATID)
            LOG_CHATS_.COUNT += 1
        except BaseException:
            pass


@Client.on_message(filters.group & filters.mentioned & filters.incoming)
async def log_tagged_messages(client: Client, message: Message):
    if BOTLOG_CHATID == -100:
        return
    if gvarstatus("GRUPLOG") and gvarstatus("GRUPLOG") == "false":
        return
    if (no_log_pms_sql.is_approved(message.chat.id)) or (BOTLOG_CHATID == -100):
        return
    result = f"<b>#TAGS #MESSAGE</b>\n<b> • From: </b>{message.from_user.mention}"
    result += f"\n<b> • Group: </b>{message.chat.title}"
    result += f"\n • <b><a href = '{message.link}'>Message</a>:</b>\n<code>{message.text}</code>"
    await asyncio.sleep(0.5)
    await client.send_message(
        BOTLOG_CHATID,
        result,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command("log", cmd) & filters.me)
async def set_log_p_m(client: Client, message: Message):
    if BOTLOG_CHATID != -100:
        if no_log_pms_sql.is_approved(message.chat.id):
            no_log_pms_sql.disapprove(message.chat.id)
            await message.edit("**LOG from this group deactivated!**")


@Client.on_message(filters.command("nolog", cmd) & filters.me)
async def set_no_log_p_m(client: Client, message: Message):
    if BOTLOG_CHATID != -100:
        if not no_log_pms_sql.is_approved(message.chat.id):
            no_log_pms_sql.approve(message.chat.id)
            await message.edit("**LOG from this group deactivated!**")


@Client.on_message(filters.command(["pmlog", "pmlogger"], cmd) & filters.me)
async def set_pmlog(client: Client, message: Message):
    if BOTLOG_CHATID == -100:
        return await message.edit(
            "**Set BOTLOG_CHATID VAR**"
        )
    input_str = get_arg(message)
    if input_str == "off":
        h_type = False
    elif input_str == "on":
        h_type = True
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        PMLOG = False
    else:
        PMLOG = True
    if PMLOG:
        if h_type:
            await edit_or_reply(message, "**PM LOG Activated!**")
        else:
            addgvar("PMLOG", h_type)
            await edit_or_reply(message, "**PM LOG Deactivated!**")
    elif h_type:
        addgvar("PMLOG", h_type)
        await edit_or_reply(message, "**PM LOG Activated!**")
    else:
        await edit_or_reply(message, "**PM LOG Deactivated!**")


@Client.on_message(filters.command(["gruplog", "grouplog", "gclog"], cmd) & filters.me)
async def set_gruplog(client: Client, message: Message):
    if BOTLOG_CHATID == -100:
        return await message.edit(
            "**Set BOTLOG_CHATID VAR**"
        )
    input_str = get_arg(message)
    if input_str == "off":
        h_type = False
    elif input_str == "on":
        h_type = True
    if gvarstatus("GRUPLOG") and gvarstatus("GRUPLOG") == "false":
        GRUPLOG = False
    else:
        GRUPLOG = True
    if GRUPLOG:
        if h_type:
            await edit_or_reply(message, "**Group Log Activated!**")
        else:
            addgvar("GRUPLOG", h_type)
            await edit_or_reply(message, "**Group Log Deactivated!**")
    elif h_type:
        addgvar("GRUPLOG", h_type)
        await edit_or_reply(message, "**Group Log Activated!**")
    else:
        await edit_or_reply(message, "**Group Log Deactivated!**")


add_command_help(
    "log",
    [
        [
            "log",
            "Activated Log for current group.",
        ],
        [
            "nolog",
            "Deactivated Log for current group.",
        ],
        [
            "pmlog on/off",
            "Set PM_LOG",
        ],
        [
            "gclog on/off",
            "Set Log mention from group.",
        ],
    ],
)
