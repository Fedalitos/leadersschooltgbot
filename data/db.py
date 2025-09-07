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