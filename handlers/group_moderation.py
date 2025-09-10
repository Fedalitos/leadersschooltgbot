# ============================================
# 🔹 handlers/group_moderation.py — группа модерация функциялари
# ============================================

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ChatPermissions
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta
import sqlite3
import re

router = Router()

# База данных для заметок и мутов
NOTES_DB = "group_data.db"

def init_group_db():
    """Группа маълумотлар базасини ишга тушириш"""
    conn = sqlite3.connect(NOTES_DB)
    cursor = conn.cursor()
    
    # Заметкалар учун таблица
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        trigger TEXT NOT NULL,
        content TEXT NOT NULL,
        created_by INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Мутлар учун таблица
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mutes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        muted_until TIMESTAMP NOT NULL,
        muted_by INTEGER NOT NULL,
        reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Админлар учун таблица
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS group_admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        added_by INTEGER NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Группа маълумотлар базаси ишга тушди")

def get_group_connection():
    """Группа базаси билан боғланиш"""
    return sqlite3.connect(NOTES_DB)

# Тексты на узбекском языке
TEXTS = {
    "ban_success": "✅ <b>{user}</b> гуруҳдан ҳақиқий ҳайдаб юборилди!",
    "ban_error": "❌ Фойдаланувчини ҳайдаб бўлмади. Мен ундан юқорироқ ҳуқуқға эгаман.",
    "kick_success": "✅ <b>{user}</b> гуруҳдан чиқариб юборилди!",
    "kick_error": "❌ Фойдаланувчини чиқариб бўлмади.",
    "mute_success": "🔇 <b>{user}</b> {time} муддатга овозсизланди!",
    "mute_error": "❌ Фойдаланувчини овозсизлантириб бўлмади.",
    "unmute_success": "🔊 <b>{user}</b> овози қайтарилди!",
    "unmute_error": "❌ Фойдаланувчини овозини қайтариб бўлмади.",
    "note_added": "📝 <b>Янги эслатма қўшилди:</b>\nТриггер: <code>{trigger}</code>\nМазмуни: {content}",
    "note_removed": "🗑️ <b>Эслатма ўчирилди:</b> #{note_id}",
    "note_not_found": "❌ Бундай ID га эга эслатма топилмади.",
    "note_triggered": "📌 <b>Эслатма:</b>\n{content}",
    "admin_added": "👑 <b>{user}</b> гуруҳда администратор қилиб тайинланди!",
    "admin_removed": "👑 <b>{user}</b> гуруҳдан администраторлик ҳуқуқи олиб ташланди!",
    "admin_list": "👑 <b>Гуруҳ администраторлари:</b>\n\n{admins}",
    "no_admins": "❌ Гуруҳда ҳеч қандай администратор йўқ.",
    "message_deleted": "🗑️ <b>Хабар ўчирилди!</b>",
    "no_permission": "⛔ <b>Сизда бу ҳаракатни бажариш учун ҳуқуқ йўқ!</b>",
    "user_not_found": "❌ Фойдаланувчи топилмади.",
    "syntax_error": "❌ <b>Нотўғри синтаксис!</b>\nТўғри фойдаланиш: <code>{syntax}</code>",
    "broadcast_success": "📢 <b>Хабар {count} та гуруҳга юборилди!</b>",
    "broadcast_error": "❌ Хабарни юборишда хатолик юз берди."
}

# Время мута по умолчанию
MUTE_TIMES = {
    "5m": timedelta(minutes=5),
    "30m": timedelta(minutes=30),
    "1h": timedelta(hours=1),
    "6h": timedelta(hours=6),
    "1d": timedelta(days=1),
    "7d": timedelta(days=7)
}

# ==============================
# 🔘 Админлик ҳуқуқини текшириш
# ==============================
async def is_group_admin(bot, chat_id, user_id):
    """Фойдаланувчи гуруҳда администраторми ёки йўқми"""
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

async def is_bot_admin(bot, chat_id):
    """Бот гуруҳда администраторми ёки йўқми"""
    try:
        me = await bot.get_me()
        member = await bot.get_chat_member(chat_id, me.id)
        return member.status in ['administrator', 'creator']
    except:
        return False

# ==============================
# 🔘 Бан қилиш
# ==============================
@router.message(Command("ban"))
async def ban_user(message: Message):
    """Фойдаланувчини гуруҳдан бан қилиш"""
    if not await is_bot_admin(message.bot, message.chat.id):
        return
    
    if not await is_group_admin(message.bot, message.chat.id, message.from_user.id):
        await message.reply(TEXTS["no_permission"])
        return
    
    if not message.reply_to_message:
        await message.reply(TEXTS["syntax_error"].format(syntax="/ban [сабаб] - хабарга жавобан"))
        return
    
    target_user = message.reply_to_message.from_user
    reason = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else "Сабаб кўрсатилмаган"
    
    try:
        await message.bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=target_user.id
        )
        await message.reply(TEXTS["ban_success"].format(user=target_user.full_name))
    except Exception as e:
        await message.reply(TEXTS["ban_error"])

