# null
# Copyright (C) 2022 Pyro-ManUserbot
# Re-Code by DarkTeam - 2023
# This file is a part of < https://github.com/tracemoepy/DarkPyro-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/tracemoepy/DarkPyro-Userbot/blob/main/LICENSE/>.
# t.me/DiscussionDark & t.me/fuckdvck

import asyncio

from pyrogram import Client, filters
from pyrogram.enums import ChatType, UserStatus
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark import BOTLOG_CHATID
from ProjectDark.helpers.basic import edit_or_reply

from .help import *


@Client.on_message(filters.me & filters.command("invite", cmd))
async def inviteee(client: Client, message: Message):
    mg = await edit_or_reply(message, "__Adding Users!__")
    user_s_to_add = message.text.split(" ", 1)[1]
    if not user_s_to_add:
        await mg.edit("__Give Me Users To Add! Check Help Menu For More Info!__")
        return
    user_list = user_s_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except BaseException as e:
        await mg.edit(f"__Unable To Add Users! \nTraceBack : {e}__")
        return
    await mg.edit(f"__Sucessfully Added {len(user_list)} To This Group / Channel!__")


@Client.on_message(filters.command(["inviteall"], cmd) & filters.me)
async def inv(client: Client, message: Message):
    Dark = await edit_or_reply(message, "__Processing . . .__")
    text = message.text.split(" ", 1)
    queryy = text[1]
    chat = await client.get_chat(queryy)
    tgchat = message.chat
    await Dark.edit_text(f"inviting users from {chat.username}")
    async for member in client.get_chat_members(chat.id):
        user = member.user
        zxb = [
            UserStatus.ONLINE,
            UserStatus.OFFLINE,
            UserStatus.RECENTLY,
            UserStatus.LAST_WEEK,
        ]
        if user.status in zxb:
            try:
                await client.add_chat_members(tgchat.id, user.id)
            except Exception as e:
                mg = await client.send_message(BOTLOG_CHATID, f"**ERROR:** __{e}__")
                await asyncio.sleep(0.3)
                await mg.delete()


@Client.on_message(filters.command("invitelink", cmd) & filters.me)
async def invite_link(client: Client, message: Message):
    Dark = await edit_or_reply(message, "__Processing...__")
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        message.chat.title
        try:
            link = await client.export_chat_invite_link(message.chat.id)
            await Dark.edit(f"**Link Invite:** {link}")
        except Exception:
            await Dark.edit("Denied permission")


add_command_help(
    "invite",
    [
        ["invitelink",
        "Get invite link",
        ],
        
        ["invite @username",
        "Invite a user"
        ],
        
        ["inviteall @usernamegc",
        "Invite all-member from destination group [BE CAREFULL FOR THIS COMMAND! (Not Recommended)",
        ],
    ],
)
