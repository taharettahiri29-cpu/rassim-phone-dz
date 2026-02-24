#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS ULTIMATE 2026
منصة وسيط ذكي شامل - 69 ولاية
هواتف • عقارات • سيارات • خردة • خدمات
نظام وساطة متكامل مع كاشف الجدية والتبليغ
"""

import streamlit as st
import sqlite3
import random
import time
import json
import hashlib
import secrets
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, Any, Optional, List

# ==========================================
# 1. إعدادات الصفحة المتقدمة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS ULTIMATE • الوسيط الذكي",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. الثوابت والتكوين
# ==========================================
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)
DB_PATH = Path("rassim_os_ultimate.db")

# ==========================================
# 3. قائمة الفئات الشاملة
# ==========================================
CATEGORIES: Tuple[str, ...] = (
    "الكل",
    "📱 هواتف ونقالات",
    "🚗 قطع غيار السيارات",
    "🏠 عقارات (بيع/كراء)",
    "💄 تجميل و Cosmetique",
    "🛋️ أثاث ومنزل",
    "🔧 خردة وأدوات مستعملة",
    "👕 ملابس وأزياء",
    "🛠️ خدمات",
    "📦 أخرى"
)

# ==========================================
# 4. قائمة الولايات (69 ولاية)
# ==========================================
WILAYAS: Tuple[str, ...] = (
    "16 - الجزائر", "31 - وهران", "25 - قسنطينة", "42 - تيبازة", "06 - بجاية",
    "19 - سطيف", "23 - عنابة", "13 - تلمسان", "09 - البليدة", "15 - تيزي وزو",
    "07 - بسكرة", "26 - المدية", "29 - معسكر", "35 - بومرداس", "41 - سوق أهراس",
    "47 - غرداية", "55 - توقرت", "57 - المغير", "58 - المنيع", "69 - عين الحجر",
    "01 - أدرار", "02 - الشلف", "03 - الأغواط", "04 - أم البواقي", "05 - باتنة",
    "08 - بشار", "10 - البويرة", "11 - تمنراست", "12 - تبسة", "14 - تيارت",
    "17 - الجلفة", "18 - جيجل", "20 - سعيدة", "21 - سكيكدة", "22 - سيدي بلعباس",
    "24 - قالمة", "27 - مستغانم", "28 - المسيلة", "30 - ورقلة", "32 - البيض",
    "33 - إليزي", "34 - برج بوعريريج", "36 - الطارف", "37 - تندوف", "38 - تيسمسيلت",
    "39 - الوادي", "40 - خنشلة", "41 - سوق أهراس", "43 - ميلة", "44 - عين الدفلى",
    "45 - النعامة", "46 - عين تموشنت", "47 - غرداية", "48 - غليزان", "49 - تيميمون",
    "50 - برج باجي مختار", "51 - أولاد جلال", "52 - بني عباس", "53 - عين صالح",
    "54 - عين قزام", "55 - توقرت", "56 - جانت", "57 - المغير", "58 - المنيع",
    "59 - الطيبات", "60 - أولاد سليمان", "61 - سيدي خالد", "62 - بوسعادة",
    "63 - عين وسارة", "64 - حاسي بحبح", "65 - عين الملح", "66 - سيدي عيسى",
    "67 - عين الباردة", "68 - عين آزال"
)

# ==========================================
# 5. حالات السلعة
# ==========================================
CONDITIONS: Tuple[str, ...] = (
    "جديد", "ممتاز", "جيد جداً", "مستعمل", "للإصلاح", "خردة"
)

# ==========================================
# 6. كلمات مفتاحية لكاشف الجدية
# ==========================================
SERIOUS_KEYWORDS: Dict[str, List[str]] = {
    "عام": ["حاب نشري", "نخلصك", "وين نسكنو", "كاش", "آخر سعر", "دابا", "نروحو"],
    "عقارات": ["حاب نكري", "حاب نشري دار", "وقتاش نشوف", "العقار", "شقة", "فيلا"],
    "سيارات": ["حاب نشري سيارة", "قطع غيار", "رونو", "هيونداي", "بيجو"],
    "خردة": ["شحال", "وين راهي", "نخلص دابا"]
}

# ==========================================
# 7. قاعدة البيانات المتطورة
# ==========================================
@st.cache_resource
def get_connection():
    return sqlite3.connect(str(DB_PATH), check_same_thread=False)

conn = get_connection()

def init_db():
    cursor = conn.cursor()
    
    # جدول الإعلانات الرئيسي
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            price INTEGER NOT NULL,
            wilaya TEXT NOT NULL,
            description TEXT,
            condition TEXT,
            metadata TEXT,  -- JSON data للمواصفات المتغيرة
            seller_name TEXT NOT NULL,
            seller_phone TEXT NOT NULL,
            image_url TEXT,
            views INTEGER DEFAULT 0,
            reports INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # جدول طلبات المشتريين (أبحث عن)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buyer_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            max_price INTEGER,
            wilaya TEXT NOT NULL,
            buyer_name TEXT NOT NULL,
            buyer_phone TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # جدول التبليغات
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_id INTEGER,
            reporter_name TEXT,
            reporter_phone TEXT,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ad_id) REFERENCES ads(id)
        )
    """)
    
    conn.commit()

