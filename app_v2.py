#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS ULTIMATE 2026
منصة وسيط بين الشاري والبائع - 69 ولاية
دخول حر بدون تسجيل - صور حقيقية
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
# 2. قائمة الولايات (69 ولاية)
# ==========================================
WILAYAS = [
    "16 - الجزائر", "31 - وهران", "25 - قسنطينة", "42 - تيبازة", "06 - بجاية",
    "19 - سطيف", "23 - عنابة", "13 - تلمسان", "09 - البليدة", "15 - تيزي وزو",
    "07 - بسكرة", "26 - المدية", "29 - معسكر", "35 - بومرداس", "41 - سوق أهراس",
    "47 - غرداية", "55 - توقرت", "57 - المغير", "58 - المنيع", "69 - عين الحجر"
]

# ==========================================
# 3. إعلانات تلقائية بالصور (12 إعلان)
# ==========================================
def get_auto_ads():
    """توليد إعلانات تلقائية"""
    phones = [
        {
            "name": "iPhone 15 Pro Max 512GB",
            "price": 225000,
            "img": "https://images.unsplash.com/photo-1696446701796-da61225697cc?w=400",
            "specs": "A17 Pro • 8GB RAM • 48MP • 4422mAh",
            "seller": "محمد من الجزائر",
            "seller_phone": "0555123456"
        },
        {
            "name": "Samsung S24 Ultra 512GB",
            "price": 185000,
            "img": "https://images.unsplash.com/photo-1707248545831-7e8c356f981e?w=400",
            "specs": "Snapdragon 8 Gen 3 • 12GB RAM • 200MP • 5000mAh",
            "seller": "أحمد من وهران",
            "seller_phone": "0666123456"
        },
        {
            "name": "Google Pixel 8 Pro 256GB",
            "price": 145000,
            "img": "https://images.unsplash.com/photo-1696429117066-e399580556f0?w=400",
            "specs": "Tensor G3 • 12GB RAM • 50MP • 5050mAh",
            "seller": "كريم من قسنطينة",
            "seller_phone": "0777123456"
        },
        {
            "name": "Xiaomi 14 Ultra 512GB",
            "price": 155000,
            "img": "https://images.unsplash.com/photo-1610433554474-76348234983c?w=400",
            "specs": "Snapdragon 8 Gen 3 • 16GB RAM • 50MP • 5300mAh",
            "seller": "سمير من تيبازة",
            "seller_phone": "0555987654"
        },
        {
            "name": "iPhone 13 Pro Max 256GB",
            "price": 115000,
            "img": "https://images.unsplash.com/photo-1633333008433-89948d3eb300?w=400",
            "specs": "A15 Bionic • 6GB RAM • 12MP • 4352mAh",
            "seller": "نوال من بجاية",
            "seller_phone": "0665987654"
        },
        {
            "name": "Samsung S23 Ultra 512GB",
            "price": 145000,
            "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
            "specs": "Snapdragon 8 Gen 2 • 12GB RAM • 200MP • 5000mAh",
            "seller": "ياسين من سطيف",
            "seller_phone": "0775987654"
        },
        {
            "name": "Nothing Phone 2 256GB",
            "price": 85000,
            "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
            "specs": "Snapdragon 8+ Gen 1 • 12GB RAM • 50MP • 4700mAh",
            "seller": "أمينة من عنابة",
            "seller_phone": "0555123987"
        },
        {
            "name": "OnePlus 12 512GB",
            "price": 130000,
            "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
            "specs": "Snapdragon 8 Gen 3 • 16GB RAM • 50MP • 5400mAh",
            "seller": "بلال من تلمسان",
            "seller_phone": "0666123987"
        },
        {
            "name": "Huawei P60 Pro 512GB",
            "price": 135000,
            "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
            "specs": "Snapdragon 8+ Gen 1 • 8GB RAM • 48MP • 4815mAh",
            "seller": "ليلى من البليدة",
            "seller_phone": "0777123987"
        },
        {
            "name": "iPhone 14 Pro Max 256GB",
            "price": 155000,
            "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
            "specs": "A16 Bionic • 6GB RAM • 48MP • 4323mAh",
            "seller": "عمر من تيزي وزو",
            "seller_phone": "0555876543"
        },
        {
            "name": "Samsung Z Fold 5 1TB",
            "price": 210000,
            "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
            "specs": "Snapdragon 8 Gen 2 • 12GB RAM • 50MP • 4400mAh",
            "seller": "سارة من بسكرة",
            "seller_phone": "0665876543"
        },
        {
            "name": "Xiaomi 13 Ultra 512GB",
            "price": 115000,
            "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
            "specs": "Snapdragon 8 Gen 2 • 12GB RAM • 50MP • 5000mAh",
            "seller": "خالد من المدية",
            "seller_phone": "0775876543"
        }
    ]
    
    sources = ["بائع محترف", "تاجر معتمد", "مستخدم جديد", "محل موثوق"]
    tags = ["🔥 عرض حي", "⚡ جديد", "⭐ مميز", "💰 فرصة", "🚀 كمية محدودة"]
    
    ads = []
    for i, phone in enumerate(phones):
        wilaya = random.choice(WILAYAS)
        source = random.choice(sources)
        tag = random.choice(tags)
        
        ads.append({
            "id": i + 1,
            "title": phone["name"],
            "price": phone["price"],
            "price_f": f"{phone['price']:,} دج",
            "wilaya": wilaya,
            "img": phone["img"],
            "source": source,
            "tag": tag,
            "specs": phone["specs"],
            "seller": phone["seller"],
            "seller_phone": phone["seller_phone"],
            "description": f"{phone['specs']} • البائع: {phone['seller']}"
        })
    return ads