# ==============================
# 🔘 Чиқариб юбориш
# ==============================
@router.message(Command("kick"))
async def kick_user(message: Message):
    """Фойдаланувчини гуруҳдан чиқариш"""
    if not await is_bot_admin(message.bot, message.chat.id):
        return
    
    if not await is_group_admin(message.bot, message.chat.id, message.from_user.id):
        await message.reply(TEXTS["no_permission"])
        return
    
    if not message.reply_to_message:
        await message.reply(TEXTS["syntax_error"].format(syntax="/kick [сабаб] - хабарга жавобан"))
        return
    
    target_user = message.reply_to_message.from_user
    reason = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else "Сабаб кўрсатилмаган"
    
    try:
        await message.bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=target_user.id,
            until_date=datetime.now() + timedelta(seconds=30)
        )
        await message.reply(TEXTS["kick_success"].format(user=target_user.full_name))
    except Exception as e:
        await message.reply(TEXTS["kick_error"])

# ==============================
# 🔘 Овозсизлантириш
# ==============================
@router.message(Command("mute"))
async def mute_user(message: Message, command: CommandObject):
    """Фойдаланувчини овозсизлантириш"""
    if not await is_bot_admin(message.bot, message.chat.id):
        return
    
    if not await is_group_admin(message.bot, message.chat.id, message.from_user.id):
        await message.reply(TEXTS["no_permission"])
        return
    
    if not message.reply_to_message:
        await message.reply(TEXTS["syntax_error"].format(syntax="/mute [вақт] [сабаб] - хабарга жавобан\nМисол: /mute 1h реклама учун"))
        return
    
    target_user = message.reply_to_message.from_user
    args = command.args.split() if command.args else []
    
    if not args:
        mute_time = timedelta(hours=1)
        reason = "Сабаб кўрсатилмаган"
    else:
        time_arg = args[0].lower()
        reason = ' '.join(args[1:]) if len(args) > 1 else "Сабаб кўрсатилмаган"
        
        if time_arg in MUTE_TIMES:
            mute_time = MUTE_TIMES[time_arg]
        else:
            # Время в минутах
            try:
                minutes = int(time_arg)
                mute_time = timedelta(minutes=minutes)
            except:
                mute_time = timedelta(hours=1)
    
    muted_until = datetime.now() + mute_time
    
    try:
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=target_user.id,
            permissions=ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False
            ),
            until_date=muted_until
        )
        
        # Мутни базага сақлаш
        conn = get_group_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO mutes (user_id, group_id, muted_until, muted_by, reason)
        VALUES (?, ?, ?, ?, ?)
        ''', (target_user.id, message.chat.id, muted_until, message.from_user.id, reason))
        conn.commit()
        conn.close()
        
        time_str = ""
        if mute_time.days > 0:
            time_str = f"{mute_time.days} кун"
        else:
            hours = mute_time.seconds // 3600
            minutes = (mute_time.seconds % 3600) // 60
            if hours > 0:
                time_str = f"{hours} соат"
            else:
                time_str = f"{minutes} дақиқа"
        
        await message.reply(TEXTS["mute_success"].format(user=target_user.full_name, time=time_str))
    except Exception as e:
        await message.reply(TEXTS["mute_error"])

# ==============================
# 🔘 Овозини қайтариш
# ==============================
@router.message(Command("unmute"))
async def unmute_user(message: Message):
    """Фойдаланувчининг овозини қайтариш"""
    if not await is_bot_admin(message.bot, message.chat.id):
        return
    
    if not await is_group_admin(message.bot, message.chat.id, message.from_user.id):
        await message.reply(TEXTS["no_permission"])
        return
    
    if not message.reply_to_message:
        await message.reply(TEXTS["syntax_error"].format(syntax="/unmute - хабарга жавобан"))
        return
    
    target_user = message.reply_to_message.from_user
    
    try:
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=target_user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        
        # Мутни базадан ўчириш
        conn = get_group_connection()
        cursor = conn.cursor()
        cursor.execute('''
        DELETE FROM mutes 
        WHERE user_id = ? AND group_id = ?
        ''', (target_user.id, message.chat.id))
        conn.commit()
        conn.close()
        
        await message.reply(TEXTS["unmute_success"].format(user=target_user.full_name))
    except Exception as e:
        await message.reply(TEXTS["unmute_error"])

# ==============================
# 🔘 Хабарни ўчириш
# ==============================
@router.message(Command("del"))
async def delete_message(message: Message):
    """Хабарни ўчириш"""
    if not await is_bot_admin(message.bot, message.chat.id):
        return
    
    if not await is_group_admin(message.bot, message.chat.id, message.from_user.id):
        await message.reply(TEXTS["no_permission"])
        return
    
    if not message.reply_to_message:
        await message.reply(TEXTS["syntax_error"].format(syntax="/del - ўчириш учун хабарга жавоб беринг"))
        return
    
    try:
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.reply_to_message.message_id
        )
        await message.delete()
    except:
        pass

# ==============================
# 🔘 Эслатма қўшиш
# ==============================
@router.message(Command("note"))
async def add_note(message: Message, command: CommandObject):
    """Янги эслатма қўшиш"""
    if not await is_group_admin(message.bot, message.chat.id, message.from_user.id):
        await message.reply(TEXTS["no_permission"])
        return
    
    if not command.args:
        await message.reply(TEXTS["syntax_error"].format(syntax="/note [триггер] [матн]"))
        return
    
    args = command.args.split(' ', 1)
    if len(args) < 2:
        await message.reply(TEXTS["syntax_error"].format(syntax="/note [триггер] [матн]"))
        return
    
    trigger = args[0].lower()
    content = args[1]
    
    conn = get_group_connection()
    cursor = conn.cursor()
    
    # Триггер мавжудлигини текшириш
    cursor.execute('''
    SELECT id FROM notes 
    WHERE group_id = ? AND trigger = ?
    ''', (message.chat.id, trigger))
    
    existing_note = cursor.fetchone()
    
    if existing_note:
        # Янгиланган эслатма
        cursor.execute('''
        UPDATE notes SET content = ?, created_by = ?
        WHERE id = ?
        ''', (content, message.from_user.id, existing_note[0]))
    else:
        # Янги эслатма
        cursor.execute('''
        INSERT INTO notes (group_id, trigger, content, created_by)
        VALUES (?, ?, ?, ?)
        ''', (message.chat.id, trigger, content, message.from_user.id))
    
    conn.commit()
    conn.close()
    
    await message.reply(TEXTS["note_added"].format(trigger=trigger, content=content))

# ==============================
# 🔘 Эслатмани ўчириш
# ==============================
@router.message(Command("delnote"))
async def delete_note(message: Message, command: CommandObject):
    """Эслатмани ўчириш"""
    if not await is_group_admin(message.bot, message.chat.id, message.from_user.id):
        await message.reply(TEXTS["no_permission"])
        return
    
    if not command.args:
        await message.reply(TEXTS["syntax_error"].format(syntax="/delnote [ID]"))
        return
    
    try:
        note_id = int(command.args)
    except ValueError:
        await message.reply(TEXTS["syntax_error"].format(syntax="/delnote [ID]"))
        return
    
    conn = get_group_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM notes 
    WHERE id = ? AND group_id = ?
    ''', (note_id, message.chat.id))
    
    if cursor.rowcount > 0:
        conn.commit()
        await message.reply(TEXTS["note_removed"].format(note_id=note_id))
    else:
        await message.reply(TEXTS["note_not_found"])
    
    conn.close()

