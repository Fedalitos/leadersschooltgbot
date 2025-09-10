from aiogram import Router, types
from data.db import add_group, remove_group

router = Router()

@router.my_chat_member()
async def track_group(event: types.ChatMemberUpdated):
    chat = event.chat
    new_status = event.new_chat_member.status

    if new_status in ["administrator", "member"]:
        add_group(chat.id, chat.title or "Без названия")
    elif new_status in ["left", "kicked"]:
        remove_group(chat.id)
