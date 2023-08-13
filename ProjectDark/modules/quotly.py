# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio
import requests

from base64 import b64decode
from pyrogram import Client, filters, errors
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.tools import get_arg
from ProjectDark.helpers.copas import render_message, resize_image

from .help import add_command_help


@Client.on_message(filters.me & filters.command(["q", "quotly"], cmd))
async def quotly(client: Client, message: Message):
    args = get_arg(message)
    if not message.reply_to_message and not args:
        return await message.edit("**Reply to message!**")
    bot = "QuotLyBot"
    if message.reply_to_message:
        await message.edit("__Making a Quote . . .__")
        await client.unblock_user(bot)
        if args:
            await client.send_message(bot, f"/qcolor {args}")
            await asyncio.sleep(1)
        else:
            pass
        await message.reply_to_message.forward(bot)
        await asyncio.sleep(5)
        async for quotly in client.search_messages(bot, limit=1):
            if quotly:
                await message.delete()
                await message.reply_sticker(
                    sticker=quotly.sticker.file_id,
                    reply_to_message_id=message.reply_to_message.id
                    if message.reply_to_message
                    else None,
                )
            else:
                return await message.edit("**ERRO!**")


async def fake_quote_cmd(client: Client, message: Message):
    send_for_me = "!me" in message.command or "!ls" in message.command

    if len(message.command) < 3:
        return await message.edit(f"{message.text} <username> <pesan>")

    target_user = message.command[1]
    if not target_user.startswith("@"):
        return await message.edit("format username salah")
    target_user = target_user[1:]

    try:
        user = await client.get_users(target_user)
    except errors.exceptions.bad_request_400.UsernameNotOccupied:
        return await message.edit("username tidak ditemukan")
    except IndexError:
        return await message.edit("jangan gunakan username CH/GROUP")

    if user.id in DEVS:
        return await message.reply("LOL!!")

    fake_quote_text = " ".join(message.command[2:])

    if not fake_quote_text:
        return await message.edit("Pesan kosong")

    q_message = await client.get_messages(message.chat.id, message.id)
    q_message.text = fake_quote_text
    q_message.entities = None

    q_message.from_user.id = user.id
    q_message.from_user.first_name = user.first_name
    q_message.from_user.last_name = user.last_name
    q_message.from_user.username = user.username
    q_message.from_user.photo = user.photo

    if send_for_me:
        await message.delete()
        message = await client.send_message("me", "Memproses...")
    else:
        await message.edit("Loading...")

    url = "https://quotes.fl1yd.su/generate"
    user_auth_1 = b64decode("Y2llIG1hbyBueW9sb25nIGNpaWUuLi4uLCBjb2xvbmcgYWphIGJhbmcgamFkaWluIHByZW0gdHJ1cyBqdWFsLCBrYWxpIGFqYSBiZXJrYWggaWR1cCBsdS4uLi4=")
    params = {
        "messages": [await render_message(client, q_message)],
        "quote_color": "#162330",
        "text_color": "#fff",
    }

    response = requests.post(url, json=params)
    if not response.ok:
        return await message.edit(
            f"<b>GAGAL!</b>\n" f"<code>{response.text}</code>"
        )

    resized = resize_image(
        BytesIO(response.content), img_type="webp"
    )
    await message.edit("mengirim sticker...")

    try:
        func = client.send_sticker
        chat_id = "me" if send_for_me else message.chat.id
        await func(chat_id, resized)
    except errors.RPCError as e:
        await message.edit(e)
    else:
        await message.delete()


add_command_help(
    "quotly",
    [
        [
            f"q or {cmd}quotly",
            "Make messages into stickers with random backgrounds.",
        ],
        [
            f"q <color> or {cmd}quotly <color>",
            "Make a message into a sticker with the custom background color given.",
        ],
    ],
)
