# ============================================
# 🔹 data/db.py — arizalar va savollar uchun ma'lumotlar bazasi
# ============================================

import sqlite3
import os

DB_PATH = "applications.db"

def init_db():
    """Ma'lumotlar bazasini ishga tushirish"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Таблица заявок
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        full_name TEXT NOT NULL,
        course TEXT NOT NULL,
        phone TEXT NOT NULL,
        lang TEXT NOT NULL,
        status TEXT DEFAULT 'kutilmoqda',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        admin_id INTEGER,
        admin_comment TEXT
    )
    ''')
    
    # Таблица вопросов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_text TEXT NOT NULL,
        lang TEXT NOT NULL,
        status TEXT DEFAULT 'waiting',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        admin_id INTEGER,
        answer_text TEXT
    )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Ma'lumotlar bazasi ishga tushirildi")

def get_connection():
    """Baza bilan bog'lanishni olish"""
    return sqlite3.connect(DB_PATH)

# Функции для заявок
def save_application(user_id: int, full_name: str, course: str, phone: str, lang: str) -> int:
    """Yangi arizani bazaga saqlash"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO applications (user_id, full_name, course, phone, lang, status)
    VALUES (?, ?, ?, ?, ?, 'kutilmoqda')
    ''', (user_id, full_name, course, phone, lang))
    
    application_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ Ariza saqlandi: ID {application_id}")
    return application_id

def update_application_status(application_id: int, status: str, admin_id: int = None, comment: str = None):
    """Ariza statusini yangilash"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE applications 
    SET status = ?, admin_id = ?, admin_comment = ?
    WHERE id = ?
    ''', (status, admin_id, comment, application_id))
    
    conn.commit()
    conn.close()
    print(f"✅ Ariza statusi yangilandi: ID {application_id} -> {status}")

def get_application(application_id: int):
    """Ariza ma'lumotlarini olish"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM applications WHERE id = ?', (application_id,))
    application = cursor.fetchone()
    
    conn.close()
    return application

def get_pending_applications():
    """Kutilayotgan arizalarni olish"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM applications WHERE status = "kutilmoqda" ORDER BY created_at DESC')
    applications = cursor.fetchall()
    
    conn.close()
    return applications

def get_user_applications(user_id: int):
    """Foydalanuvchi arizalarini olish"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM applications WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    applications = cursor.fetchall()
    
    conn.close()
    return applications

# Функции для вопросов
def save_question(user_id: int, question_text: str, lang: str) -> int:
    """Savolni bazaga saqlash"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO questions (user_id, question_text, lang, status)
    VALUES (?, ?, ?, 'waiting')
    ''', (user_id, question_text, lang))
    
    question_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ Savol saqlandi: ID {question_id}")
    return question_id

def update_question_status(question_id: int, status: str, admin_id: int = None, answer_text: str = None):
    """Savol statusini yangilash"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE questions 
    SET status = ?, admin_id = ?, answer_text = ?
    WHERE id = ?
    ''', (status, admin_id, answer_text, question_id))
    
    conn.commit()
    conn.close()
    print(f"✅ Savol statusi yangilandi: ID {question_id} -> {status}")

def get_question(question_id: int):
    """Savol ma'lumotlarini olish"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM questions WHERE id = ?', (question_id,))
    question = cursor.fetchone()
    
    conn.close()
    return question

# ============================================
# 🔹 data/db.py — добавим функции для статистики
# ============================================

# ... существующий код ...

# Функции для статистики
def get_statistics():
    """Получить полную статистику бота"""
    conn = get_connection()
    cursor = conn.cursor()
    
    stats = {}
    
    # Статистика заявок
    cursor.execute('SELECT COUNT(*) FROM applications')
    stats['total_applications'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM applications WHERE status = "kutilmoqda"')
    stats['pending_applications'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM applications WHERE status = "qabul qilindi"')
    stats['approved_applications'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM applications WHERE status = "rad etildi"')
    stats['rejected_applications'] = cursor.fetchone()[0]
    
    # Статистика вопросов
    cursor.execute('SELECT COUNT(*) FROM questions')
    stats['total_questions'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM questions WHERE status = "waiting"')
    stats['pending_questions'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM questions WHERE status = "answered"')
    stats['answered_questions'] = cursor.fetchone()[0]
    
    # Статистика по дням (последние 7 дней)
    cursor.execute('''
    SELECT DATE(created_at) as date, COUNT(*) as count 
    FROM applications 
    WHERE created_at >= date('now', '-7 days')
    GROUP BY DATE(created_at)
    ORDER BY date DESC
    ''')
    stats['applications_last_7_days'] = cursor.fetchall()
    
    cursor.execute('''
    SELECT DATE(created_at) as date, COUNT(*) as count 
    FROM questions 
    WHERE created_at >= date('now', '-7 days')
    GROUP BY DATE(created_at)
    ORDER BY date DESC
    ''')
    stats['questions_last_7_days'] = cursor.fetchall()
    
    # Популярные курсы
    cursor.execute('''
    SELECT course, COUNT(*) as count 
    FROM applications 
    GROUP BY course 
    ORDER BY count DESC 
    LIMIT 5
    ''')
    stats['popular_courses'] = cursor.fetchall()
    
    conn.close()
    return stats

def get_user_count():
    """Получить количество уникальных пользователей"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(DISTINCT user_id) FROM applications')
    applications_users = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT user_id) FROM questions')
    questions_users = cursor.fetchone()[0]
    
    # Объединяем пользователей из обеих таблиц
    cursor.execute('''
    SELECT COUNT(DISTINCT user_id) FROM (
        SELECT user_id FROM applications 
        UNION 
        SELECT user_id FROM questions
    )
    ''')
    total_users = cursor.fetchone()[0]
    
    conn.close()
    return {
        'total_users': total_users,
        'applications_users': applications_users,
        'questions_users': questions_users
    }
    
# Добавим в db.py новые функции
def get_pending_applications_count():
    """Количество ожидающих заявок"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM applications WHERE status = "kutilmoqda"')
    count = cursor.fetchone()[0]
    
    conn.close()
    return count

def get_pending_questions_count():
    """Количество ожидающих вопросов"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM questions WHERE status = "waiting"')
    count = cursor.fetchone()[0]
    
    conn.close()
    return count

def get_recent_applications(limit=5):
    """Последние заявки"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, user_id, full_name, course, created_at 
    FROM applications 
    WHERE status = "kutilmoqda" 
    ORDER BY created_at DESC 
    LIMIT ?
    ''', (limit,))
    
    applications = cursor.fetchall()
    conn.close()
    return applications

def get_recent_questions(limit=5):
    """Последние вопросы"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, user_id, question_text, created_at 
    FROM questions 
    WHERE status = "waiting" 
    ORDER BY created_at DESC 
    LIMIT ?
    ''', (limit,))
    
    questions = cursor.fetchall()
    conn.close()
    return questions