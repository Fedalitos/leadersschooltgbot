# ============================================
# 🔹 handlers/admin.py — administrator harakatlari
# ============================================

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data.db import update_application_status, update_question_status
from data.languages import user_languages
from data.admins import is_admin

router = Router()

# Состояние для ответа на вопрос
class AnswerState(StatesGroup):
    waiting_for_answer = State()

# Foydalanuvchilarga javob matnlari
response_texts = {
    "ru": {
        "approved": "✅ <b>Ваша заявка одобрена!</b>\n\nАдминистратор свяжется с вами для уточнения деталей.",
        "rejected": "❌ <b>Ваша заявка отклонена.</b>\n\nДля уточнения информации обратитесь к администратору.",
        "answered": "💬 <b>Ответ на ваш вопрос:</b>\n\n{}",
        "not_admin": "⛔ <b>У вас нет прав администратора!</b>"
    },
    "uz": {
        "approved": "✅ <b>Arizangiz qabul qilindi!</b>\n\nAdministrator tafsilotlar uchun siz bilan bog'lanadi.",
        "rejected": "❌ <b>Arizangiz rad etildi.</b>\n\nMa'lumot uchun administratorga murojaat qiling.",
        "answered": "💬 <b>Savolingizga javob:</b>\n\n{}",
        "not_admin": "⛔ <b>Sizda administrator huquqlari yo'q!</b>"
    },
    "en": {
        "approved": "✅ <b>Your application has been approved!</b>\n\nAdministrator will contact you for details.",
        "rejected": "❌ <b>Your application has been rejected.</b>\n\nContact administrator for information.",
        "answered": "💬 <b>Answer to your question:</b>\n\n{}",
        "not_admin": "⛔ <b>You don't have administrator rights!</b>"
    }
}

# ==============================
# 🔘 Administrator harakatlarini qayta ishlash
# ==============================
@router.callback_query(lambda c: c.data.startswith(("approve_", "reject_", "contact_", "delete_", "answer_question_", "question_done_", "delete_question_")))
async def admin_action(call: CallbackQuery, state: FSMContext):
    # Administratorlik huquqini tekshirish
    if not is_admin(call.from_user.id):
        lang = user_languages.get(call.from_user.id, "uz")
        await call.answer(response_texts[lang]["not_admin"], show_alert=True)
        return
    
    data = call.data
    admin_id = call.from_user.id
    
    if data.startswith("approve_"):
        # Qabul qilish
        parts = data.split("_")
        target_user_id = int(parts[1])
        application_id = int(parts[2])
        
        # Foydalanuvchi tilini olish
        user_lang = user_languages.get(target_user_id, "uz")
        
        # Ariza statusini yangilash
        update_application_status(application_id, "qabul qilindi", admin_id, "Ariza qabul qilindi")
        
        # Foydalanuvchiga xabar (o'z tilida)
        user_text = response_texts[user_lang]["approved"]
        
        try:
            await call.bot.send_message(chat_id=target_user_id, text=user_text)
        except:
            pass
            
        await call.answer("✅ Ariza qabul qilindi")
        await call.message.edit_reply_markup(reply_markup=None)
        
    elif data.startswith("reject_"):
        # Rad etish
        parts = data.split("_")
        target_user_id = int(parts[1])
        application_id = int(parts[2])
        
        # Foydalanuvchi tilini olish
        user_lang = user_languages.get(target_user_id, "uz")
        
        # Ariza statusini yangilash
        update_application_status(application_id, "rad etildi", admin_id, "Ariza rad etildi")
        
        # Foydalanuvchiga xabar (o'z tilida)
        user_text = response_texts[user_lang]["rejected"]
        
        try:
            await call.bot.send_message(chat_id=target_user_id, text=user_text)
        except:
            pass
            
        await call.answer("❌ Ariza rad etildi")
        await call.message.edit_reply_markup(reply_markup=None)
        
    elif data.startswith("answer_question_"):
        # Ответить на вопрос
        parts = data.split("_")
        target_user_id = int(parts[2])
        question_id = int(parts[3])
        
        # Сохраняем данные для ответа
        await state.update_data(target_user_id=target_user_id, question_id=question_id)
        await call.message.answer("💬 <b>Введите ответ для пользователя:</b>")
        await state.set_state(AnswerState.waiting_for_answer)
        await call.answer()
        
    elif data.startswith("question_done_"):
        # Отметить как отвеченное
        question_id = int(data.split("_")[2])
        update_question_status(question_id, "answered", call.from_user.id)
        await call.message.edit_reply_markup(reply_markup=None)
        await call.answer("✅ Вопрос отмечен как отвеченный")
        
    elif data.startswith("contact_"):
        # Bog'lanish
        target_user_id = int(data.split("_")[1])
        await call.answer(f"Foydalanuvchi ID: {target_user_id}")
        
    elif data.startswith("delete_"):
        # O'chirish
        application_id = int(data.split("_")[1])
        await call.message.delete()
        await call.answer("🗑️ Ariza o'chirildi")
        
    elif data.startswith("delete_question_"):
        # Удалить вопрос
        question_id = int(data.split("_")[2])
        await call.message.delete()
        await call.answer("🗑️ Вопрос удален")

# ==============================
# 🔘 Обработка ответа на вопрос
# ==============================
@router.message(AnswerState.waiting_for_answer)
async def process_admin_answer(message: Message, state: FSMContext):
    user_data = await state.get_data()
    
    if 'target_user_id' in user_data and 'question_id' in user_data:
        target_user_id = user_data['target_user_id']
        question_id = user_data['question_id']
        answer_text = message.text
        
        # Получаем язык пользователя
        user_lang = user_languages.get(target_user_id, "uz")
        
        # Отправляем ответ пользователю
        try:
            response_text = response_texts[user_lang]["answered"].format(answer_text)
            await message.bot.send_message(chat_id=target_user_id, text=response_text)
            
            # Обновляем статус вопроса
            update_question_status(question_id, "answered", message.from_user.id, answer_text)
            
            await message.answer("✅ Ответ отправлен пользователю!")
        except Exception as e:
            await message.answer(f"❌ Ошибка отправки: {e}")
        
        await state.clear()