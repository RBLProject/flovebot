# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply

from .help import add_command_help


@Client.on_message(filters.command("join", cmd) & filters.me)
async def join(client: Client, message: Message):
    Dark = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await edit_or_reply(message, "__Joining to chat...__")
    try:
        await xxnx.edit(f"**Successfully joined to Chat ID** __{Dark}__")
        await client.join_chat(Dark)
    except Exception as ex:
        await xxnx.edit(f"**ERROR:** \n\n{str(ex)}")


@Client.on_message(filters.command(["leave", "kickme"], cmd) & filters.me)
async def leave(client: Client, message: Message):
    Dark = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await edit_or_reply(message, "__Good bye dumb ass...__")
    try:
        await xxnx.edit_text(f"{client.me.first_name} has left this group, bye!!")
        await client.leave_chat(Dark)
    except Exception as ex:
        await xxnx.edit_text(f"**ERROR:** \n\n{str(ex)}")


@Client.on_message(filters.command(["leaveallgc"], cmd) & filters.me)
async def kickmeall(client: Client, message: Message):
    Dark = await edit_or_reply(message, "__Leaving all group chat...__")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Dark.edit(
        f"**Successfully leave from {done} Group, Failed leave from {er} Group**"
    )


@Client.on_message(filters.command(["leaveallch"], cmd) & filters.me)
async def kickmeallch(client: Client, message: Message):
    Dark = await edit_or_reply(message, "__Leaving from all channels...__")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.CHANNEL):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Dark.edit(
        f"**Successfully leave from {done} Channel, Failed leave from {er} Channel**"
    )


add_command_help(
    "joinleave",
    [
        ["kickme",
        "Leave the group with a message has left this group, bye!!.",
        ],
        
        ["leaveallgc",
        "Leave all telegram groups you have joined."
        ],
        
        ["leaveallch",
        "Leave all telegram channels you have joined."
        ],
        
        ["join <UsernameGC>",
        "To joined group chat with the username."
        ],
        
        ["leave <UsernameGC>",
        "To leaving group chat with the username."
        ],
    ],
)