init_db()

# ==========================================
# 8. المتغيرات في الجلسة
# ==========================================
if 'user' not in st.session_state:
    st.session_state.user = "زائر"
if 'role' not in st.session_state:
    st.session_state.role = "guest"
if 'last_alert' not in st.session_state:
    st.session_state.last_alert = None
if 'show_form' not in st.session_state:
    st.session_state.show_form = False
if 'show_request_form' not in st.session_state:
    st.session_state.show_request_form = False
if 'ads' not in st.session_state:
    st.session_state.ads = []
    st.session_state.requests = []
    st.session_state.last_update = datetime.now().strftime("%H:%M:%S")

# ==========================================
# 9. إعلانات تلقائية متنوعة
# ==========================================
def get_auto_ads():
    """توليد إعلانات تلقائية لجميع الفئات"""
    
    ads = []
    
    # هواتف
    phones = [
        {
            "category": "📱 هواتف ونقالات",
            "title": "iPhone 15 Pro Max 512GB",
            "price": 225000,
            "img": "https://images.unsplash.com/photo-1696446701796-da61225697cc?w=400&h=300&fit=crop",
            "condition": "جديد",
            "metadata": {"ram": "8GB", "storage": "512GB", "color": "أسود", "battery": "100%"},
            "seller": "محمد",
            "phone": "0555123456"
        },
        {
            "category": "📱 هواتف ونقالات",
            "title": "Samsung S24 Ultra",
            "price": 185000,
            "img": "https://images.unsplash.com/photo-1707248545831-7e8c356f981e?w=400&h=300&fit=crop",
            "condition": "ممتاز",
            "metadata": {"ram": "12GB", "storage": "512GB", "color": "فضي", "battery": "98%"},
            "seller": "أحمد",
            "phone": "0666123456"
        }
    ]
    
    # قطع غيار سيارات
    car_parts = [
        {
            "category": "🚗 قطع غيار السيارات",
            "title": "محرك رونو كليو 2 ديزل",
            "price": 45000,
            "img": "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=400&h=300&fit=crop",
            "condition": "مستعمل",
            "metadata": {"car_model": "رونو كليو 2", "year": "2005", "part_number": "K9K 702", "mileage": "120000 كم"},
            "seller": "علي",
            "phone": "0555987123"
        },
        {
            "category": "🚗 قطع غيار السيارات",
            "title": "فرامل أمامية بيجو 308",
            "price": 8500,
            "img": "https://images.unsplash.com/photo-1599762676042-6fe94b5e6a6e?w=400&h=300&fit=crop",
            "condition": "جديد",
            "metadata": {"car_model": "بيجو 308", "type": "أقراص فرامل", "brand": "Bosch"},
            "seller": "ياسين",
            "phone": "0775987123"
        }
    ]
    
    # عقارات
    properties = [
        {
            "category": "🏠 عقارات (بيع/كراء)",
            "title": "شقة للبيع في حيدرة 3 غرف",
            "price": 45000000,
            "img": "https://images.unsplash.com/photo-1560448204-603b3fc33ddc?w=400&h=300&fit=crop",
            "condition": "للبيع",
            "metadata": {"rooms": 3, "surface": "120m²", "floor": 2, "furnished": False, "parking": True},
            "seller": "نسرين",
            "phone": "0555876123"
        },
        {
            "category": "🏠 عقارات (بيع/كراء)",
            "title": "محل تجاري للكراء في باب الزوار",
            "price": 350000,
            "img": "https://images.unsplash.com/photo-1558888401-60b4d6c3a6b9?w=400&h=300&fit=crop",
            "condition": "للكراء",
            "metadata": {"surface": "80m²", "location": "باب الزوار", "electricity": True, "water": True},
            "seller": "عبد الرحمان",
            "phone": "0665876123"
        }
    ]
    
    # أثاث
    furniture = [
        {
            "category": "🛋️ أثاث ومنزل",
            "title": "طقم صالون 4 قطع",
            "price": 45000,
            "img": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=300&fit=crop",
            "condition": "جديد",
            "metadata": {"material": "خشب + قماش", "color": "بيج", "pieces": 4},
            "seller": "سهام",
            "phone": "0555876345"
        }
    ]
    
    # خردة
    scrap = [
        {
            "category": "🔧 خردة وأدوات مستعملة",
            "title": "عدد يدوية متنوعة (شنطة كاملة)",
            "price": 12000,
            "img": "https://images.unsplash.com/photo-1581141848549-07e4b2840f8a?w=400&h=300&fit=crop",
            "condition": "مستعمل",
            "metadata": {"tools_count": 25, "type": "عدد كهربائية ويدوية"},
            "seller": "فتحي",
            "phone": "0775987456"
        }
    ]
    
    # دمج كل الإعلانات
    all_ads = phones + car_parts + properties + furniture + scrap
    
    for i, ad in enumerate(all_ads):
        ad["id"] = i + 1
        ad["price_f"] = f"{ad['price']:,} دج"
        ad["wilaya"] = random.choice(WILAYAS)
        ad["image_url"] = ad["img"]
        ad["seller_name"] = ad["seller"]
        ad["seller_phone"] = ad["phone"]
        ad["metadata_json"] = json.dumps(ad["metadata"], ensure_ascii=False)
    
    return all_ads

