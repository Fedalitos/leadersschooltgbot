# ============================================
# 🔹 handlers/admin.py — administrator harakatlari
# ============================================

from aiogram import Router
from aiogram.types import CallbackQuery
from data.db import update_application_status
from data.languages import user_languages
from data.admins import is_admin

router = Router()

# Foydalanuvchilarga javob matnlari
response_texts = {
    "ru": {
        "approved": "✅ <b>Ваша заявка одобрена!</b>\n\nАдминистратор свяжется с вами для уточнения деталей.",
        "rejected": "❌ <b>Ваша заявка отклонена.</b>\n\nДля уточнения информации обратитесь к администратору.",
        "not_admin": "⛔ <b>У вас нет прав администратора!</b>"
    },
    "uz": {
        "approved": "✅ <b>Arizangiz qabul qilindi!</b>\n\nAdministrator tafsilotlar uchun siz bilan bog'lanadi.",
        "rejected": "❌ <b>Arizangiz rad etildi.</b>\n\nMa'lumot uchun administratorga murojaat qiling.",
        "not_admin": "⛔ <b>Sizda administrator huquqlari yo'q!</b>"
    },
    "en": {
        "approved": "✅ <b>Your application has been approved!</b>\n\nAdministrator will contact you for details.",
        "rejected": "❌ <b>Your application has been rejected.</b>\n\nContact administrator for information.",
        "not_admin": "⛔ <b>You don't have administrator rights!</b>"
    }
}

# ==============================
# 🔘 Administrator harakatlarini qayta ishlash
# ==============================
@router.callback_query(lambda c: c.data.startswith(("approve_", "reject_", "contact_", "delete_")))
async def admin_action(call: CallbackQuery):
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
        
    elif data.startswith("contact_"):
        # Bog'lanish
        target_user_id = int(data.split("_")[1])
        await call.answer(f"Foydalanuvchi ID: {target_user_id}")
        
    elif data.startswith("delete_"):
        # O'chirish
        application_id = int(data.split("_")[1])
        await call.message.delete()
        await call.answer("🗑️ Ariza o'chirildi")