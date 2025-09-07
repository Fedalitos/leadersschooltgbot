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
            "ru": "💻 <b>IT Курсы:</b>\n- Программирование\n- Веб-разработка\n- Графический дизайн\n- Кибербезопасность",
            "uz": "💻 <b>IT Kurslari:</b>\n- Dasturlash\n- Veb-dasturlash\n- Grafik dizayn\n- Kiberxavfsizlik",
            "en": "💻 <b>IT Courses:</b>\n- Programming\n- Web Development\n- Graphic Design\n- Cybersecurity"
        },
        "lang": {
            "ru": "🌍 <b>Языковые Курсы:</b>\n- Английский язык\n- Русский язык\n- Немецкий язык\n- Корейский язык",
            "uz": "🌍 <b>Tillar Kurslari:</b>\n- Ingliz tili\n- Rus tili\n- Nemis tili\n- Koreys tili",
            "en": "🌍 <b>Language Courses:</b>\n- English Language\n- Russian Language\n- German Language\n- Korean Language"
        },
        "math": {
            "ru": "🧮 <b>Математика:</b>\n- Подготовка к школе\n- Подготовка к ОГЭ/ЕГЭ\n- Олимпиадная математика\n- Высшая математика",
            "uz": "🧮 <b>Matematika:</b>\n- Maktabga tayyorgarlik\n- Imtihonlarga tayyorlash\n- Olimpiada matematikasi\n- Oliy matematika",
            "en": "🧮 <b>Math:</b>\n- School Preparation\n- Exam Preparation\n- Olympiad Mathematics\n- Higher Mathematics"
        },
        "bio": {
            "ru": "🔬 <b>Биология:</b>\n- Общая биология\n- Подготовка к ЕГЭ\n- Анатомия и физиология\n- Молекулярная биология",
            "uz": "🔬 <b>Biologiya:</b>\n- Umumiy biologiya\n- Imtihonlarga tayyorlash\n- Anatomiya va fiziologiya\n- Molekulyar biologiya",
            "en": "🔬 <b>Biology:</b>\n- General Biology\n- Exam Preparation\n- Anatomy and Physiology\n- Molecular Biology"
        },
        "sat": {
            "ru": "🎓 <b>SAT Подготовка:</b>\n- SAT Mathematics\n- SAT Reading & Writing\n- SAT Practice Tests\n- Стратегии сдачи SAT",
            "uz": "🎓 <b>SAT Tayyorgarlik:</b>\n- SAT Matematika\n- SAT Reading & Writing\n- SAT Amaliy testlar\n- SAT topshirish strategiyalari",
            "en": "🎓 <b>SAT Preparation:</b>\n- SAT Mathematics\n- SAT Reading & Writing\n- SAT Practice Tests\n- SAT Test Strategies"
        }
    }
    return texts[direction][lang]

# ---------------------------
# Обработка кнопки "📚 Курсы"
# ---------------------------
@router.callback_query(lambda c: c.data in ["courses", "dir_it", "dir_lang", "dir_math", "dir_bio", "dir_sat", "back_main"])
async def courses_handler(call: CallbackQuery):
    user_id = call.from_user.id
    lang = user_languages.get(user_id, "ru")  # по умолчанию русский
    data = call.data

    if data == "courses":
        texts = {
            "ru": "📚 <b>Выберите направление:</b>",
            "uz": "📚 <b>Yo'nalishni tanlang:</b>",
            "en": "📚 <b>Choose a direction:</b>"
        }
        await call.message.answer(texts[lang], reply_markup=courses_menu(lang))
    
    elif data in ["dir_it", "dir_lang", "dir_math", "dir_bio", "dir_sat"]:
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