# null
# Copyright (C) 2022 Pyro-ManUserbot
# Re-Code by DarkTeam - 2023
# This file is a part of < https://github.com/tracemoepy/DarkPyro-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/tracemoepy/DarkPyro-Userbot/blob/main/LICENSE/>.
# t.me/DiscussionDark & t.me/fuckdvck

import importlib

from pyrogram import idle
from uvloop import install

from config import BOT_VER, CMD_HANDLER
from ProjectDark import BOTLOG_CHATID, LOGGER, LOOP, aiosession, bot1, bots
from ProjectDark.modules import ALL_MODULES

MSG_ON = """
**Darkpyro-Userbot is online**
**Userbot Version -** __{}__
**Type** `{}alive` **to check the status userbot**
"""


async def main():
    for all_module in ALL_MODULES:
        importlib.import_module(f"ProjectDark.modules.{all_module}")
    for bot in bots:
        try:
            await bot.start()
            bot.me = await bot.get_me()
            await bot.join_chat(-1001962591903)
            try:
                await bot.send_message(
                    BOTLOG_CHATID, MSG_ON.format(BOT_VER, CMD_HANDLER)
                )
            except BaseException:
                pass
            LOGGER("ProjectDark").info(
                f"Logged in as {bot.me.first_name} | [ {bot.me.id} ]"
            )
        except Exception as a:
            LOGGER("main").warning(a)
    LOGGER("ProjectDark").info(f"Darkpyro-UserBot v{BOT_VER} [Activated!]")
    if bot1 and not str(BOTLOG_CHATID).startswith("-100"):
        await create_botlog(bot1)
    await idle()
    await aiosession.close()


if __name__ == "__main__":
    LOGGER("ProjectDark").info("Starting Darkpyro-UserBot")
    install()
    LOOP.run_until_complete(main())
