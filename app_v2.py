#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS ULTIMATE 2026
نسخة مجانية - دخول حر بدون تسجيل - إعلانات تلقائية بالصور
69 ولاية جزائرية
"""

import streamlit as st
import sqlite3
import random
import time
import os
import base64
from datetime import datetime
from pathlib import Path

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS • 69 ولاية",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# 2. إنشاء مجلد للصور
# ==========================================
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

# ==========================================
# 3. قائمة الولايات (69 ولاية)
# ==========================================
WILAYAS = [
    "16 - الجزائر", "31 - وهران", "25 - قسنطينة", "42 - تيبازة", "06 - بجاية",
    "19 - سطيف", "23 - عنابة", "13 - تلمسان", "09 - البليدة", "15 - تيزي وزو",
    "07 - بسكرة", "26 - المدية", "29 - معسكر", "35 - بومرداس", "41 - سوق أهراس",
    "47 - غرداية", "55 - توقرت", "57 - المغير", "58 - المنيع", "69 - عين الحجر"
]

# ==========================================
# 4. قاعدة بيانات بسيطة
# ==========================================
DB = Path("rassim_os.db")

@st.cache_resource
def get_connection():
    return sqlite3.connect(str(DB), check_same_thread=False)

conn = get_connection()

def init_db():
    cursor = conn.cursor()
    
    # جدول الإعلانات - بدون أعمدة معقدة
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
            date TEXT DEFAULT CURRENT_TIMESTAMP,
            image_url TEXT
        )
    """)
    
    conn.commit()

init_db()

# ==========================================
# 5. إعلانات تلقائية بالصور
# ==========================================
def get_auto_ads():
    """توليد إعلانات تلقائية"""
    phones = [
        {
            "name": "iPhone 15 Pro Max 512GB",
            "price": 225000,
            "img": "https://images.unsplash.com/photo-1696446701796-da61225697cc?w=400",
            "specs": "A17 Pro • 8GB • 48MP • 4422mAh"
        },
        {
            "name": "Samsung S24 Ultra 512GB",
            "price": 185000,
            "img": "https://images.unsplash.com/photo-1707248545831-7e8c356f981e?w=400",
            "specs": "Snapdragon 8 Gen 3 • 12GB • 200MP • 5000mAh"
        },
        {
            "name": "Google Pixel 8 Pro 256GB",
            "price": 145000,
            "img": "https://images.unsplash.com/photo-1696429117066-e399580556f0?w=400",
            "specs": "Tensor G3 • 12GB • 50MP • 5050mAh"
        },
        {
            "name": "Xiaomi 14 Ultra 512GB",
            "price": 155000,
            "img": "https://images.unsplash.com/photo-1610433554474-76348234983c?w=400",
            "specs": "Snapdragon 8 Gen 3 • 16GB • 50MP • 5300mAh"
        },
        {
            "name": "iPhone 13 Pro Max 256GB",
            "price": 115000,
            "img": "https://images.unsplash.com/photo-1633333008433-89948d3eb300?w=400",
            "specs": "A15 Bionic • 6GB • 12MP • 4352mAh"
        },
        {
            "name": "Samsung S23 Ultra 512GB",
            "price": 145000,
            "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
            "specs": "Snapdragon 8 Gen 2 • 12GB • 200MP • 5000mAh"
        },
        {
            "name": "Nothing Phone 2 256GB",
            "price": 85000,
            "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
            "specs": "Snapdragon 8+ Gen 1 • 12GB • 50MP • 4700mAh"
        },
        {
            "name": "OnePlus 12 512GB",
            "price": 130000,
            "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
            "specs": "Snapdragon 8 Gen 3 • 16GB • 50MP • 5400mAh"
        },
        {
            "name": "Huawei P60 Pro 512GB",
            "price": 135000,
            "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
            "specs": "Snapdragon 8+ Gen 1 • 8GB • 48MP • 4815mAh"
        },
    ]
    
    sources = ["واد كنيس", "فيسبوك ماركت", "مجموعة RASSIM", "تاجر معتمد"]
    tags = ["🔥 عرض حي", "⚡ جديد", "⭐ مميز", "💰 فرصة", "🚀 كمية محدودة"]
    
    auto_ads = []
    for i, phone in enumerate(phones * 2):  # تكرار للحصول على 18 إعلان
        if len(auto_ads) >= 18:
            break
        wilaya = random.choice(WILAYAS)
        auto_ads.append({
            "id": i,
            "title": phone["name"],
            "price": phone["price"],
            "price_f": f"{phone['price']:,} دج",
            "wilaya": wilaya,
            "img": phone["img"],
            "source": random.choice(sources),
            "tag": random.choice(tags),
            "specs": phone["specs"],
            "phone_num": f"0555{random.randint(1000,9999)}"
        })
    return auto_ads

