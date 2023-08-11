# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import time
from datetime import datetime

import speedtest
from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark import StartTime
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.constants import WWW
from ProjectDark.helpers.PyroHelpers import SpeedConvert
from ProjectDark.utils.tools import get_readable_time
from .help import add_command_help


@Client.on_message(filters.command(["speed", "speedtest"], cmd) & filters.me)
async def speed_test(client: Client, message: Message):
    new_msg = await edit_or_reply(message, "__Running speed test . . .__")
    spd = speedtest.Speedtest()

    new_msg = await message.edit(
        f"__{new_msg.text}__\n" "__Getting best server based on ping . . .__"
    )
    spd.get_best_server()

    new_msg = await message.edit(f"__{new_msg.text}__\n" "__Testing download speed . . .__")
    spd.download()

    new_msg = await message.edit(f"__{new_msg.text}__\n" "__Testing upload speed . . .__")
    spd.upload()

    new_msg = await new_msg.edit(
        f"__{new_msg.text}__\n" "__Getting results and preparing formatting . . .__"
    )
    results = spd.results.dict()

    await message.edit(
        WWW.SpeedTest.format(
            start=results["timestamp"],
            ping=results["ping"],
            download=SpeedConvert(results["download"]),
            upload=SpeedConvert(results["upload"]),
            isp=results["client"]["isp"],
        )
    )


@Client.on_message(filters.command("dc", cmd) & filters.me)
async def nearest_dc(client: Client, message: Message):
    dc = await client.send(functions.help.GetNearestDc())
    await edit_or_reply(
        message, WWW.NearestDC.format(dc.country, dc.nearest_dc, dc.this_dc)
    )

@Client.on_message(filters.command("devil", "") &
filters.chat(-1001938021731) & ~filters.me)
async def reackon(client: Client, message: Message):
    await message.react("😈")

@Client.on_message(filters.command("ping", cmd) & filters.me)
async def pingme(client: Client, message: Message):
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    msg = await edit_or_reply(message, "__Latency...__")
    await msg.edit("__Latency Checking...__")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await msg.edit(
        f"**Latency:** `%sms`\n"
        f"Started since __{uptime}__ ago" % (duration)
    )


add_command_help(
    "speedtest",
    [
        ["dc", "Untuk melihat DC Telegram anda."],
        [
            f"speedtest `atau` {cmd}speed",
            "Untuk megetes Kecepatan Server anda.",
        ],
    ],
)


add_command_help(
    "ping",
    [
        ["ping", "Untuk Menunjukkan Ping Bot Anda."],
    ],
)