# ==========================================
# 10. طلبات شراء تلقائية
# ==========================================
def get_auto_requests():
    """توليد طلبات شراء تلقائية"""
    requests = [
        {
            "category": "🚗 قطع غيار السيارات",
            "title": "أبحث عن محرك رونو كليو 2",
            "description": "محرك ديزل بحالة جيدة",
            "max_price": 50000,
            "wilaya": "16 - الجزائر",
            "buyer": "ناصر",
            "phone": "0555987234"
        },
        {
            "category": "🏠 عقارات (بيع/كراء)",
            "title": "أبحث عن شقة كراء في الجزائر",
            "description": "غرفتين + صالون",
            "max_price": 30000,
            "wilaya": "16 - الجزائر",
            "buyer": "فاطمة",
            "phone": "0665987234"
        },
        {
            "category": "📱 هواتف ونقالات",
            "title": "أبحث عن iPhone 13 Pro Max",
            "description": "نظيف بطارية فوق 90%",
            "max_price": 100000,
            "wilaya": "31 - وهران",
            "buyer": "كريم",
            "phone": "0775987234"
        }
    ]
    
    for i, req in enumerate(requests):
        req["id"] = i + 1
        req["price_f"] = f"{req['max_price']:,} دج" if req["max_price"] else "غير محدد"
    
    return requests

# ==========================================
# 11. تهيئة البيانات
# ==========================================
if not st.session_state.ads:
    st.session_state.ads = get_auto_ads()
    st.session_state.requests = get_auto_requests()
    st.session_state.last_update = datetime.now().strftime("%H:%M:%S")

# ==========================================
# 12. كاشف الجدية الذكي
# ==========================================
def serious_buyer_detector(message: str) -> bool:
    """كشف المشتري الجدي في جميع الفئات"""
    message_lower = message.lower()
    
    for category, keywords in SERIOUS_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message_lower:
                st.session_state.last_alert = {
                    'message': message,
                    'category': category,
                    'time': datetime.now().strftime("%H:%M:%S")
                }
                st.toast(f"🚨 مشتري جدي في {category}!", icon="💰")
                return True
    return False

# ==========================================
# 13. التصميم المتطور
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Cairo', 'Space Grotesk', sans-serif !important;
    direction: rtl;
    box-sizing: border-box;
}

