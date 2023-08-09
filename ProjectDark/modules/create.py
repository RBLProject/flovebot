# null
# Copyright (C) 2022 Pyro-ManUserbot
# Re-Code by DarkTeam - 2023
# This file is a part of < https://github.com/tracemoepy/DarkPyro-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/tracemoepy/DarkPyro-Userbot/blob/main/LICENSE/>.
# t.me/DiscussionDark & t.me/fuckdvck

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply

from .help import add_command_help


@Client.on_message(filters.command("create", cmd) & filters.me)
async def create(client: Client, message: Message):
    if len(message.command) < 3:
        return await edit_or_reply(
            message, f"__Type __{cmd}help create` for more__"
        )
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    Dark = await edit_or_reply(message, "__Processing...__")
    desc = "Welcome to my" + ("group" if group_type == "gc" else "channel")
    if group_type == "gc":  # for supergroup
        _id = await client.create_supergroup(group_name, desc)
        link = await client.get_chat(_id["id"])
        await Dark.edit(
            f"__Successfully create group: [{group_name}]({link['invite_link']})__",
            disable_web_page_preview=True,
        )
    elif group_type == "ch":  # for channel
        _id = await client.create_channel(group_name, desc)
        link = await client.get_chat(_id["id"])
        await Dark.edit(
            f"__Successfully create channel: [{group_name}]({link['invite_link']})__",
            disable_web_page_preview=True,
        )


add_command_help(
    "create",
    [
        ["create ch", "to create channel"],
        ["create gc", "to create group"],
    ],
)
