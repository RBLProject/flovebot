# Part of PyroMan - 2022
# Kang by DarkPyro - 2023


from pyrogram import Client, enums, filters
from pyrogram.types import Message
from sqlalchemy.exc import IntegrityError

from config import CMD_HANDLER as cmd
from ProjectDark import TEMP_SETTINGS
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.SQL.globals import addgvar, gvarstatus
from ProjectDark.helpers.tools import get_arg

from .help import add_command_help

DEF_UNAPPROVED_MSG = (
"__This message is sent automatically by the session to prevent unknown users from spamming. Your message will be replied to immediately if the account owner is online and as long as it don't spam__"
)

@Client.on_message(
    ~filters.me & filters.private & ~filters.bot & filters.incoming, group=69
)
async def incomingpm(client: Client, message: Message):
    try:
        from ProjectDark.helpers.SQL.globals import gvarstatus
        from ProjectDark.helpers.SQL.pm_permit_sql import is_approved
    except BaseException:
        pass

    if gvarstatus("PMPERMIT") and gvarstatus("PMPERMIT") == "false":
        return
    if await auto_accept(client, message) or message.from_user.is_self:
        message.continue_propagation()
    if message.chat.id != 777000:
        PM_LIMIT = gvarstatus("PM_LIMIT") or 5
        getmsg = gvarstatus("unapproved_msg")
        if getmsg is not None:
            UNAPPROVED_MSG = getmsg
        else:
            UNAPPROVED_MSG = DEF_UNAPPROVED_MSG

        apprv = is_approved(message.chat.id)
        if not apprv and message.text != UNAPPROVED_MSG:
            if message.chat.id in TEMP_SETTINGS["PM_LAST_MSG"]:
                prevmsg = TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                if message.text != prevmsg:
                    async for message in client.search_messages(
                        message.chat.id,
                        from_user="me",
                        limit=10,
                        query=UNAPPROVED_MSG,
                    ):
                        await message.delete()
                    if TEMP_SETTINGS["PM_COUNT"][message.chat.id] < (int(PM_LIMIT) - 1):
                        ret = await message.reply_text(UNAPPROVED_MSG)
                        TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id] = ret.text
            else:
                ret = await message.reply_text(UNAPPROVED_MSG)
                if ret.text:
                    TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id] = ret.text
            if message.chat.id not in TEMP_SETTINGS["PM_COUNT"]:
                TEMP_SETTINGS["PM_COUNT"][message.chat.id] = 1
            else:
                TEMP_SETTINGS["PM_COUNT"][message.chat.id] = (
                    TEMP_SETTINGS["PM_COUNT"][message.chat.id] + 1
                )
            if TEMP_SETTINGS["PM_COUNT"][message.chat.id] > (int(PM_LIMIT) - 1):
                await message.reply("You has been blocked!")
                try:
                    del TEMP_SETTINGS["PM_COUNT"][message.chat.id]
                    del TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                except BaseException:
                    pass

                await client.block_user(message.chat.id)

    message.continue_propagation()


async def auto_accept(client, message):
    try:
        from ProjectDark.helpers.SQL.pm_permit_sql import approve, is_approved
    except BaseException:
        pass

    if message.chat.id not in [client.me.id, 777000]:
        if is_approved(message.chat.id):
            return True

        async for msg in client.get_chat_history(message.chat.id, limit=1):
            if msg.from_user.id == client.me.id:
                try:
                    del TEMP_SETTINGS["PM_COUNT"][message.chat.id]
                    del TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                except BaseException:
                    pass

                try:
                    approve(chat.id)
                    async for message in client.search_messages(
                        message.chat.id,
                        from_user="me",
                        limit=10,
                        query=UNAPPROVED_MSG,
                    ):
                        await message.delete()
                    return True
                except BaseException:
                    pass

    return False


@Client.on_message(
    filters.command(["ok", "setuju", "approve"], cmd) & filters.me & filters.private
)
async def approvepm(client: Client, message: Message):
    try:
        from ProjectDark.helpers.SQL.pm_permit_sql import approve
    except BaseException:
        await message.edit("Running on Non-SQL mode!")
        return

    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            await message.edit("Are you stupid?")
            return
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id
    else:
        aname = message.chat
        if not aname.type == enums.ChatType.PRIVATE:
            await message.edit("Are you stupid?")
            return
        name0 = aname.first_name
        uid = aname.id

    try:
        approve(uid)
        await message.edit(f"[{name0}](tg://user?id={uid}) Approved!")
    except IntegrityError:
        await message.edit(
            f"[{name0}](tg://user?id={uid}) already approved."
        )
        return


@Client.on_message(
    filters.command(["tolak", "nopm", "disapprove"], cmd) & filters.me & filters.private
)
async def disapprovepm(client: Client, message: Message):
    try:
        from ProjectDark.helpers.SQL.pm_permit_sql import dissprove
    except BaseException:
        await message.edit("Running on Non-SQL mode!")
        return

    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            await message.edit("Are you stupid?")
            return
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id
    else:
        aname = message.chat
        if not aname.type == enums.ChatType.PRIVATE:
            await message.edit("Are you stupid?")
            return
        name0 = aname.first_name
        uid = aname.id

    dissprove(uid)

    await message.edit(
        f"[{name0}](tg://user?id={uid}) declined! Spam detected."
    )