# ==============================
# 🔘 Эслатмаларни кўрсатиш
# ==============================
@router.message(Command("notes"))
async def show_notes(message: Message):
    """Барча эслатмаларни кўрсатиш"""
    conn = get_group_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, trigger, content FROM notes 
    WHERE group_id = ? 
    ORDER BY id
    ''', (message.chat.id,))
    
    notes = cursor.fetchall()
    conn.close()
    
    if not notes:
        await message.reply("📝 <b>Ҳеч қандай эслатма топилмади.</b>")
        return
    
    text = "📋 <b>Гуруҳ эслатмалари:</b>\n\n"
    for note_id, trigger, content in notes:
        short_content = content[:50] + "..." if len(content) > 50 else content
        text += f"🔹 <b>#{note_id}</b> - <code>{trigger}</code>\n{short_content}\n\n"
    
    await message.reply(text)

# ==============================
# 🔘 Эслатма триггерларини қайта ишлаш
# ==============================
@router.message(F.text)
async def handle_note_triggers(message: Message):
    """Эслатма триггерларини аниклаш"""
    if not message.text or message.text.startswith('/'):
        return
    
    text = message.text.lower().strip()
    
    conn = get_group_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT content FROM notes 
    WHERE group_id = ? AND trigger = ?
    ''', (message.chat.id, text))
    
    note = cursor.fetchone()
    conn.close()
    
    if note:
        await message.reply(TEXTS["note_triggered"].format(content=note[0]))

