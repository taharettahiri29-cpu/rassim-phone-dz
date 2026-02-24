#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS ULTIMATE 2026
الإصدار المتوافق مع Python 3.14.3
أول سوق إلكتروني جزائري يغطي 69 ولاية
المالك: الطاهر الطاهري
"""

from __future__ import annotations
import streamlit as st
import sqlite3
import hashlib
import secrets
import time
import os
import base64
import random
import json
import sys
from datetime import datetime
from typing import Optional, Dict, List, Any, Tuple
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# التحقق من إصدار Python
# ==========================================
if sys.version_info < (3, 14, 3):
    st.error(f"⚠️ هذا التطبيق يتطلب Python 3.14.3 أو أحدث. الإصدار الحالي: {sys.version}")
    st.stop()

# ==========================================
# 1. إعدادات الصفحة المتقدمة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS ULTIMATE 2026 • 69 ولاية",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. الثوابت والتكوين
# ==========================================
class Config:
    """إعدادات التطبيق"""
    APP_NAME: str = "RASSIM OS ULTIMATE"
    APP_VERSION: str = "2026.3.14"
    UPLOADS_DIR: Path = Path("uploads")
    DB_PATH: Path = Path("rassim_os_ultimate.db")
    PYTHON_VERSION: str = "3.14.3"
    
    # إعدادات التشفير
    HASH_ITERATIONS: int = 100000
    HASH_ALGORITHM: str = 'sha256'
    
    # إعدادات التطبيق
    CACHE_TTL: int = 600
    MAX_ADS_PER_PAGE: int = 12
    MAX_IMAGE_SIZE: int = 5 * 1024 * 1024  # 5MB

# إنشاء المجلدات المطلوبة
Config.UPLOADS_DIR.mkdir(exist_ok=True)

# ==========================================
# 3. قائمة الولايات (69 ولاية) - باستخدام tuple للثبات
# ==========================================
ALGERIAN_WILAYAS: Tuple[str, ...] = (
    "الكل",
    "01 - أدرار", "02 - الشلف", "03 - الأغواط", "04 - أم البواقي", "05 - باتنة",
    "06 - بجاية", "07 - بسكرة", "08 - بشار", "09 - البليدة", "10 - البويرة",
    "11 - تمنراست", "12 - تبسة", "13 - تلمسان", "14 - تيارت", "15 - تيزي وزو",
    "16 - الجزائر", "17 - الجلفة", "18 - جيجل", "19 - سطيف", "20 - سعيدة",
    "21 - سكيكدة", "22 - سيدي بلعباس", "23 - عنابة", "24 - قالمة", "25 - قسنطينة",
    "26 - المدية", "27 - مستغانم", "28 - المسيلة", "29 - معسكر", "30 - ورقلة",
    "31 - وهران", "32 - البيض", "33 - إليزي", "34 - برج بوعريريج", "35 - بومرداس",
    "36 - الطارف", "37 - تندوف", "38 - تيسمسيلت", "39 - الوادي", "40 - خنشلة",
    "41 - سوق أهراس", "42 - تيبازة", "43 - ميلة", "44 - عين الدفلى", "45 - النعامة",
    "46 - عين تموشنت", "47 - غرداية", "48 - غليزان", "49 - تيميمون", "50 - برج باجي مختار",
    "51 - أولاد جلال", "52 - بني عباس", "53 - عين صالح", "54 - عين قزام", "55 - توقرت",
    "56 - جانت", "57 - المغير", "58 - المنيع", "59 - الطيبات", "60 - أولاد سليمان",
    "61 - سيدي خالد", "62 - بوسعادة", "63 - عين وسارة", "64 - حاسي بحبح", "65 - عين الملح",
    "66 - سيدي عيسى", "67 - عين الباردة", "68 - عين آزال", "69 - عين الحجر"
)

# ==========================================
# 4. إدارة حالة الجلسة (Session State)
# ==========================================
class SessionManager:
    """مدير حالة الجلسة - متوافق مع Python 3.14"""
    
    @staticmethod
    def initialize() -> None:
        """تهيئة جميع متغيرات الجلسة"""
        defaults: Dict[str, Any] = {
            'user': "زائر",
            'role': "guest",
            'ip': secrets.token_hex(8),
            'admin_access': False,
            'last_alert': None,
            'guest_mode': True,
            'filters': {
                "wilaya": "الكل",
                "min_price": 0,
                "max_price": 10000000,
                "search_query": "",
                "sort_by": "الأحدث",
                "category": "الكل"
            }
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

# تهيئة الجلسة
SessionManager.initialize()

# ==========================================
# 5. قاعدة البيانات - باستخدام Type Hints
# ==========================================
class Database:
    """إدارة قاعدة البيانات مع Python 3.14 features"""
    
    _instance: Optional[sqlite3.Connection] = None
    
    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        """الحصول على اتصال قاعدة البيانات (Singleton)"""
        if cls._instance is None:
            cls._instance = sqlite3.connect(
                str(Config.DB_PATH), 
                check_same_thread=False,
                isolation_level=None  # autocommit mode for 3.14
            )
            cls._instance.row_factory = sqlite3.Row
        return cls._instance
    
    @classmethod
    def init_db(cls) -> None:
        """تهيئة جداول قاعدة البيانات"""
        conn = cls.get_connection()
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
                status TEXT DEFAULT 'active',
                owner TEXT NOT NULL,
                verified INTEGER DEFAULT 1,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                image_path TEXT,
                rating REAL DEFAULT 4.5,
                cpu TEXT,
                ram TEXT,
                camera TEXT,
                capacity TEXT,
                battery TEXT,
                condition TEXT
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
        
        conn.commit()

# تهيئة قاعدة البيانات
Database.init_db()
conn = Database.get_connection()

# ==========================================
# 6. دوال التشفير - محسنة لـ Python 3.14
# ==========================================
class Security:
    """الأمان والتشفير"""
    
    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        """تشفير كلمة المرور باستخدام salt"""
        return hashlib.pbkdf2_hmac(
            Config.HASH_ALGORITHM,
            password.encode('utf-8'),
            salt.encode('utf-8'),
            Config.HASH_ITERATIONS
        ).hex()
    
    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """التحقق من صحة كلمة المرور"""
        return hashed == Security.hash_password(password, salt)

# ==========================================
# 7. دوال المساعدة
# ==========================================
class Helpers:
    """دوال مساعدة متفرقة"""
    
    @staticmethod
    def log_visitor() -> None:
        """تسجيل زائر جديد"""
        try:
            conn.execute(
                "INSERT INTO visitors (ip, page) VALUES (?, ?)",
                (st.session_state.ip, 'main')
            )
        except:
            pass
    
    @staticmethod
    def get_stats() -> Tuple[int, int, int, int]:
        """الحصول على إحصائيات الموقع"""
        try:
            users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            ads = conn.execute("SELECT COUNT(*) FROM ads WHERE status='active'").fetchone()[0]
            visitors = conn.execute("SELECT COUNT(*) FROM visitors").fetchone()[0]
            views = conn.execute("SELECT SUM(views) FROM ads").fetchone()[0] or 0
            return users, ads, visitors, views
        except:
            return 0, 0, 0, 0
    
    @staticmethod
    def save_uploaded_file(uploaded_file) -> Optional[str]:
        """حفظ ملف مرفوع"""
        if uploaded_file is not None:
            # التحقق من حجم الملف
            if uploaded_file.size > Config.MAX_IMAGE_SIZE:
                st.error("الملف كبير جداً. الحد الأقصى 5MB")
                return None
            
            file_extension = uploaded_file.name.split('.')[-1].lower()
            if file_extension not in ['png', 'jpg', 'jpeg']:
                st.error("الصيغة غير مدعومة. استخدم PNG, JPG")
                return None
            
            unique_filename = f"{secrets.token_hex(8)}.{file_extension}"
            file_path = Config.UPLOADS_DIR / unique_filename
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return str(file_path)
        return None
    
    @staticmethod
    def get_image_base64(image_path: str) -> Optional[str]:
        """تحويل الصورة إلى base64"""
        if image_path and Path(image_path).exists():
            try:
                with open(image_path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
            except:
                return None
        return None
    
    @staticmethod
    def display_ad_image(ad_image_path: Optional[str], remote_url: Optional[str] = None) -> str:
        """عرض الصورة بشكل ذكي"""
        if ad_image_path and Path(ad_image_path).exists():
            img_base64 = Helpers.get_image_base64(ad_image_path)
            if img_base64:
                return f'data:image/jpeg;base64,{img_base64}'
        return remote_url or "https://via.placeholder.com/400x300?text=صورة+الهاتف"

# ==========================================
# 8. الذكاء الاصطناعي - كاشف المشتري
# ==========================================
class BuyerDetector:
    """كشف المشتري الجدي"""
    
    SERIOUS_KEYWORDS: Tuple[str, ...] = (
        "حاب نشري", "نخلصك توت سويت", "وين نسكنو", 
        "كاش", "آخر سعر", "دابا", "نروحو نخلصو", "العنوان"
    )
    
    @classmethod
    def detect(cls, message: str, price_offered: int = 0) -> bool:
        """الكشف عن المشتري الجدي"""
        message_lower = message.lower() if message else ""
        is_serious = any(word in message_lower for word in cls.SERIOUS_KEYWORDS)
        
        if is_serious or price_offered > 0:
            st.session_state.last_alert = {
                'message': message,
                'price': price_offered,
                'time': datetime.now().strftime("%H:%M:%S")
            }
            st.toast("🚨 مشتري جدي!", icon="💰")
            return True
        return False

# ==========================================
# 9. روبوت RASSIM الذكي
# ==========================================
class RassimRobot:
    """روبوت المحادثة الذكي"""
    
    RESPONSES: Dict[str, str] = {
        "سعر": "💰 الأسعار عندنا هي الأفضل! تفقد الإعلانات وشوف بنفسك",
        "متوفر": "✅ كل الإعلانات المعروضة متوفرة حالياً",
        "تيبازة": "📍 مقرنا في فوكة (42). التوصيل لـ69 ولاية",
        "سلام": "وعليكم السلام! نورت RASSIM OS",
        "آيفون": "📱 آيفون 15 بـ225,000 دج موجود",
        "سامسونج": "📱 S24 Ultra بـ185,000 دج",
        "واد كنيس": "🎯 نحن البديل العصري لواد كنيس",
        "الدزة": "⚡ الدزة الجزائرية واجدة!",
        "وين": "📍 فوكة، تيبازة (42) - نغطي 69 ولاية",
        "69": "✅ 69 ولاية جزائرية مدعومة",
        "كيفاش": "💡 سجل، دوز على الإعلان، وضغط واتساب"
    }
    
    WELCOME_MESSAGE: str = """
    🎯 يا أهلاً بيك في RASSIM OS ULTIMATE! 🇩🇿 
    
    راني هنا باش نعاونك تبيع ولا تشري تليفونك في 69 ولاية بكل سهولة.
    
    🔥 ميزتي الكبيرة؟ نعرف شكون المشتري "الصح" وشكون اللي جاي "يقصر".
    
    ⚡ أدخل، سجل، وحط إعلانك.. الرادار راهو خدام!
    """
    
    @classmethod
    def get_response(cls, user_message: str) -> str:
        """الحصول على رد مناسب"""
        user_message = user_message.lower()
        
        if user_message == "ترحيب_خاص":
            return cls.WELCOME_MESSAGE
        
        for key, response in cls.RESPONSES.items():
            if key in user_message:
                if key in ["حاب نشري", "كاش", "وين"]:
                    BuyerDetector.detect(user_message)
                return response
        
        return "رسالتك وصلت! سأرد قريباً 🌟"

# ==========================================
# 10. الإعلانات التلقائية
# ==========================================
class AutoAds:
    """توليد إعلانات تلقائية"""
    
    PHONES: Tuple[Dict[str, Any], ...] = (
        {
            "name": "iPhone 15 Pro Max 512GB",
            "price_range": (210000, 240000),
            "img": "https://images.unsplash.com/photo-1696446701796-da61225697cc?w=400",
            "specs": {"cpu": "A17 Pro", "ram": "8GB", "cam": "48MP", "battery": "4422mAh"}
        },
        {
            "name": "Samsung S24 Ultra 512GB",
            "price_range": (180000, 205000),
            "img": "https://images.unsplash.com/photo-1707248545831-7e8c356f981e?w=400",
            "specs": {"cpu": "Snapdragon 8 Gen 3", "ram": "12GB", "cam": "200MP", "battery": "5000mAh"}
        },
        {
            "name": "Google Pixel 8 Pro 256GB",
            "price_range": (120000, 145000),
            "img": "https://images.unsplash.com/photo-1696429117066-e399580556f0?w=400",
            "specs": {"cpu": "Tensor G3", "ram": "12GB", "cam": "50MP", "battery": "5050mAh"}
        },
    )
    
    WILAYAS: Tuple[str, ...] = ("16 - الجزائر", "31 - وهران", "25 - قسنطينة", "42 - تيبازة", "06 - بجاية")
    SOURCES: Tuple[str, ...] = ("واد كنيس", "فيسبوك ماركت", "مجموعة RASSIM", "تاجر معتمد")
    TAGS: Tuple[str, ...] = ("🔥 عرض حي", "⚡ جديد", "⭐ مميز", "💰 فرصة")
    
    @classmethod
    def generate(cls, count: int = 9) -> List[Dict[str, Any]]:
        """توليد إعلانات تلقائية"""
        ads = []
        for i in range(count):
            phone = random.choice(cls.PHONES)
            price = random.randint(*phone["price_range"])
            wilaya = random.choice(cls.WILAYAS)
            
            ads.append({
                "id": i,
                "title": phone["name"],
                "price": price,
                "price_formatted": f"{price:,} دج",
                "wilaya": wilaya,
                "img": phone["img"],
                "source": random.choice(cls.SOURCES),
                "tag": random.choice(cls.TAGS),
                "specs": phone["specs"]
            })
        return ads

# ==========================================
# 11. واجهة المستخدم - PWA
# ==========================================
class PWA:
    """Progressive Web App"""
    
    @staticmethod
    def enable() -> None:
        """تفعيل PWA"""
        st.markdown("""
        <script>
        if ('serviceWorker' in navigator) {
          window.addEventListener('load', function() {
            navigator.serviceWorker.register('/sw.js').then(function(registration) {
              console.log('✅ ServiceWorker registered');
            }, function(err) {
              console.log('❌ ServiceWorker failed: ', err);
            });
          });
        }
        
        let deferredPrompt;
        window.addEventListener('beforeinstallprompt', (e) => {
          e.preventDefault();
          deferredPrompt = e;
        });
        </script>
        
        <link rel="manifest" href="/manifest.json">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-title" content="RASSIM OS">
        <link rel="apple-touch-icon" href="https://img.icons8.com/color/96/iphone.png">
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_manifest() -> None:
        """إنشاء ملف manifest.json"""
        manifest = {
            "name": "RASSIM OS ULTIMATE",
            "short_name": "RASSIM OS",
            "description": "أول سوق إلكتروني جزائري يغطي 69 ولاية",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#0a0a1a",
            "theme_color": "#00ffff",
            "icons": [
                {
                    "src": "https://img.icons8.com/color/192/iphone.png",
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": "https://img.icons8.com/color/512/iphone.png",
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ]
        }
        
        with open('manifest.json', 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        # إنشاء Service Worker
        sw_code = """
        self.addEventListener('install', function(event) {
            console.log('✅ Service Worker installed');
            self.skipWaiting();
        });
        
        self.addEventListener('activate', function(event) {
            console.log('✅ Service Worker activated');
        });
        
        self.addEventListener('fetch', function(event) {
            event.respondWith(
                caches.match(event.request).then(function(response) {
                    return response || fetch(event.request);
                })
            );
        });
        """
        
        with open('sw.js', 'w', encoding='utf-8') as f:
            f.write(sw_code)

# إنشاء ملفات PWA
PWA.create_manifest()

# ==========================================
# 12. التصميم المتقدم (CSS)
# ==========================================
class UIStyles:
    """تصميم واجهة المستخدم"""
    
    @staticmethod
    def inject() -> None:
        """إدخال CSS"""
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
        
        * {
            font-family: 'Cairo', sans-serif !important;
            direction: rtl;
            box-sizing: border-box;
        }
        
        .stApp {
            background: radial-gradient(circle at 20% 20%, #1a1a2a, #0a0a0f);
            color: #ffffff;
            min-height: 100vh;
        }
        
        .cyber-logo {
            text-align: center;
            padding: 20px;
            animation: fadeIn 1s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .logo-glitch {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 4rem;
            font-weight: 900;
            text-transform: uppercase;
            text-shadow: 0.05em 0 0 rgba(255,0,255,0.75),
                        -0.05em -0.05em 0 rgba(0,255,255,0.75);
            animation: glitch 2s infinite;
        }
        
        @keyframes glitch {
            0%, 100% { transform: none; opacity: 1; }
            92% { transform: none; opacity: 1; }
            93% { transform: skew(2deg, 1deg); opacity: 0.8; }
            94% { transform: skew(-2deg, -1deg); opacity: 0.9; }
            95% { transform: none; opacity: 1; }
        }
        
        .logo-sub {
            font-size: 1rem;
            letter-spacing: 8px;
            color: #00ffff;
            animation: glow 2s ease-in-out infinite;
        }
        
        @keyframes glow {
            0%, 100% { text-shadow: 0 0 10px #00ffff; }
            50% { text-shadow: 0 0 20px #ff00ff; }
        }
        
        .badge-69 {
            background: linear-gradient(135deg, #00ffff, #ff00ff);
            color: black;
            padding: 5px 20px;
            border-radius: 50px;
            font-weight: bold;
            font-size: 1.2rem;
            display: inline-block;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .hologram-card {
            background: rgba(20, 20, 30, 0.4);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(0, 255, 255, 0.1);
            border-radius: 30px;
            padding: 20px;
            margin-bottom: 20px;
            transition: all 0.4s ease;
            position: relative;
        }
        
        .hologram-card:hover {
            border-color: #00ffff;
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 255, 255, 0.2);
        }
        
        .ad-tag {
            position: absolute;
            top: 10px;
            right: 10px;
            background: linear-gradient(135deg, #ff00ff, #ff0000);
            color: white;
            padding: 4px 12px;
            border-radius: 50px;
            font-size: 0.7rem;
            font-weight: bold;
            z-index: 10;
        }
        
        .ad-image {
            width: 100%;
            height: 180px;
            object-fit: cover;
            border-radius: 20px;
            margin-bottom: 15px;
            border: 1px solid rgba(0, 255, 255, 0.3);
        }
        
        .stat-card {
            background: rgba(20, 20, 30, 0.5);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(0, 255, 255, 0.1);
            border-radius: 25px;
            padding: 20px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 2.2rem;
            font-weight: 800;
            color: #00ffff;
        }
        
        .wilaya-badge {
            display: inline-block;
            background: rgba(0, 255, 255, 0.1);
            border: 1px solid #00ffff;
            border-radius: 50px;
            padding: 5px 10px;
            margin: 3px;
            color: #00ffff;
            font-size: 0.8rem;
            white-space: nowrap;
        }
        
        .wilaya-counter {
            background: linear-gradient(135deg, #00ffff, #ff00ff);
            border-radius: 60px;
            padding: 15px 30px;
            display: inline-block;
            margin: 20px 0;
        }
        
        .wilaya-counter span {
            color: black;
            font-size: 2.5rem;
            font-weight: 900;
        }
        
        .stButton > button {
            background: linear-gradient(90deg, #00ffff, #ff00ff) !important;
            border: none !important;
            color: black !important;
            font-weight: 800 !important;
            border-radius: 15px !important;
            padding: 12px 25px !important;
            width: 100%;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(255, 0, 255, 0.3) !important;
        }
        
        .chat-bubble {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, #00ffff, #ff00ff);
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 9999;
            animation: float 3s ease-in-out infinite;
            box-shadow: 0 10px 20px rgba(0, 255, 255, 0.3);
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        .live-counter {
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid #00ffff;
            padding: 10px 20px;
            border-radius: 50px;
            z-index: 999;
            color: white;
            backdrop-filter: blur(5px);
        }
        
        .install-prompt {
            position: fixed;
            bottom: 100px;
            left: 20px;
            background: linear-gradient(135deg, #00ffff, #ff00ff);
            color: black;
            padding: 12px 20px;
            border-radius: 50px;
            font-weight: bold;
            cursor: pointer;
            z-index: 9998;
            animation: bounce 2s infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        
        .legal-footer {
            background: rgba(255, 0, 0, 0.1);
            border: 1px solid red;
            padding: 15px;
            border-radius: 10px;
            margin-top: 50px;
        }
        
        .legal-footer h5 {
            color: red;
            margin: 0;
        }
        
        .legal-footer p {
            font-size: 0.8rem;
            color: #ccc;
            margin: 5px 0;
        }
        
        @media screen and (max-width: 768px) {
            .logo-glitch { font-size: 2.2rem; }
            .stat-value { font-size: 1.8rem; }
        }
        </style>
        """, unsafe_allow_html=True)

# ==========================================
# 13. دوال الواجهة - عرض العناصر
# ==========================================
class UIComponents:
    """مكونات واجهة المستخدم"""
    
    @staticmethod
    def show_logo() -> None:
        st.markdown("""
        <div class="cyber-logo">
            <div class="logo-glitch">RASSIM OS</div>
            <div class="logo-sub">ULTIMATE 2026</div>
            <div class="badge-69">🇩🇿 69 ولاية جزائرية</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_live_counter() -> None:
        users, ads, visitors, views = Helpers.get_stats()
        st.markdown(f"""
        <div class="live-counter">
            <span style="color: #00ffff;">●</span> 
            <b>{visitors}</b> زائر • <b>{ads}</b> إعلان
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_install_prompt() -> None:
        st.markdown("""
        <div class="install-prompt" onclick="window.prompt('📱 للتثبيت، اضغط ⋮ ثم اضف إلى الشاشة الرئيسية')">
            ⚡ ثبت التطبيق على هاتفك
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_wilaya_counter() -> None:
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <div class="wilaya-counter">
                <span>69</span>
                <span style="color: black; font-size: 1.2rem; margin-right: 10px;">ولاية جزائرية</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_wilaya_badges() -> None:
        cols = st.columns(5)
        for i, wilaya in enumerate(ALGERIAN_WILAYAS[1:11]):
            with cols[i % 5]:
                display_text = wilaya[:8] + "..." if len(wilaya) > 10 else wilaya
                st.markdown(f"<span class='wilaya-badge'>{display_text}</span>", unsafe_allow_html=True)
    
    @staticmethod
    def show_auto_market() -> None:
        st.markdown("### 🤖 إعلانات محدثة تلقائياً")
        ads = AutoAds.generate(9)
        
        cols = st.columns(3)
        for i, ad in enumerate(ads):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="hologram-card">
                    <div class="ad-tag">{ad['tag']}</div>
                    <img src="{ad['img']}" class="ad-image">
                    <h4>{ad['title'][:30]}</h4>
                    <p style="color: #00ffff; font-size: 1.2rem;">{ad['price_formatted']}</p>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem;">
                        <span>📍 {ad['wilaya']}</span>
                        <span>🌐 {ad['source']}</span>
                    </div>
                    <div style="display: flex; gap: 5px; margin-top: 10px;">
                        <a href="https://wa.me/213555555555" style="flex:1;">
                            <button style="background:#25D366;">📱</button>
                        </a>
                        <a href="tel:0555555555" style="flex:1;">
                            <button style="background:transparent; border:2px solid #00ffff;">📞</button>
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    @staticmethod
    def show_market() -> None:
        st.markdown("### 🛍️ السوق الذكي")
        UIComponents.show_auto_market()
        
        st.markdown("---")
        st.markdown("### 📢 إعلانات المستخدمين")
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ads WHERE status='active' ORDER BY date DESC")
        user_ads = cursor.fetchall()
        
        if user_ads:
            cols = st.columns(3)
            for i, ad in enumerate(user_ads[:6]):
                img_src = Helpers.display_ad_image(ad[12] if len(ad) > 12 else None)
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="hologram-card">
                        <img src="{img_src}" class="ad-image">
                        <h4>{ad[1][:25]}</h4>
                        <p style="color: #00ffff;">{ad[2]:,} دج</p>
                        <p>📍 {ad[4]}</p>
                        <div style="display: flex; gap: 5px;">
                            <a href="tel:{ad[3]}" style="flex:1;">
                                <button style="background:#00ffff; color:black;">اتصال</button>
                            </a>
                            <a href="https://wa.me/{ad[3]}" style="flex:1;">
                                <button style="background:#25D366;">واتساب</button>
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("لا توجد إعلانات بعد")
    
    @staticmethod
    def show_live_chat() -> None:
        st.markdown("""
        <div class="chat-bubble" onclick="document.getElementById('chat_trigger').click();">
            <img src="https://img.icons8.com/ios-filled/30/ffffff/speech-bubble.png" width="30">
        </div>
        """, unsafe_allow_html=True)

        with st.sidebar:
            st.markdown("### 💬 روبوت RASSIM")
            with st.expander("🗣️ تحدث مع الروبوت", expanded=False):
                st.markdown('<div style="background:#ff00ff20; padding:10px; border-radius:10px;">أهلاً! أنا روبوت راسم الذكي</div>', unsafe_allow_html=True)
                msg = st.text_area("رسالتك:", height=80)
                if st.button("إرسال") and msg:
                    reply = RassimRobot.get_response(msg)
                    st.info(f"🤖 {reply}")
                    BuyerDetector.detect(msg)
    
    @staticmethod
    def show_legal_footer() -> None:
        st.markdown("""
        <div class="legal-footer">
            <h5>⚠️ تنبيه قانوني:</h5>
            <p>منصة RASSIM OS هي وسيط تقني فقط. نلتزم بالقانون 18-07 لحماية البيانات الشخصية.</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 14. صفحات التطبيق
# ==========================================
class Pages:
    """صفحات التطبيق"""
    
    @staticmethod
    def login() -> None:
        UIComponents.show_logo()
        UIComponents.show_wilaya_counter()
        
        users, ads, visitors, views = Helpers.get_stats()
        cols = st.columns(4)
        for i, (val, label) in enumerate(zip([users, ads, visitors, views], ["مستخدم", "إعلان", "زيارة", "مشاهدة"])):
            with cols[i]:
                st.markdown(f'<div class="stat-card"><div class="stat-value">{val}</div><div>{label}</div></div>', unsafe_allow_html=True)
        
        with st.expander("📍 الولايات المدعومة"):
            UIComponents.show_wilaya_badges()
        
        tab1, tab2 = st.tabs(["🔑 دخول", "📝 تسجيل"])
        
        with tab1:
            with st.form("login"):
                u = st.text_input("اسم المستخدم")
                p = st.text_input("كلمة المرور", type="password")
                if st.form_submit_button("دخول") and u and p:
                    if u == "admin" and p == "admin":
                        st.session_state.user = u
                        st.session_state.role = "admin"
                        st.rerun()
                    else:
                        user = conn.execute(
                            "SELECT password, salt, role FROM users WHERE username=?", 
                            (u,)
                        ).fetchone()
                        if user and Security.verify_password(p, user[0], user[1]):
                            st.session_state.user = u
                            st.session_state.role = user[2]
                            st.rerun()
                        else:
                            st.error("بيانات غير صحيحة")
        
        with tab2:
            with st.form("register"):
                nu = st.text_input("اسم مستخدم جديد")
                np = st.text_input("كلمة المرور", type="password")
                if st.form_submit_button("تسجيل") and nu and np:
                    if len(np) >= 6:
                        salt = secrets.token_hex(16)
                        hashed = Security.hash_password(np, salt)
                        try:
                            conn.execute(
                                "INSERT INTO users (username, password, salt, role) VALUES (?,?,?,'user')",
                                (nu, hashed, salt)
                            )
                            st.success("تم التسجيل!")
                        except sqlite3.IntegrityError:
                            st.error("المستخدم موجود")
                    else:
                        st.error("كلمة المرور قصيرة")
    
    @staticmethod
    def post_ad() -> None:
        if st.session_state.role == "guest":
            st.warning("يجب تسجيل الدخول لنشر إعلان")
            return
        
        st.markdown("### 📢 إعلان جديد")
        with st.form("new_ad"):
            title = st.text_input("اسم المنتج *")
            price = st.number_input("السعر *", min_value=0, step=1000)
            wilaya = st.selectbox("الولاية *", ALGERIAN_WILAYAS[1:])
            phone = st.text_input("رقم الهاتف *")
            desc = st.text_area("الوصف")
            uploaded = st.file_uploader("صورة", type=["png", "jpg", "jpeg"])
            
            if st.form_submit_button("نشر") and title and phone:
                img_path = Helpers.save_uploaded_file(uploaded)
                try:
                    conn.execute("""
                        INSERT INTO ads (title, price, phone, wilaya, description, category, owner, image_path)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (title, price, phone, wilaya, desc, "أخرى", st.session_state.user, img_path))
                    st.success("تم النشر!")
                    st.rerun()
                except Exception as e:
                    st.error(f"خطأ: {e}")
    
    @staticmethod
    def profile() -> None:
        if st.session_state.role == "guest":
            st.warning("هذه الصفحة للمستخدمين المسجلين")
            return
        
        st.markdown(f"### 👤 {st.session_state.user}")
        user_ads = conn.execute("SELECT COUNT(*) FROM ads WHERE owner=?", (st.session_state.user,)).fetchone()[0]
        user_views = conn.execute("SELECT SUM(views) FROM ads WHERE owner=?", (st.session_state.user,)).fetchone()[0] or 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("إعلاناتي", user_ads)
        with col2:
            st.metric("مشاهداتي", user_views)
    
    @staticmethod
    def admin() -> None:
        if st.session_state.role != "admin":
            st.error("غير مصرح")
            return
        
        st.markdown("### 🔐 لوحة الإدارة")
        users, ads, visitors, views = Helpers.get_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("المستخدمين", users)
        col2.metric("الإعلانات", ads)
        col3.metric("الزيارات", visitors)
        col4.metric("المشاهدات", views)

# ==========================================
# 15. الدالة الرئيسية - الماستر النهائي
# ==========================================
def main() -> None:
    """الدالة الرئيسية للتطبيق"""
    
    # عرض معلومات الإصدار
    st.sidebar.info(f"🚀 Python {Config.PYTHON_VERSION} • {Config.APP_NAME} v{Config.APP_VERSION}")
    
    # تفعيل PWA
    PWA.enable()
    
    # تطبيق التصميم
    UIStyles.inject()
    
    # عناصر ثابتة
    UIComponents.show_live_counter()
    UIComponents.show_install_prompt()
    UIComponents.show_live_chat()
    
    # عرض الشعار
    UIComponents.show_logo()
    
    if st.session_state.user:
        with st.sidebar:
            st.markdown(f"### أهلاً {st.session_state.user}")
            choice = st.radio("القائمة", ["السوق", "إعلان جديد", "حسابي", "خروج"])
            
            if st.session_state.role == "admin":
                if st.button("🔐 الإدارة"):
                    choice = "admin"
            
            if choice == "خروج":
                st.session_state.user = "زائر"
                st.session_state.role = "guest"
                st.rerun()
        
        if choice == "السوق":
            UIComponents.show_market()
        elif choice == "إعلان جديد":
            Pages.post_ad()
        elif choice == "حسابي":
            Pages.profile()
        elif choice == "admin":
            Pages.admin()
    else:
        Pages.login()
    
    # تسجيل الزائر
    Helpers.log_visitor()
    
    # تذييل قانوني
    UIComponents.show_legal_footer()

# ==========================================
# 16. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
        st.stop()

