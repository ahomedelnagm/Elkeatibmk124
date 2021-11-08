# Daisyxmusic (Telegram bot project )
# Copyright (C) 2021  Inukaasith

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import asyncio

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant

from DaisyXMusic.config import SUDO_USERS
from DaisyXMusic.helpers.decorators import authorized_users_only, errors
from DaisyXMusic.services.callsmusic import client as USER


@Client.on_message(filters.command(["userbotjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b> قم بترقيتي كمسؤول أولاً! </ b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "DaisyMusic"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "🤖: لقد انضممت هنا لتشغيل الموسيقى في الدردشة الصوتية")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b> ✅ userbot انضم بالفعل إلى هذه المجموعة. </ b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b> 🛑 خطأ في انتظار الفيضان 🛑 \n \n تعذر على المستخدم {user.first_name} الانضمام إلى مجموعتك بسبب كثرة طلبات الانضمام إلى userbot."
           +f"\n \ أو إضافة المساعد يدويًا إلى مجموعتك وحاول مرة أخرى </ b>",
        )
        return
    await message.reply_text(
        "<b> ✅ userbot انضم بنجاح إلى هذه المجموعة. </ b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"لا يمكن للمستخدم مغادرة مجموعتك! قد يكون الفيضان."
            "\n\nOr ركلني يدويًا من إلى مجموعتك</b>",
        )
        return


@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left = 0
        failed = 0
        lol = await message.reply("✅ غادر userbot المجموعات بنجاح")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left + 1
                await lol.edit(
                    f"Assistant leaving... Left: {left} chats. Failed: {failed} chats."
                )
            except:
                failed = failed + 1
                await lol.edit(
                    f"Assistant leaving... Left: {left} chats. Failed: {failed} chats."
                )
            await asyncio.sleep(0.7)
        await client.send_message(
            message.chat.id, f"Left {left} chats. Failed {failed} chats."
        )


@Client.on_message(
    filters.command(["userbotjoinchannel", "ubjoinc"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("هل الدردشة مرتبطة حتى؟")
        return
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>قم بترقيتي كمسؤول المجموعة أولاً!</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "DaisyMusic"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "🤖: لقد انضممت هنا كما طلبت")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>المساعد موجود بالفعل في قناتك</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b> 🛑 خطأ في انتظار الفيضان 🛑 \n\n تعذر على المستخدم {user.first_name} الانضمام إلى قناتك بسبب كثرة طلبات الانضمام إلى userbot! تأكد من عدم حظر المستخدم في القناة."
            f"\n\n أو أضف @{ASSISTANT_NAME} يدويًا إلى مجموعتك وحاول مرة أخرى </b>",
        )
        return
    await message.reply_text(
        "<b> انضم userbot المساعد إلى قناتك </b>",
    )