# ==========================================
# 4. حفظ الإعلانات في جلسة المستخدم
# ==========================================
if 'ads' not in st.session_state:
    st.session_state.ads = get_auto_ads()
    st.session_state.last_update = datetime.now().strftime("%H:%M:%S")

# ==========================================
# 5. التصميم المتطور
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
    height: 200px;
    object-fit: cover;
    border-radius: 20px;
    margin-bottom: 15px;
    border: 1px solid rgba(0, 255, 255, 0.3);
    transition: transform 0.3s ease;
}

.ad-image:hover {
    transform: scale(1.02);
}

.ad-title {
    color: #00ffff;
    font-size: 1.3rem;
    font-weight: bold;
    margin: 10px 0;
}

.ad-price {
    color: #ff00ff;
    font-size: 1.8rem;
    font-weight: bold;
    margin: 10px 0;
}

.ad-specs {
    color: #aaa;
    font-size: 0.9rem;
    margin: 10px 0;
    padding: 10px;
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    line-height: 1.6;
}

.wilaya-badge {
    display: inline-block;
    background: rgba(0,255,255,0.1);
    border: 1px solid #00ffff;
    border-radius: 50px;
    padding: 5px 15px;
    margin: 5px;
    color: #00ffff;
    font-size: 0.9rem;
    white-space: nowrap;
}

.seller-info {
    background: rgba(255,0,255,0.1);
    border: 1px solid #ff00ff;
    border-radius: 50px;
    padding: 8px 15px;
    margin: 10px 0;
    color: #ff00ff;
    font-size: 1rem;
    text-align: center;
}

.contact-buttons {
    display: flex;
    gap: 10px;
    margin-top: 15px;
}

.whatsapp-btn {
    flex: 1;
    background: #25D366;
    color: white;
    border: none;
    border-radius: 15px;
    padding: 15px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.3s ease;
    text-decoration: none;
    display: inline-block;
    text-align: center;
}

.whatsapp-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #25D366;
}

.call-btn {
    flex: 1;
    background: linear-gradient(90deg, #00ffff, #ff00ff);
    color: black;
    border: none;
    border-radius: 15px;
    padding: 15px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.3s ease;
    text-decoration: none;
    display: inline-block;
    text-align: center;
}

.call-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #ff00ff;
}