@Client.on_message(filters.command("pmlimit", cmd) & filters.me)
async def setpm_limit(client: Client, cust_msg: Message):
    if gvarstatus("PMPERMIT") and gvarstatus("PMPERMIT") == "false":
        return await cust_msg.edit(
            f"**You Must Set Var** `PM_AUTO_BAN` **To** `True`\n\n**If you want to activate PMPERMIT, please type:** __{cmd}setvar PM_AUTO_BAN True__"
        )
    try:
        from ProjectDark.helpers.SQL.globals import addgvar
    except AttributeError:
        await cust_msg.edit("**Running on Non-SQL mode!**")
        return
    input_str = (
        cust_msg.text.split(None, 1)[1]
        if len(
            cust_msg.command,
        )
        != 1
        else None
    )
    if not input_str:
        return await cust_msg.edit("**Please enter a number for PM_LIMIT.**")
    Dark = await cust_msg.edit("__Processing...__")
    if input_str and not input_str.isnumeric():
        return await Dark.edit("**Please enter a number for PM_LIMIT.**")
    addgvar("PM_LIMIT", input_str)
    await Dark.edit(f"**Set PM limit to** __{input_str}__")


@Client.on_message(filters.command(["pmpermit", "pmguard"], cmd) & filters.me)
async def onoff_pmpermit(client: Client, message: Message):
    input_str = get_arg(message)
    if input_str == "off":
        h_type = False
    elif input_str == "on":
        h_type = True
    if gvarstatus("PMPERMIT") and gvarstatus("PMPERMIT") == "false":
        PMPERMIT = False
    else:
        PMPERMIT = True
    if PMPERMIT:
        if h_type:
            await edit_or_reply(message, "**PMPERMIT Successfully activated**")
        else:
            addgvar("PMPERMIT", h_type)
            await edit_or_reply(message, "**PMPERMIT Successfully deactivated **")
    elif h_type:
        addgvar("PMPERMIT", h_type)
        await edit_or_reply(message, "**PMPERMIT Successfully activated**")
    else:
        await edit_or_reply(message, "**PMPERMIT Successfully deactivated**")


@Client.on_message(filters.command("setpmpermit", cmd) & filters.me)
async def setpmpermit(client: Client, cust_msg: Message):
    """Set your own Unapproved message"""
    if gvarstatus("PMPERMIT") and gvarstatus("PMPERMIT") == "false":
        return await cust_msg.edit(
            "**You Must Set Var** `PM_AUTO_BAN` **To** `True`\n\n**If you want to activate PMPERMIT, please type:** `.setvar PM_AUTO_BAN True__"
        )
    try:
        import ProjectDark.helpers.SQL.globals as sql
    except AttributeError:
        await cust_msg.edit("**Running on Non-SQL mode!**")
        return
    Dark = await cust_msg.edit("__Processing...__")
    custom_message = sql.gvarstatus("unapproved_msg")
    message = cust_msg.reply_to_message
    if custom_message is not None:
        sql.delgvar("unapproved_msg")
    if not message:
        return await Dark.edit("**Please Reply To Message**")
    msg = message.text
    sql.addgvar("unapproved_msg", msg)
    await Dark.edit("**Message Saved Successfully To Room Chat**")


@Client.on_message(filters.command("getpmpermit", cmd) & filters.me)
async def get_pmermit(client: Client, cust_msg: Message):
    if gvarstatus("PMPERMIT") and gvarstatus("PMPERMIT") == "false":
        return await cust_msg.edit(
            "**You Must Set Var** `PM_AUTO_BAN` **To** `True`\n\n**If you want to activate PMPERMIT, please type:** `.setvar PM_AUTO_BAN True__"
        )
    try:
        import ProjectDark.helpers.SQL.globals as sql
    except AttributeError:
        await cust_msg.edit("**Running on Non-SQL mode!**")
        return
    Dark = await cust_msg.edit("__Processing...__")
    custom_message = sql.gvarstatus("unapproved_msg")
    if custom_message is not None:
        await Dark.edit("**Your PMPERMIT message now:**" f"\n\n{custom_message}")
    else:
        await Dark.edit(
            "**You Have Not Set PMPERMIT Costume Messages,**\n"
            f"**Still Using Default PM Messages:**\n\n{DEF_UNAPPROVED_MSG}"
        )


@Client.on_message(filters.command("resetpmpermit", cmd) & filters.me)
async def reset_pmpermit(client: Client, cust_msg: Message):
    if gvarstatus("PMPERMIT") and gvarstatus("PMPERMIT") == "false":
        return await cust_msg.edit(
            f"**You Must Set Var** `PM_AUTO_BAN` **To** `True`\n\n**If you want to activate PMPERMIT, please type:** __{cmd}setvar PM_AUTO_BAN True__"
        )
    try:
        import ProjectDark.helpers.SQL.globals as sql
    except AttributeError:
        await cust_msg.edit("**Running on Non-SQL mode!**")
        return
    Dark = await cust_msg.edit("__Processing...__")
    custom_message = sql.gvarstatus("unapproved_msg")

    if custom_message is None:
        await Dark.edit("**Your PMPERMIT message is back to Default**")
    else:
        sql.delgvar("unapproved_msg")
        await Dark.edit("**Successfully Changed PMPERMIT Custom Message to Default**")


add_command_help(
    "pmpermit",
    [
        [f"ok or {cmd}approve",
        "Receive someone's message by replying to the message or tagging and also to do it in pm",
        ],
        
        [f"tolak or {cmd}nopm",
        "Reject someone's message by replying to the message or tagging and also to do it in pm",
        ],
        
        ["pmlimit <number>",
        "To customize messages, limit auto block messages",
        ],
        
        ["setpmpermit <reply to chat>",
        "To customize the PMPERMIT message for people whose messages have not been received.",
        ],
        
        ["getpmpermit",
        "To view PMPERMIT messages.",
        ],
        
        ["resetpmpermit",
        "To Reset PMPERMIT Messages to DEFAULT",
        ],
        
        ["pmpermit on/off",
        "To activated and deactivated PMPERMIT",
        ],
    ],
)
