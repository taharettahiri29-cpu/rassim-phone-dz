import sqlite3
import hashlib
import secrets
import os
import streamlit as st

# ==========================================
# إعدادات قاعدة البيانات
# ==========================================
DB = "rassim_os_ultimate.db"
UPLOADS_DIR = "uploads"

# إنشاء مجلد الصور إذا لم يكن موجوداً
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

def init_db():
    """تهيئة قاعدة البيانات مع جميع الجداول"""
    try:
        conn = sqlite3.connect(DB, check_same_thread=False)
        cursor = conn.cursor()
        
        # جدول المستخدمين
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                salt TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                role TEXT DEFAULT 'user',
                verified INTEGER DEFAULT 1,
                banned INTEGER DEFAULT 0,
                ad_count INTEGER DEFAULT 0,
                last_login TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # جدول الإعلانات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price INTEGER NOT NULL,
                phone TEXT NOT NULL,
                wilaya TEXT NOT NULL,
                description TEXT,
                category TEXT DEFAULT 'أخرى',
                views INTEGER DEFAULT 0,
                featured INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                owner TEXT NOT NULL,
                verified INTEGER DEFAULT 1,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                image_path TEXT,
                image_url TEXT
            )
        """)
        
        # جدول الرسائل
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                message TEXT NOT NULL,
                read INTEGER DEFAULT 0,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # جدول الزوار
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                page TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # جدول التنبيهات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                price INTEGER,
                status TEXT DEFAULT 'new',
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # جدول الإعلانات الممولة
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS promoted_ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                link TEXT,
                views INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        return conn
    except Exception as e:
        st.error(f"خطأ في قاعدة البيانات: {e}")
        return None

def get_connection():
    """الحصول على اتصال بقاعدة البيانات"""
    return sqlite3.connect(DB, check_same_thread=False)

def hash_password(password, salt):
    """تشفير كلمة المرور باستخدام salt"""
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    ).hex()

def hash_pass(password):
    """تشفير بسيط للتوافق (يمكن استخدامه في حال عدم وجود salt)"""
    return hashlib.sha256(password.encode()).hexdigest()