.stApp {
    background: radial-gradient(circle at 20% 20%, #1a1a2a, #0a0a0f);
    color: #ffffff;
    min-height: 100vh;
}

/* ===== الشعار المتطور ===== */
.logo-container {
    text-align: center;
    padding: 20px;
    margin-bottom: 20px;
    position: relative;
}

.logo-main {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.5rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 8px;
    background: linear-gradient(90deg, #00ffff, #ff00ff, #ffff00, #00ffff);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientFlow 8s linear infinite;
    filter: drop-shadow(0 0 15px rgba(0,255,255,0.3));
}

@keyframes gradientFlow {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

.logo-sub {
    font-size: 1.1rem;
    color: #00ffff;
    letter-spacing: 4px;
    margin-top: -10px;
    animation: glow 2s ease-in-out infinite;
}

@keyframes glow {
    0%, 100% { text-shadow: 0 0 10px #00ffff; }
    50% { text-shadow: 0 0 20px #ff00ff; }
}

.badge-69 {
    display: inline-block;
    background: linear-gradient(135deg, #00ffff, #ff00ff);
    color: black;
    padding: 5px 20px;
    border-radius: 50px;
    font-weight: bold;
    font-size: 1.2rem;
    margin-top: 10px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

/* ===== بطاقة الإعلان ===== */
.hologram-card {
    background: rgba(20, 20, 30, 0.4);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0, 255, 255, 0.15);
    border-radius: 25px;
    padding: 18px;
    margin-bottom: 20px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    height: 100%;
}

.hologram-card:hover {
    border-color: #00ffff;
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 20px 30px rgba(0, 255, 255, 0.2);
}

/* ===== شارة الفئة ===== */
.category-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background: linear-gradient(135deg, #00ffff, #ff00ff);
    color: black;
    padding: 4px 12px;
    border-radius: 50px;
    font-size: 0.7rem;
    font-weight: bold;
    z-index: 10;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

/* ===== الصورة ===== */
.ad-image {
    width: 100%;
    height: 160px;
    object-fit: cover;
    border-radius: 20px;
    margin-bottom: 15px;
    border: 2px solid rgba(0, 255, 255, 0.2);
    transition: transform 0.3s ease;
}

.ad-image:hover {
    transform: scale(1.03);
}

/* ===== العنوان ===== */
.ad-title {
    color: #00ffff;
    font-size: 1.1rem;
    font-weight: bold;
    margin: 10px 0 5px;
    line-height: 1.4;
}

/* ===== السعر ===== */
.ad-price {
    color: #ff00ff;
    font-size: 1.5rem;
    font-weight: bold;
    margin: 8px 0;
    text-shadow: 0 0 10px rgba(255,0,255,0.3);
}

/* ===== الحالة ===== */
.ad-condition {
    display: inline-block;
    background: rgba(255,255,255,0.1);
    padding: 3px 12px;
    border-radius: 50px;
    font-size: 0.75rem;
    color: #aaa;
    border: 1px solid rgba(255,255,255,0.1);
}

/* ===== المواصفات ===== */
.ad-metadata {
    background: rgba(0, 255, 255, 0.03);
    border-radius: 15px;
    padding: 10px;
    margin: 12px 0;
    font-size: 0.75rem;
    color: #ddd;
    border: 1px solid rgba(0, 255, 255, 0.1);
    line-height: 1.8;
}

.metadata-item {
    display: inline-block;
    background: rgba(0,255,255,0.1);
    padding: 3px 8px;
    border-radius: 20px;
    margin: 2px;
    color: #00ffff;
    font-size: 0.7rem;
    border: 1px solid rgba(0,255,255,0.2);
}

/* ===== شارات ===== */
.wilaya-badge {
    display: inline-block;
    background: rgba(0,255,255,0.08);
    border: 1px solid #00ffff;
    border-radius: 30px;
    padding: 4px 10px;
    margin: 3px;
    color: #00ffff;
    font-size: 0.75rem;
    white-space: nowrap;
}

.seller-info {
    background: rgba(255,0,255,0.08);
    border: 1px solid #ff00ff;
    border-radius: 30px;
    padding: 8px 12px;
    margin: 12px 0;
    color: #ff00ff;
    font-size: 0.85rem;
    text-align: center;
    font-weight: 500;
}

/* ===== أزرار التواصل ===== */
.contact-buttons {
    display: flex;
    gap: 8px;
    margin-top: 15px;
}

.whatsapp-btn, .call-btn, .report-btn {
    flex: 1;
    padding: 10px 5px;
    border-radius: 15px;
    font-size: 0.85rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
    text-align: center;
    border: none;
}

.whatsapp-btn {
    background: #25D366;
    color: white;
}

.whatsapp-btn:hover {
    background: #128C7E;
    transform: scale(1.02);
    box-shadow: 0 5px 15px rgba(37, 211, 102, 0.3);
}

.call-btn {
    background: linear-gradient(90deg, #00ffff, #ff00ff);
    color: black;
}

.call-btn:hover {
    opacity: 0.9;
    transform: scale(1.02);
    box-shadow: 0 5px 15px rgba(255, 0, 255, 0.3);
}

.report-btn {
    background: rgba(255,0,0,0.1);
    border: 1px solid #ff4444;
    color: #ff4444;
    font-size: 0.75rem;
}

.report-btn:hover {
    background: rgba(255,0,0,0.2);
    transform: scale(1.02);
}

/* ===== بطاقة الطلب ===== */
.request-card {
    background: rgba(30, 20, 30, 0.4);
    border: 1px solid #ff00ff;
    border-radius: 25px;
    padding: 18px;
    margin-bottom: 15px;
    border-right: 5px solid #ff00ff;
}

/* ===== إحصائيات ===== */
.stat-card {
    background: rgba(20,20,30,0.5);
    border: 1px solid #00ffff;
    border-radius: 20px;
    padding: 15px;
    text-align: center;
    transition: transform 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0,255,255,0.15);
}

.stat-value {
    font-size: 2rem;
    color: #00ffff;
    font-weight: bold;
    font-family: 'Space Grotesk', monospace;
}

.stat-label {
    font-size: 0.85rem;
    color: white;
    margin-top: 5px;
}

/* ===== فلترة متقدمة ===== */
.filter-section {
    background: rgba(20,20,30,0.5);
    border: 1px solid #00ffff;
    border-radius: 50px;
    padding: 15px 20px;
    margin: 20px 0;
    backdrop-filter: blur(10px);
}

/* ===== أزرار التحكم ===== */
.stButton > button {
    background: linear-gradient(90deg, #00ffff, #ff00ff) !important;
    border: none !important;
    color: black !important;
    font-weight: bold !important;
    border-radius: 15px !important;
    padding: 12px 20px !important;
    font-size: 1rem !important;
    width: 100%;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 20px rgba(255, 0, 255, 0.3) !important;
}

/* ===== عداد الزوار ===== */
.live-counter {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background: rgba(0,0,0,0.9);
    border: 1px solid #00ffff;
    padding: 8px 15px;
    border-radius: 50px;
    z-index: 999;
    color: white;
    font-size: 0.85rem;
    backdrop-filter: blur(5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

/* ===== فقاعة الدردشة ===== */
.chat-bubble {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: linear-gradient(135deg, #00ffff, #ff00ff);
    width: 55px;
    height: 55px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 9999;
    animation: float 3s ease-in-out infinite;
    box-shadow: 0 10px 20px rgba(0,255,255,0.3);
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

.chat-bubble img {
    width: 28px;
    height: 28px;
    filter: brightness(0) invert(1);
}

/* ===== تنبيه الرادار ===== */
.radar-alert {
    background: rgba(255,0,0,0.15);
    border: 2px solid #ff00ff;
    border-radius: 20px;
    padding: 15px;
    margin: 15px 0;
    animation: alertPulse 1.5s infinite;
}

@keyframes alertPulse {
    0%, 100% { box-shadow: 0 0 20px #ff00ff; }
    50% { box-shadow: 0 0 40px #ff0000; }
}

/* ===== الفوتر ===== */
.footer {
    text-align: center;
    color: #666;
    font-size: 0.8rem;
    margin-top: 50px;
    padding: 20px;
    border-top: 1px solid #333;
    background: rgba(0,0,0,0.3);
    border-radius: 30px;
}

/* ===== تجاوب مع الجوال ===== */
@media screen and (max-width: 768px) {
    .logo-main { font-size: 2.2rem; }
    .stat-value { font-size: 1.5rem; }
    .ad-image { height: 130px; }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 14. دوال المساعدة
# ==========================================
def get_stats() -> Tuple[int, int, int]:
    """إحصائيات سريعة"""
    ads_count = len(st.session_state.ads)
    requests_count = len(st.session_state.requests)
    visitors = random.randint(50, 200)
    return ads_count, requests_count, visitors

def format_metadata(metadata_dict: dict) -> str:
    """تنسيق عرض المواصفات"""
    if not metadata_dict:
        return "لا توجد مواصفات"
    
    items = []
    labels = {
        "ram": "🫀 رام", "storage": "💾 تخزين", "color": "🎨 لون", "battery": "🔋 بطارية",
        "rooms": "🛏️ غرف", "surface": "📐 مساحة", "floor": "📍 طابق", "furnished": "🛋️ مفروش",
        "parking": "🅿️ موقف", "car_model": "🚗 سيارة", "part_number": "🔧 رقم القطعة",
        "year": "📅 سنة", "mileage": "📏 كم", "type": "🔨 نوع", "material": "🧵 خامة",
        "pieces": "📦 قطع", "tools_count": "🔨 أدوات", "brand": "🏷️ ماركة",
        "expiry": "⏳ صلاحية", "gender": "👤 جنس", "size": "📏 قياس"
    }
    
    for key, value in metadata_dict.items():
        label = labels.get(key, key)
        if isinstance(value, bool):
            value = "نعم" if value else "لا"
        items.append(f"{label}: {value}")
    
    return " • ".join(items)

def get_category_emoji(category: str) -> str:
    """استخراج الإيموجي من الفئة"""
    emoji_map = {
        "📱 هواتف": "📱",
        "🚗 قطع": "🚗",
        "🏠 عقارات": "🏠",
        "💄 تجميل": "💄",
        "🛋️ أثاث": "🛋️",
        "🔧 خردة": "🔧",
        "👕 ملابس": "👕",
        "🛠️ خدمات": "🛠️",
        "📦 أخرى": "📦"
    }
    
    for key, emoji in emoji_map.items():
        if key in category:
            return emoji
    return "📌"

# ==========================================
# 15. عرض الإعلانات
# ==========================================
def show_ads():
    """عرض الإعلانات مع فلترة متقدمة"""
    
    # فلترة
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("", placeholder="🔍 بحث في العناوين...")
    with col2:
        categories = ["الكل"] + [c for c in CATEGORIES if c != "الكل"]
        selected_category = st.selectbox("", categories, format_func=lambda x: x, key="cat_filter")
    with col3:
        price_range = st.selectbox("", ["الكل", "أقل من 10k", "10k-50k", "50k-100k", "100k-1M", "أكثر من 1M"], key="price_filter")
    
    col_a, col_b = st.columns(2)
    with col_a:
        selected_wilaya = st.selectbox("الولاية", ["الكل"] + list(WILAYAS), key="wilaya_filter")
    with col_b:
        condition = st.selectbox("الحالة", ["الكل"] + list(CONDITIONS), key="condition_filter")
    
    # فلترة الإعلانات
    filtered_ads = st.session_state.ads
    
    if selected_category != "الكل":
        filtered_ads = [ad for ad in filtered_ads if ad["category"] == selected_category]
    if selected_wilaya != "الكل":
        filtered_ads = [ad for ad in filtered_ads if ad["wilaya"] == selected_wilaya]
    if condition != "الكل":
        filtered_ads = [ad for ad in filtered_ads if ad["condition"] == condition]
    if search:
        filtered_ads = [ad for ad in filtered_ads if search.lower() in ad["title"].lower()]
    
    # فلترة حسب السعر
    if price_range != "الكل":
        if price_range == "أقل من 10k":
            filtered_ads = [ad for ad in filtered_ads if ad["price"] < 10000]
        elif price_range == "10k-50k":
            filtered_ads = [ad for ad in filtered_ads if 10000 <= ad["price"] <= 50000]
        elif price_range == "50k-100k":
            filtered_ads = [ad for ad in filtered_ads if 50000 <= ad["price"] <= 100000]
        elif price_range == "100k-1M":
            filtered_ads = [ad for ad in filtered_ads if 100000 <= ad["price"] <= 1000000]
        elif price_range == "أكثر من 1M":
            filtered_ads = [ad for ad in filtered_ads if ad["price"] > 1000000]
    
    # عرض عدد النتائج
    st.markdown(f"<p style='text-align:center; color:#888; font-size:0.9rem;'>عرض {len(filtered_ads)} إعلان من أصل {len(st.session_state.ads)}</p>", unsafe_allow_html=True)
    
    # عرض الإعلانات
    if filtered_ads:
        cols = st.columns(3)
        for i, ad in enumerate(filtered_ads):
            with cols[i % 3]:
                phone = ad["seller_phone"]
                whatsapp = phone[1:] if phone.startswith('0') else phone
                metadata_str = format_metadata(ad["metadata"])
                
                st.markdown(f"""
                <div class="hologram-card">
                    <div class="category-badge">{get_category_emoji(ad['category'])} {ad['category'].split()[1][:15]}</div>
                    <img src="{ad['image_url']}" class="ad-image" loading="lazy">
                    
                    <div class="ad-title">{ad['title'][:35]}</div>
                    <div class="ad-price">{ad['price_f']}</div>
                    <span class="ad-condition">{ad['condition']}</span>
                    
                    <div class="ad-metadata">
                        {metadata_str}
                    </div>
                    
                    <div style="margin: 8px 0;">
                        <span class="wilaya-badge">📍 {ad['wilaya'][:15]}</span>
                    </div>
                    
                    <div class="seller-info">
                        👤 {ad['seller_name'][:15]} • 📞 {ad['seller_phone']}
                    </div>
                    
                    <div class="contact-buttons">
                        <a href="https://wa.me/213{whatsapp}" target="_blank" class="whatsapp-btn">
                            واتساب
                        </a>
                        <a href="tel:{ad['seller_phone']}" class="call-btn">
                            اتصال
                        </a>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                        <span style="color:#666; font-size:0.65rem;">👁️ {ad.get('views', 0)} مشاهدة</span>
                        <span style="color:#666; font-size:0.65rem;">🕒 {ad.get('created_at', 'الآن')[:10]}</span>
                    </div>
                    
                    <button class="report-btn" onclick="alert('تم استلام البلاغ')">
                        🚨 تبليغ
                    </button>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("😕 لا توجد إعلانات تطابق بحثك")

# ==========================================
# 16. عرض طلبات المشتريين
# ==========================================
def show_requests():
    """عرض طلبات 'أبحث عن'"""
    st.markdown("### 🔍 طلبات المشتريين (أبحث عن)")
    
    if st.session_state.requests:
        cols = st.columns(2)
        for i, req in enumerate(st.session_state.requests):
            with cols[i % 2]:
                phone = req["phone"]
                whatsapp = phone[1:] if phone.startswith('0') else phone
                
                st.markdown(f"""
                <div class="request-card">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color:#ff00ff;">{req['category']}</span>
                        <span style="color:#00ffff;">💰 {req['price_f']}</span>
                    </div>
                    
                    <h4 style="color:white; margin:10px 0;">{req['title']}</h4>
                    <p style="color:#aaa;">{req['description']}</p>
                    
                    <div style="margin:10px 0;">
                        <span class="wilaya-badge">📍 {req['wilaya']}</span>
                        <span class="wilaya-badge">👤 {req['buyer']}</span>
                    </div>
                    
                    <div class="contact-buttons">
                        <a href="https://wa.me/213{whatsapp}" target="_blank" class="whatsapp-btn">
                            تواصل مع المشتري
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("لا توجد طلبات حالياً")

# ==========================================
# 17. إضافة إعلان جديد (ذكي)
# ==========================================
def add_new_ad():
    """إضافة إعلان جديد مع حقول متغيرة"""
    st.markdown("### 📢 إعلان جديد - وسيط")
    
    category = st.selectbox("ماذا تبيع؟", [c for c in CATEGORIES if c != "الكل"])
    
    with st.form("new_ad_form"):
        title = st.text_input("عنوان الإعلان *", placeholder="مثال: شقة للبيع في الجزائر")
        price = st.number_input("السعر (دج) *", min_value=0, step=1000)
        wilaya = st.selectbox("الولاية *", WILAYAS)
        condition = st.selectbox("الحالة *", CONDITIONS)
        
        # حقول متغيرة حسب الفئة
        metadata = {}
        
        if "عقارات" in category:
            col1, col2 = st.columns(2)
            with col1:
                metadata["rooms"] = st.number_input("عدد الغرف", 1, 20, 3)
                metadata["surface"] = st.text_input("المساحة", placeholder="120m²")
            with col2:
                metadata["floor"] = st.number_input("الطابق", 0, 20, 2)
                col_a, col_b = st.columns(2)
                with col_a:
                    metadata["furnished"] = st.checkbox("مفروش")
                with col_b:
                    metadata["parking"] = st.checkbox("موقف سيارة")
        
        elif "قطع غيار" in category:
            col1, col2 = st.columns(2)
            with col1:
                metadata["car_model"] = st.text_input("نوع السيارة", placeholder="رونو كليو 2")
                metadata["part_number"] = st.text_input("رقم القطعة", placeholder="K9K 702")
            with col2:
                metadata["year"] = st.text_input("سنة الصنع", placeholder="2005")
                metadata["mileage"] = st.text_input("عدد الكيلومترات", placeholder="120000 كم")
        
        elif "هواتف" in category:
            col1, col2 = st.columns(2)
            with col1:
                metadata["ram"] = st.selectbox("الرام", ["4GB", "6GB", "8GB", "12GB", "16GB"])
                metadata["storage"] = st.selectbox("التخزين", ["64GB", "128GB", "256GB", "512GB", "1TB"])
            with col2:
                metadata["color"] = st.text_input("اللون", placeholder="أسود")
                metadata["battery"] = st.text_input("حالة البطارية", placeholder="98%")
        
        elif "أثاث" in category:
            col1, col2 = st.columns(2)
            with col1:
                metadata["material"] = st.text_input("الخامة", placeholder="خشب, قماش...")
                metadata["color"] = st.text_input("اللون", placeholder="بيج")
            with col2:
                metadata["pieces"] = st.number_input("عدد القطع", 1, 20, 1)
        
        elif "خردة" in category:
            col1, col2 = st.columns(2)
            with col1:
                metadata["tools_count"] = st.number_input("عدد القطع", 1, 100, 1)
            with col2:
                metadata["type"] = st.text_input("النوع", placeholder="عدد يدوية")
        
        else:
            metadata["details"] = st.text_area("تفاصيل إضافية", height=80)
        
        # معلومات البائع
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            seller_name = st.text_input("اسم البائع *")
        with col2:
            seller_phone = st.text_input("رقم الهاتف *", placeholder="0555123456")
        
        description = st.text_area("وصف إضافي", height=80, placeholder="اكتب تفاصيل أكثر...")
        image_url = st.text_input("رابط الصورة (اختياري)", placeholder="https://...")
        
        if st.form_submit_button("🚀 نشر كوسيط", use_container_width=True):
            if title and price > 0 and seller_name and seller_phone:
                new_ad = {
                    "id": len(st.session_state.ads) + 1,
                    "category": category,
                    "title": title,
                    "price": price,
                    "price_f": f"{price:,} دج",
                    "wilaya": wilaya,
                    "condition": condition,
                    "metadata": metadata,
                    "seller_name": seller_name,
                    "seller_phone": seller_phone,
                    "description": description,
                    "image_url": image_url if image_url else "https://images.unsplash.com/photo-1591337676887-a217a6970a8a?w=400&h=300&fit=crop",
                    "views": 0
                }
                st.session_state.ads.append(new_ad)
                st.success("✅ تم نشر الإعلان بنجاح!")
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ يرجى ملء جميع الحقول المطلوبة")

# ==========================================
# 18. إضافة طلب شراء
# ==========================================
def add_buyer_request():
    """إضافة طلب 'أبحث عن'"""
    st.markdown("### 🔍 أبحث عن...")
    
    with st.form("request_form"):
        category = st.selectbox("ما الذي تبحث عنه؟", [c for c in CATEGORIES if c != "الكل"])
        title = st.text_input("عنوان الطلب *", placeholder="مثال: أبحث عن iPhone 13")
        description = st.text_area("الوصف", height=80, placeholder="اكتب تفاصيل ما تبحث عنه...")
        
        col1, col2 = st.columns(2)
        with col1:
            max_price = st.number_input("أقصى سعر (دج)", min_value=0, step=1000)
        with col2:
            wilaya = st.selectbox("الولاية", WILAYAS)
        
        col1, col2 = st.columns(2)
        with col1:
            buyer_name = st.text_input("اسمك *")
        with col2:
            buyer_phone = st.text_input("رقم الهاتف *", placeholder="0555123456")
        
        if st.form_submit_button("📢 نشر الطلب", use_container_width=True):
            if title and buyer_name and buyer_phone:
                new_request = {
                    "id": len(st.session_state.requests) + 1,
                    "category": category,
                    "title": title,
                    "description": description,
                    "max_price": max_price,
                    "price_f": f"{max_price:,} دج" if max_price else "غير محدد",
                    "wilaya": wilaya,
                    "buyer": buyer_name,
                    "phone": buyer_phone
                }
                st.session_state.requests.append(new_request)
                st.success("✅ تم نشر طلبك بنجاح!")
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ يرجى ملء جميع الحقول المطلوبة")

# ==========================================
# 19. رادار الجدية
# ==========================================
def show_radar():
    """عرض رادار الجدية"""
    if st.session_state.last_alert:
        st.markdown(f"""
        <div class="radar-alert">
            <h4 style="color:#ff00ff;">🚨 مشتري جدي!</h4>
            <p><b>الرسالة:</b> {st.session_state.last_alert['message']}</p>
            <p><b>الفئة:</b> {st.session_state.last_alert['category']}</p>
            <p><b>الوقت:</b> {st.session_state.last_alert['time']}</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 20. إحصائيات
# ==========================================
def show_stats():
    """عرض إحصائيات"""
    ads_count, requests_count, visitors = get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{ads_count}</div>
            <div class="stat-label">إعلان</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{requests_count}</div>
            <div class="stat-label">طلب</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">69</div>
            <div class="stat-label">ولاية</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{visitors}</div>
            <div class="stat-label">زائر</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 21. فقاعة الدردشة
# ==========================================
def show_chat():
    """فقاعة الدردشة"""
    st.markdown("""
    <div class="chat-bubble" onclick="window.open('https://wa.me/213555555555')">
        <img src="https://img.icons8.com/ios-filled/30/ffffff/speech-bubble.png">
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 22. الدالة الرئيسية
# ==========================================
def main():
    """الدالة الرئيسية - المحرك النهائي"""
    
    # عداد الزوار
    ads_count, requests_count, visitors = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span style="color:#00ffff;">●</span> {visitors} زائر • {ads_count} إعلان • {requests_count} طلب
    </div>
    """, unsafe_allow_html=True)
    
    # فقاعة الدردشة
    show_chat()
    
    # الشعار
    st.markdown("""
    <div class="logo-container">
        <div class="logo-main">RASSIM OS</div>
        <div class="logo-sub">ULTIMATE BROKER 2026</div>
        <div class="badge-69">🇩🇿 69 ولاية • وسيط ذكي</div>
    </div>
    """, unsafe_allow_html=True)
    
    # رادار الجدية
    show_radar()
    
    # آخر تحديث
    st.markdown(f"<p style='text-align:center; color:#666; font-size:0.8rem;'>آخر تحديث: {st.session_state.last_update}</p>", unsafe_allow_html=True)
    
    # إحصائيات
    show_stats()
    
    # تبويبات رئيسية
    tab1, tab2, tab3 = st.tabs(["🛒 السوق", "🔍 طلبات", "📢 إضافة"])
    
    with tab1:
        # أزرار التحكم
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 تحديث الإعلانات", use_container_width=True):
                st.session_state.ads = get_auto_ads()
                st.session_state.last_update = datetime.now().strftime("%H:%M:%S")
                st.rerun()
        with col2:
            if st.button("📊 ترتيب عشوائي", use_container_width=True):
                random.shuffle(st.session_state.ads)
                st.rerun()
        with col3:
            if st.button("🔍 فلترة متقدمة", use_container_width=True):
                pass
        
        st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
        
        # عرض الإعلانات
        show_ads()
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 تحديث الطلبات", use_container_width=True):
                st.session_state.requests = get_auto_requests()
                st.rerun()
        with col2:
            if st.button("➕ طلب جديد", use_container_width=True):
                st.session_state.show_request_form = True
        
        if st.session_state.show_request_form:
            add_buyer_request()
            if st.button("❌ إغلاق"):
                st.session_state.show_request_form = False
                st.rerun()
        
        show_requests()
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📢 إعلان جديد", use_container_width=True):
                st.session_state.show_form = True
        with col2:
            if st.button("🔍 طلب شراء", use_container_width=True):
                st.session_state.show_request_form = True
        
        if st.session_state.show_form:
            add_new_ad()
            if st.button("❌ إغلاق نموذج الإعلان"):
                st.session_state.show_form = False
                st.rerun()
    
    # تذييل
    st.markdown("""
    <div class="footer">
        <p>RASSIM OS ULTIMATE 2026 • منصة وسيط ذكي • جميع الحقوق محفوظة ©</p>
        <p style="font-size:0.7rem;">نظام وساطة متكامل - نلتزم بالقوانين الجزائرية</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 23. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()