.stat-card {
    background: rgba(20,20,30,0.5);
    border: 1px solid #00ffff;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
}

.stat-value {
    font-size: 2.5rem;
    color: #00ffff;
    font-weight: bold;
}

.stat-label {
    font-size: 1.1rem;
    color: white;
    margin-top: 5px;
}

.stButton > button {
    background: linear-gradient(90deg, #00ffff, #ff00ff) !important;
    border: none !important;
    color: black !important;
    font-weight: bold !important;
    border-radius: 15px !important;
    padding: 12px 25px !important;
    font-size: 1.1rem !important;
    width: 100%;
}

.live-counter {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background: rgba(0,0,0,0.7);
    border: 1px solid #00ffff;
    padding: 10px 20px;
    border-radius: 50px;
    z-index: 999;
    color: white;
    font-size: 0.9rem;
    backdrop-filter: blur(5px);
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
    box-shadow: 0 10px 20px rgba(0,255,255,0.3);
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.footer {
    text-align: center;
    color: #888;
    font-size: 0.9rem;
    margin-top: 50px;
    padding: 20px;
    border-top: 1px solid #333;
}

.filter-section {
    background: rgba(20,20,30,0.5);
    border: 1px solid #00ffff;
    border-radius: 50px;
    padding: 15px 25px;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 6. دوال المساعدة
# ==========================================
def get_stats():
    """إحصائيات سريعة"""
    ads_count = len(st.session_state.ads)
    visitors = random.randint(100, 300)  # محاكاة للزوار
    return ads_count, visitors

# ==========================================
# 7. عرض الإعلانات
# ==========================================
def show_ads():
    """عرض كل الإعلانات مع خيارات التواصل"""
    
    # فلترة حسب الولاية
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍", placeholder="ابحث عن هاتف...")
    with col2:
        selected_wilaya = st.selectbox("الولاية", ["الكل"] + WILAYAS)
    
    # فلترة الإعلانات
    filtered_ads = st.session_state.ads
    if selected_wilaya != "الكل":
        filtered_ads = [ad for ad in filtered_ads if ad["wilaya"] == selected_wilaya]
    if search:
        filtered_ads = [ad for ad in filtered_ads if search.lower() in ad["title"].lower()]
    
    # عرض الإعلانات في شبكة 3 أعمدة
    cols = st.columns(3)
    for i, ad in enumerate(filtered_ads):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="hologram-card">
                <div class="ad-tag">{ad['tag']}</div>
                <img src="{ad['img']}" class="ad-image">
                <div class="ad-title">{ad['title']}</div>
                <div class="ad-price">{ad['price_f']}</div>
                <div class="ad-specs">{ad['specs']}</div>
                
                <div style="margin: 10px 0;">
                    <span class="wilaya-badge">📍 {ad['wilaya']}</span>
                    <span class="wilaya-badge">👤 {ad['seller']}</span>
                </div>
                
                <div class="seller-info">
                    📞 {ad['seller_phone']}
                </div>
                
                <div class="contact-buttons">
                    <a href="https://wa.me/213{ad['seller_phone'][1:]}" target="_blank" class="whatsapp-btn">
                        📱 واتساب
                    </a>
                    <a href="tel:{ad['seller_phone']}" class="call-btn">
                        📞 اتصال
                    </a>
                </div>
                
                <p style="color: #888; font-size: 0.8rem; margin-top: 10px; text-align: center;">
                    وسيط: RASSIM OS • البائع: {ad['source']}
                </p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# 8. إضافة إعلان جديد
# ==========================================
def add_new_ad():
    """إضافة إعلان جديد من مستخدم"""
    with st.form("new_ad"):
        st.markdown("### 📢 إضافة إعلان جديد")
        
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("اسم المنتج *")
            price = st.number_input("السعر (دج) *", min_value=0, step=1000)
        with col2:
            wilaya = st.selectbox("الولاية *", WILAYAS)
            seller_name = st.text_input("اسم البائع *")
        
        seller_phone = st.text_input("رقم الهاتف *", placeholder="مثال: 0555123456")
        specs = st.text_area("المواصفات", placeholder="اكتب مواصفات الهاتف...")
        
        img_url = st.text_input("رابط الصورة", placeholder="https://... (اختياري)")
        
        if st.form_submit_button("🚀 نشر الإعلان", use_container_width=True):
            if title and price > 0 and seller_name and seller_phone:
                new_ad = {
                    "id": len(st.session_state.ads) + 1,
                    "title": title,
                    "price": price,
                    "price_f": f"{price:,} دج",
                    "wilaya": wilaya,
                    "img": img_url if img_url else "https://images.unsplash.com/photo-1591337676887-a217a6970a8a?w=400",
                    "source": "مستخدم جديد",
                    "tag": "🆕 جديد",
                    "specs": specs if specs else "مواصفات غير محددة",
                    "seller": seller_name,
                    "seller_phone": seller_phone
                }
                st.session_state.ads.append(new_ad)
                st.success("✅ تم نشر الإعلان بنجاح!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ يرجى ملء جميع الحقول المطلوبة")

# ==========================================
# 9. إحصائيات سريعة
# ==========================================
def show_stats():
    """عرض إحصائيات سريعة"""
    ads_count, visitors = get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{ads_count}</div>
            <div class="stat-label">إعلان نشط</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">69</div>
            <div class="stat-label">ولاية</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{visitors}</div>
            <div class="stat-label">زائر الآن</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{len(st.session_state.ads) * 2}</div>
            <div class="stat-label">مشتري محتمل</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 10. واجهة الدردشة
# ==========================================
def show_chat():
    """فقاعة الدردشة"""
    st.markdown("""
    <div class="chat-bubble" onclick="window.open('https://wa.me/213555555555')">
        <img src="https://img.icons8.com/ios-filled/30/ffffff/speech-bubble.png" width="30">
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 11. الدالة الرئيسية
# ==========================================
def main():
    # عداد الزوار
    ads_count, visitors = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span style="color:#00ffff;">●</span> {visitors} زائر • {ads_count} إعلان • {len(WILAYAS)} ولاية
    </div>
    """, unsafe_allow_html=True)
    
    # فقاعة الدردشة
    show_chat()
    
    # الشعار
    st.markdown('<div class="logo">RASSIM OS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">⚡ وسيط بين الشاري والبائع • 69 ولاية جزائرية</div>', unsafe_allow_html=True)
    
    # آخر تحديث
    st.markdown(f"""
    <p style="text-align:center; color:#666; font-size:0.9rem;">
        آخر تحديث: {st.session_state.last_update}
    </p>
    """, unsafe_allow_html=True)
    
    # إحصائيات
    show_stats()
    
    # أزرار التحكم
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 تحديث الإعلانات", use_container_width=True):
            st.session_state.ads = get_auto_ads()
            st.session_state.last_update = datetime.now().strftime("%H:%M:%S")
            st.rerun()
    with col2:
        if st.button("📢 إعلان جديد", use_container_width=True):
            st.session_state.show_form = True
    with col3:
        if st.button("🎲 ترتيب عشوائي", use_container_width=True):
            random.shuffle(st.session_state.ads)
            st.rerun()
    
    # نموذج إضافة إعلان
    if st.session_state.get('show_form', False):
        add_new_ad()
        if st.button("❌ إغلاق النموذج"):
            st.session_state.show_form = False
            st.rerun()
    
    # خط فاصل
    st.markdown("---")
    
    # عرض الإعلانات
    show_ads()
    
    # تذييل
    st.markdown("""
    <div class="footer">
        RASSIM OS • منصة وسيط بين الشاري والبائع • جميع الحقوق محفوظة © 2026<br>
        نلتزم بالقوانين الجزائرية • للتواصل: rassim.os@dz
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 12. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()

