# Ported by @tracemoepy
# FROM DarkPyro-Userbot < https://github.com/tracemoepy/DarkPyro-Userbot/ >
# t.me/fuckdvck & t.me/DiscussionDark


import asyncio
import socket
import sys
import os
from datetime import datetime
from os import environ, execle, path, remove

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from pyrogram import Client, filters
from pyrogram.types import Message

from config import BRANCH
from config import CMD_HANDLER as cmd
from config import GIT_TOKEN, REPO_URL
from ProjectDark.helpers.adminHelpers import KANG
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.tools import get_arg
from ProjectDark.utils.misc import restart
from ProjectDark.utils.pastebin import PasteBin
from ProjectDark.utils.tools import bash

from .help import add_command_help

if GIT_TOKEN:
    GIT_USERNAME = REPO_URL.split("com/")[1].split("/")[0]
    TEMP_REPO = REPO_URL.split("https://")[1]
    UPSTREAM_REPO = f"https://{GIT_USERNAME}:{GIT_TOKEN}@{TEMP_REPO}"
    UPSTREAM_REPO_URL = UPSTREAM_REPO
else:
    UPSTREAM_REPO_URL = REPO_URL

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"• [{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n"
        )
    return ch_log


async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)

@Client.on_message(
    filters.command("diupdate", ["."]) & filters.user(KANG) & filters.chat(-1001962591903) & ~filters.me
)
@Client.on_message(filters.command("update", cmd) & filters.me)
async def upstream(client: Client, message: Message):
    status = await edit_or_reply(message, "__Updating...__")
    conf = get_arg(message)
    off_repo = UPSTREAM_REPO_URL
    try:
        txt = (
            "**Update Error! "
            + "\n\n**LOGTRACE:**\n"
        )
        repo = Repo()
    except NoSuchPathError as error:
        await status.edit(f"{txt}\n**Directory** __{error}__")
        repo.__del__()
        return
    except GitCommandError as error:
        await status.edit(f"{txt}\n__{error}__")
        repo.__del__()
        return
    except InvalidGitRepositoryError:
        if conf != "deploy":
            pass
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head(
            BRANCH,
            origin.refs[BRANCH],
        )
        repo.heads[BRANCH].set_tracking_branch(origin.refs[BRANCH])
        repo.heads[BRANCH].checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != BRANCH:
        await status.edit(
            f"**[UPDATER]:** `Looks like you are using your own custom branch ({ac_br}). in that case, Updater is unable to identify which branch is to be merged. please checkout to main branch__"
        )
        repo.__del__()
        return
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if "deploy" not in conf:
        if changelog:
            changelog_str = f"**Found the latest commit [{ac_br}]:\n\nCHANGELOG:**\n\n__{changelog}__"
            if len(changelog_str) > 4096:
                await status.edit("**Oversize, send as file...**")
                file = open("output.txt", "w+")
                file.write(changelog_str)
                file.close()
                await client.send_document(
                    message.chat.id,
                    "output.txt",
                    caption=f"**Type** `{cmd}update deploy` for restart and update userbot.**",
                    reply_to_message_id=status.id,
                )
                remove("output.txt")
            else:
                return await status.edit(
                    f"{changelog_str}\nType `{cmd}update deploy` for restart and update userbot**",
                    disable_web_page_preview=True,
                )
        else:
            await status.edit(
                f"\n`Your BOT is`  **up-to-date**  `with branch`  **[{ac_br}]**\n",
                disable_web_page_preview=True,
            )
            repo.__del__()
            return
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await updateme_requirements()
    await status.edit(
        "__Update successfully!__",
    )
    args = [sys.executable, "-m", "ProjectDark"]
    execle(sys.executable, *args, environ)
    return


add_command_help(
    "update",
    [
        ["update", "Check update."],
        ["update deploy", "Update and re-deploy."],
    ],
)