# ==============================
# 🔘 Администратор қўшиш
# ==============================
@router.message(Command("addadmin"))
async def add_admin(message: Message):
    """Янги администратор қўшиш"""
    if not await is_group_admin(message.bot, message.chat.id, message.from_user.id):
        await message.reply(TEXTS["no_permission"])
        return
    
    if not message.reply_to_message:
        await message.reply(TEXTS["syntax_error"].format(syntax="/addadmin - фойдаланувчига жавобан"))
        return
    
    target_user = message.reply_to_message.from_user
    
    conn = get_group_connection()
    cursor = conn.cursor()
    
    # Администратор мавжудлигини текшириш
    cursor.execute('''
    SELECT id FROM group_admins 
    WHERE user_id = ? AND group_id = ?
    ''', (target_user.id, message.chat.id))
    
    existing_admin = cursor.fetchone()
    
    if existing_admin:
        await message.reply(f"❌ <b>{target_user.full_name}</b> аллақачон администратор!")
        conn.close()
        return
    
    # Янги администратор
    cursor.execute('''
    INSERT INTO group_admins (user_id, group_id, added_by)
    VALUES (?, ?, ?)
    ''', (target_user.id, message.chat.id, message.from_user.id))
    
    conn.commit()
    conn.close()
    
    await message.reply(TEXTS["admin_added"].format(user=target_user.full_name))

# ==============================
# 🔘 Администраторни олиб ташлаш
# ==============================
@router.message(Command("removeadmin"))
async def remove_admin(message: Message):
    """Администраторни олиб ташлаш"""
    if not await is_group_admin(message.bot, message.chat.id, message.from_user.id):
        await message.reply(TEXTS["no_permission"])
        return
    
    if not message.reply_to_message:
        await message.reply(TEXTS["syntax_error"].format(syntax="/removeadmin - фойдаланувчига жавобан"))
        return
    
    target_user = message.reply_to_message.from_user
    
    conn = get_group_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM group_admins 
    WHERE user_id = ? AND group_id = ?
    ''', (target_user.id, message.chat.id))
    
    if cursor.rowcount > 0:
        conn.commit()
        await message.reply(TEXTS["admin_removed"].format(user=target_user.full_name))
    else:
        await message.reply(f"❌ <b>{target_user.full_name}</b> администратор эмас!")
    
    conn.close()

# ==============================
# 🔘 Администраторлар рўйхати
# ==============================
@router.message(Command("admins"))
async def list_admins(message: Message):
    """Администраторлар рўйхати"""
    conn = get_group_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT user_id FROM group_admins 
    WHERE group_id = ?
    ''', (message.chat.id,))
    
    admin_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if not admin_ids:
        await message.reply(TEXTS["no_admins"])
        return
    
    admins_text = ""
    for user_id in admin_ids:
        try:
            user = await message.bot.get_chat(user_id)
            admins_text += f"👑 {user.full_name} (@{user.username})\n"
        except:
            admins_text += f"👑 ID: {user_id}\n"
    
    await message.reply(TEXTS["admin_list"].format(admins=admins_text))

# ==============================
# 🔘 Хабар тарқатиш
# ==============================
@router.message(Command("broadcast"))
async def broadcast_message(message: Message, command: CommandObject):
    """Хабарни барча гуруҳларга тарқатиш"""
    if not await is_group_admin(message.bot, message.chat.id, message.from_user.id):
        await message.reply(TEXTS["no_permission"])
        return
    
    if not command.args:
        await message.reply(TEXTS["syntax_error"].format(syntax="/broadcast [матн]"))
        return
    
    # Бу ерда барча гуруҳлар рўйхати бўлиши керак
    # Ҳозирча фақат жорий гуруҳга юборамиз
    try:
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=command.args
        )
        await message.reply(TEXTS["broadcast_success"].format(count=1))
    except Exception as e:
        await message.reply(TEXTS["broadcast_error"])

# ==============================
# 🔘 Ёрдам маълумотлари
# ==============================
@router.message(Command("help"))
async def help_command(message: Message):
    """Ёрдам маълумотлари"""
    help_text = """
🤖 <b>Бот Ёрдам Маълумотлари:</b>

👮 <b>Модерация:</b>
• /ban - Фойдаланувчини бан қилиш
• /kick - Фойдаланувчини чиқариб юбориш
• /mute - Фойдаланувчини овозсизлантириш
• /unmute - Фойдаланувчи овозини қайтариш
• /del - Хабарни ўчириш

📝 <b>Эслатмалар:</b>
• /note [триггер] [матн] - Янги эслатма қўшиш
• /delnote [ID] - Эслатмани ўчириш
• /notes - Барча эслатмаларни кўрсатиш

👑 <b>Администраторлар:</b>
• /addadmin - Администратор қўшиш
• /removeadmin - Администраторни олиб ташлаш
• /admins - Администраторлар рўйхати

📢 <b>Бошқа:</b>
• /broadcast [матн] - Хабар тарқатиш
• /help - Ёрдам маълумотлари

💡 <b>Эслатма:</b> Барча командалар фақат администраторлар учун!
    """
    
    await message.reply(help_text)

# Базани инициализация қилиш
init_group_db()