# ==========================================
# 6. إضافة الإعلانات التلقائية لقاعدة البيانات
# ==========================================
def seed_ads():
    """إضافة الإعلانات التلقائية"""
    ads = get_auto_ads()
    cursor = conn.cursor()
    count = 0
    
    for ad in ads:
        # التحقق من عدم التكرار
        existing = cursor.execute(
            "SELECT id FROM ads WHERE title=? AND price=?", 
            (ad["title"], ad["price"])
        ).fetchone()
        
        if not existing:
            cursor.execute("""
                INSERT INTO ads (title, price, phone, wilaya, description, category, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                ad["title"], ad["price"], ad["phone_num"], ad["wilaya"],
                f"{ad['specs']} • {ad['source']} • {ad['tag']}",
                "أخرى", ad["img"]
            ))
            count += 1
    
    conn.commit()
    return count

# ==========================================
# 7. التصميم
# ==========================================
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

.logo {
    font-size: 3.5rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00ffff, #ff00ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 20px;
    animation: shine 3s linear infinite;
}

@keyframes shine {
    to { background-position: 200% center; }
}

.subtitle {
    text-align: center;
    color: #00ffff;
    font-size: 1.2rem;
    margin-top: -10px;
    margin-bottom: 20px;
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

.ad-title {
    color: #00ffff;
    font-size: 1.2rem;
    font-weight: bold;
    margin: 10px 0;
}

.ad-price {
    color: #ff00ff;
    font-size: 1.5rem;
    font-weight: bold;
}

.ad-specs {
    color: #aaa;
    font-size: 0.8rem;
    margin: 10px 0;
    padding: 5px;
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
}

.wilaya-badge {
    display: inline-block;
    background: rgba(0,255,255,0.1);
    border: 1px solid #00ffff;
    border-radius: 50px;
    padding: 5px 10px;
    margin: 2px;
    color: #00ffff;
    font-size: 0.8rem;
}

.stat-card {
    background: rgba(20,20,30,0.5);
    border: 1px solid #00ffff;
    border-radius: 15px;
    padding: 15px;
    text-align: center;
}

.stat-value {
    font-size: 2rem;
    color: #00ffff;
    font-weight: bold;
}

.stButton > button {
    background: linear-gradient(90deg, #00ffff, #ff00ff) !important;
    border: none !important;
    color: black !important;
    font-weight: bold !important;
    border-radius: 10px !important;
    width: 100%;
}

.whatsapp-btn {
    background: #25D366 !important;
    color: white !important;
}

.call-btn {
    background: transparent !important;
    border: 1px solid #00ffff !important;
    color: #00ffff !important;
}

.live-counter {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background: rgba(0,0,0,0.7);
    border: 1px solid #00ffff;
    padding: 8px 15px;
    border-radius: 50px;
    z-index: 999;
    color: white;
}

.chat-bubble {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: linear-gradient(135deg, #00ffff, #ff00ff);
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 9999;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.footer {
    text-align: center;
    color: #666;
    font-size: 0.8rem;
    margin-top: 50px;
    padding: 20px;
    border-top: 1px solid #333;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 8. دوال المساعدة
# ==========================================
def get_stats():
    """إحصائيات سريعة"""
    try:
        ads = conn.execute("SELECT COUNT(*) FROM ads WHERE status='active'").fetchone()[0]
        visitors = random.randint(50, 200)  # محاكاة للزوار
        return ads, visitors
    except:
        return 0, 0

# ==========================================
# 9. عرض الإعلانات
# ==========================================
def show_ads():
    """عرض كل الإعلانات"""
    
    # إعلانات تلقائية
    auto_ads = get_auto_ads()
    
    st.markdown("## 🔥 أحدث العروض في 69 ولاية")
    
    cols = st.columns(3)
    for i, ad in enumerate(auto_ads):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="hologram-card">
                <div class="ad-tag">{ad['tag']}</div>
                <img src="{ad['img']}" class="ad-image">
                <div class="ad-title">{ad['title']}</div>
                <div class="ad-price">{ad['price_f']}</div>
                <div class="ad-specs">{ad['specs']}</div>
                <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                    <span class="wilaya-badge">📍 {ad['wilaya']}</span>
                    <span class="wilaya-badge">🌐 {ad['source']}</span>
                </div>
                <div style="display: flex; gap: 5px;">
                    <a href="https://wa.me/{ad['phone_num']}" style="flex:1; text-decoration:none;">
                        <button class="whatsapp-btn" style="width:100%; padding:8px; border:none; border-radius:10px;">📱 واتساب</button>
                    </a>
                    <a href="tel:{ad['phone_num']}" style="flex:1; text-decoration:none;">
                        <button class="call-btn" style="width:100%; padding:8px; border:none; border-radius:10px;">📞 اتصال</button>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # إعلانات من قاعدة البيانات (إذا وجدت)
    db_ads = conn.execute("SELECT * FROM ads WHERE status='active' ORDER BY date DESC").fetchall()
    
    if db_ads:
        st.markdown("## 📢 إعلانات المستخدمين")
        cols = st.columns(3)
        for i, ad in enumerate(db_ads[:6]):
            with cols[i % 3]:
                img_url = ad[10] if len(ad) > 10 else "https://via.placeholder.com/400x300?text=صورة"
                st.markdown(f"""
                <div class="hologram-card">
                    <img src="{img_url}" class="ad-image">
                    <div class="ad-title">{ad[1][:30]}</div>
                    <div class="ad-price">{ad[2]:,} دج</div>
                    <div style="margin: 10px 0;">
                        <span class="wilaya-badge">📍 {ad[4]}</span>
                    </div>
                    <div style="display: flex; gap: 5px;">
                        <a href="https://wa.me/{ad[3]}" style="flex:1;">
                            <button class="whatsapp-btn">📱</button>
                        </a>
                        <a href="tel:{ad[3]}" style="flex:1;">
                            <button class="call-btn">📞</button>
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# 10. واجهة الدردشة
# ==========================================
def show_chat():
    """فقاعة الدردشة"""
    st.markdown("""
    <div class="chat-bubble" onclick="window.open('https://wa.me/213555555555')">
        <img src="https://img.icons8.com/ios-filled/30/ffffff/speech-bubble.png" width="25">
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 11. الدالة الرئيسية
# ==========================================
def main():
    # عداد الزوار
    ads, visitors = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span style="color:#00ffff;">●</span> {visitors} زائر • {ads} إعلان
    </div>
    """, unsafe_allow_html=True)
    
    # فقاعة الدردشة
    show_chat()
    
    # الشعار
    st.markdown('<div class="logo">RASSIM OS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">⚡ 69 ولاية جزائرية • دخول حر بدون تسجيل</div>', unsafe_allow_html=True)
    
    # إحصائيات سريعة
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{ads}</div><div>إعلان نشط</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-value">69</div><div>ولاية</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{visitors}</div><div>زائر الآن</div></div>', unsafe_allow_html=True)
    
    # زر إضافة إعلانات
    if st.button("🚀 تحديث الإعلانات التلقائية", use_container_width=True):
        count = seed_ads()
        if count > 0:
            st.success(f"✅ تمت إضافة {count} إعلان جديد!")
            time.sleep(1)
            st.rerun()
        else:
            st.info("الإعلانات محدثة بالفعل")
    
    # عرض الإعلانات
    show_ads()
    
    # تذييل
    st.markdown("""
    <div class="footer">
        RASSIM OS • جميع الحقوق محفوظة © 2026<br>
        منصة وسيط تقني - نلتزم بالقوانين الجزائرية
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 12. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()
