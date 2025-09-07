from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.main_menu import main_menu
from keyboards.courses_menu import courses_menu
from data.languages import user_languages

router = Router()

# ---------------------------
# Список курсов по направлениям
# ---------------------------
def course_list(direction: str, lang: str = "ru") -> str:
    texts = {
        "it": {
            "ru": "💻 <b>IT Курсы:</b>\n- Python\n- Web-разработка\n- Робототехника",
            "uz": "💻 <b>IT Kurslari:</b>\n- Python\n- Veb-dasturlash\n- Robototexnika",
            "en": "💻 <b>IT Courses:</b>\n- Python\n- Web Development\n- Robotics"
        },
        "lang": {
            "ru": "🌍 <b>Языковые Курсы:</b>\n- Английский\n- Немецкий\n- Корейский",
            "uz": "🌍 <b>Tillar Kurslari:</b>\n- Ingliz tili\n- Nemis tili\n- Koreys tili",
            "en": "🌍 <b>Language Courses:</b>\n- English\n- German\n- Korean"
        },
        "math": {
            "ru": "🧮 <b>Математика:</b>\n- Подготовка к школе\n- ЕГЭ/ЦТ\n- Олимпиады",
            "uz": "🧮 <b>Matematika:</b>\n- Maktabga tayyorgarlik\n- Imtihonlarga tayyorlash\n- Olimpiadalar",
            "en": "🧮 <b>Math:</b>\n- School Prep\n- Exams\n- Olympiads"
        }
    }
    return texts[direction][lang]

# ---------------------------
# Обработка кнопки "📚 Курсы"
# ---------------------------
@router.callback_query(lambda c: c.data in ["courses", "dir_it", "dir_lang", "dir_math", "back_main"])
async def courses_handler(call: CallbackQuery):
    user_id = call.from_user.id
    lang = user_languages.get(user_id, "ru")  # по умолчанию русский
    data = call.data

    if data == "courses":
        texts = {
            "ru": "📚 <b>Выберите направление:</b>",
            "uz": "📚 <b>Yo‘nalishni tanlang:</b>",
            "en": "📚 <b>Choose a direction:</b>"
        }
        await call.message.answer(texts[lang], reply_markup=courses_menu(lang))
    
    elif data in ["dir_it", "dir_lang", "dir_math"]:
        direction = data.split("_")[1]
        await call.message.answer(course_list(direction, lang), reply_markup=courses_menu(lang))
    
    elif data == "back_main":
        greetings = {
            "ru": "🏠 Главное меню:",
            "uz": "🏠 Asosiy menyu:",
            "en": "🏠 Main menu:"
        }
        await call.message.answer(greetings[lang], reply_markup=main_menu(lang))

    await call.answer()  # убираем "часики" при нажатии