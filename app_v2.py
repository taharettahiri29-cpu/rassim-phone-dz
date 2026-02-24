#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS ULTIMATE 2026
منصة وسيط ذكي - 69 ولاية
نسخة مصححة بالكامل - صور واضحة - إعلانات متفرقة
"""

import streamlit as st
import random
import time
from datetime import datetime
from typing import Tuple, Dict, Any, List

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS • 69 ولاية",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# 2. قائمة الفئات
# ==========================================
CATEGORIES: Tuple[str, ...] = (
    "الكل",
    "📱 هواتف",
    "🚗 سيارات",
    "🏠 عقارات",
    "🛋️ أثاث",
    "👕 ملابس",
    "🔧 أدوات",
    "📦 أخرى"
)

# ==========================================
# 3. قائمة الولايات
# ==========================================
WILAYAS: Tuple[str, ...] = (
    "16 - الجزائر", "31 - وهران", "25 - قسنطينة", "42 - تيبازة", "06 - بجاية",
    "19 - سطيف", "23 - عنابة", "13 - تلمسان", "09 - البليدة", "15 - تيزي وزو",
    "07 - بسكرة", "26 - المدية", "29 - معسكر", "35 - بومرداس", "41 - سوق أهراس",
    "47 - غرداية", "55 - توقرت", "57 - المغير", "58 - المنيع", "69 - عين الحجر"
)

# ==========================================
# 4. إعلانات متنوعة مع صور حقيقية
# ==========================================
def get_ads() -> List[Dict[str, Any]]:
    """توليد إعلانات متنوعة"""
    
    ads = [
        # هواتف
        {
            "id": 1,
            "category": "📱 هواتف",
            "title": "iPhone 15 Pro Max 512GB",
            "price": 225000,
            "price_f": "225,000 دج",
            "wilaya": "16 - الجزائر",
            "condition": "جديد",
            "details": "A17 Pro • 8GB RAM • 48MP",
            "seller": "محمد",
            "phone": "0555123456",
            "image": "https://images.pexels.com/photos/20793078/pexels-photo-20793078.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"
        },
        {
            "id": 2,
            "category": "📱 هواتف",
            "title": "Samsung S24 Ultra",
            "price": 185000,
            "price_f": "185,000 دج",
            "wilaya": "31 - وهران",
            "condition": "ممتاز",
            "details": "Snapdragon 8 Gen 3 • 12GB RAM",
            "seller": "أحمد",
            "phone": "0666123456",
            "image": "https://images.pexels.com/photos/18508827/pexels-photo-18508827.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"
        },
        {
            "id": 3,
            "category": "📱 هواتف",
            "title": "Google Pixel 8 Pro",
            "price": 145000,
            "price_f": "145,000 دج",
            "wilaya": "25 - قسنطينة",
            "condition": "جديد",
            "details": "Tensor G3 • 12GB RAM",
            "seller": "كريم",
            "phone": "0777123456",
            "image": "https://images.pexels.com/photos/16475440/pexels-photo-16475440.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"
        },
        
        # سيارات
        {
            "id": 4,
            "category": "🚗 سيارات",
            "title": "رونو كليو 4 2019",
            "price": 1250000,
            "price_f": "1,250,000 دج",
            "wilaya": "42 - تيبازة",
            "condition": "ممتازة",
            "details": "ديزل • 90,000 كم • بحالة نظيفة",
            "seller": "علي",
            "phone": "0555987123",
            "image": "https://images.pexels.com/photos/1156684/pexels-photo-1156684.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"
        },
        {
            "id": 5,
            "category": "🚗 سيارات",
            "title": "هيونداي i10 2022",
            "price": 1850000,
            "price_f": "1,850,000 دج",
            "wilaya": "16 - الجزائر",
            "condition": "جديدة",
            "details": "بترول • 25,000 كم • ضمان",
            "seller": "ياسين",
            "phone": "0775987123",
            "image": "https://images.pexels.com/photos/1149831/pexels-photo-1149831.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"
        },
        
        # عقارات
        {
            "id": 6,
            "category": "🏠 عقارات",
            "title": "شقة F3 بئر مراد رايس",
            "price": 35000000,
            "price_f": "35,000,000 دج",
            "wilaya": "16 - الجزائر",
            "condition": "للبيع",
            "details": "3 غرف • 120م² • طابق 2 • مصعد",
            "seller": "نسرين",
            "phone": "0555876123",
            "image": "https://images.pexels.com/photos/2587054/pexels-photo-2587054.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"
        },
        {
            "id": 7,
            "category": "🏠 عقارات",
            "title": "محل تجاري للكراء",
            "price": 45000,
            "price_f": "45,000 دج/شهر",
            "wilaya": "31 - وهران",
            "condition": "للكراء",
            "details": "80م² • واجهة 10م • كهرباء وماء",
            "seller": "عبد الرحمان",
            "phone": "0665876123",
            "image": "https://images.pexels.com/photos/280222/pexels-photo-280222.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"
        },
        
        # أثاث
        {
            "id": 8,
            "category": "🛋️ أثاث",
            "title": "طقم صالون 5 قطع",
            "price": 65000,
            "price_f": "65,000 دج",
            "wilaya": "06 - بجاية",
            "condition": "جديد",
            "details": "قماش مخمل • لون بيج • 3 مقاعد + 2 كراسي",
            "seller": "سهام",
            "phone": "0555876345",
            "image": "https://images.pexels.com/photos/1866149/pexels-photo-1866149.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"
        },
        
        # ملابس
        {
            "id": 9,
            "category": "👕 ملابس",
            "title": "جاكيت شتوي رجالي",
            "price": 8500,
            "price_f": "8,500 دج",
            "wilaya": "19 - سطيف",
            "condition": "جديد",
            "details": "مقاس XL • صوف 100% • أسود",
            "seller": "عمار",
            "phone": "0555987456",
            "image": "https://images.pexels.com/photos/1082529/pexels-photo-1082529.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"
        },
        
        # أدوات
        {
            "id": 10,
            "category": "🔧 أدوات",
            "title": "شنطة عدة كهربائية",
            "price": 15000,
            "price_f": "15,000 دج",
            "wilaya": "47 - غرداية",
            "condition": "مستعملة",
            "details": "25 قطعة • مثقاب + مفك + منشار",
            "seller": "فتحي",
            "phone": "0775987456",
            "image": "https://images.pexels.com/photos/128208/pexels-photo-128208.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"
        }
    ]
    
    return ads

# ==========================================
# 5. حفظ الإعلانات في الجلسة
# ==========================================
if 'ads' not in st.session_state:
    st.session_state.ads = get_ads()
    st.session_state.last_update = datetime.now().strftime("%H:%M:%S")

# ==========================================
# 6. التصميم النظيف
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');

* {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl;
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

.stApp {
    background: #0a0a1a;
    color: white;
}

/* ===== الشعار ===== */
.logo {
    font-size: 2.5rem;
    font-weight: 700;
    text-align: center;
    color: #00ffff;
    padding: 20px 10px;
    text-shadow: 0 0 10px #00ffff;
}

.subtitle {
    text-align: center;
    color: #ff00ff;
    font-size: 1rem;
    margin-top: -10px;
    margin-bottom: 20px;
}

/* ===== بطاقة الإعلان ===== */
.ad-card {
    background: #1a1a2a;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 20px;
    transition: transform 0.2s ease;
    border: 1px solid #333;
    height: 100%;
}

.ad-card:hover {
    transform: translateY(-3px);
    border-color: #00ffff;
}

/* ===== الصورة ===== */
.ad-image {
    width: 100%;
    height: 160px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 12px;
    border: 1px solid #333;
}

/* ===== العنوان ===== */
.ad-title {
    color: #00ffff;
    font-size: 1.1rem;
    font-weight: 600;
    margin: 8px 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ===== السعر ===== */
.ad-price {
    color: #ff00ff;
    font-size: 1.3rem;
    font-weight: 700;
    margin: 5px 0;
}

/* ===== الفئة والحالة ===== */
.ad-category {
    display: inline-block;
    background: #2a2a3a;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    color: #aaa;
    margin: 3px 0;
}

.ad-details {
    color: #aaa;
    font-size: 0.8rem;
    margin: 8px 0;
    line-height: 1.5;
    background: #222232;
    padding: 8px;
    border-radius: 8px;
}

/* ===== معلومات البائع ===== */
.seller-info {
    background: #222232;
    border-radius: 10px;
    padding: 8px 12px;
    margin: 10px 0;
    color: #ff00ff;
    font-size: 0.9rem;
    text-align: center;
}

/* ===== أزرار التواصل ===== */
.contact-buttons {
    display: flex;
    gap: 8px;
    margin-top: 10px;
}

.whatsapp-btn {
    flex: 1;
    background: #25D366;
    color: white;
    padding: 10px;
    border-radius: 10px;
    text-decoration: none;
    text-align: center;
    font-size: 0.9rem;
    transition: opacity 0.2s;
}

.whatsapp-btn:hover {
    opacity: 0.9;
}

.call-btn {
    flex: 1;
    background: #00ffff;
    color: black;
    padding: 10px;
    border-radius: 10px;
    text-decoration: none;
    text-align: center;
    font-size: 0.9rem;
    transition: opacity 0.2s;
}

.call-btn:hover {
    opacity: 0.9;
}

/* ===== إحصائيات ===== */
.stat-card {
    background: #1a1a2a;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
}

.stat-value {
    font-size: 1.8rem;
    color: #00ffff;
    font-weight: 700;
}

.stat-label {
    color: #aaa;
    font-size: 0.9rem;
    margin-top: 5px;
}

/* ===== أزرار التحكم ===== */
.stButton > button {
    background: #2a2a3a !important;
    border: 1px solid #444 !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 10px !important;
    font-size: 0.9rem !important;
    width: 100%;
}

.stButton > button:hover {
    border-color: #00ffff !important;
    color: #00ffff !important;
}

/* ===== فلترة ===== */
.stSelectbox > div > div {
    background: #1a1a2a !important;
    border: 1px solid #333 !important;
    color: white !important;
}

/* ===== عداد الزوار ===== */
.live-counter {
    position: fixed;
    bottom: 15px;
    left: 15px;
    background: #1a1a2a;
    border: 1px solid #333;
    padding: 6px 12px;
    border-radius: 20px;
    z-index: 999;
    color: white;
    font-size: 0.8rem;
}

/* ===== فقاعة الدردشة ===== */
.chat-bubble {
    position: fixed;
    bottom: 15px;
    right: 15px;
    background: #00ffff;
    width: 45px;
    height: 45px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 9999;
    box-shadow: 0 2px 10px #00ffff;
}

.chat-bubble img {
    width: 22px;
    height: 22px;
    filter: brightness(0);
}

/* ===== تذييل ===== */
.footer {
    text-align: center;
    color: #666;
    font-size: 0.8rem;
    margin-top: 40px;
    padding: 15px;
    border-top: 1px solid #333;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 7. دوال المساعدة
# ==========================================
def get_stats() -> Tuple[int, int]:
    """إحصائيات"""
    ads_count = len(st.session_state.ads)
    visitors = random.randint(30, 100)
    return ads_count, visitors

# ==========================================
# 8. عرض الإعلانات
# ==========================================
def show_ads():
    """عرض الإعلانات"""
    
    # فلترة
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("", placeholder="🔍 بحث...")
    with col2:
        categories = ["الكل"] + [c for c in CATEGORIES if c != "الكل"]
        selected_cat = st.selectbox("", categories)
    with col3:
        selected_wilaya = st.selectbox("", ["كل الولايات"] + list(WILAYAS))
    
    # فلترة الإعلانات
    filtered_ads = st.session_state.ads
    if selected_cat != "الكل":
        filtered_ads = [ad for ad in filtered_ads if ad["category"] == selected_cat]
    if selected_wilaya != "كل الولايات":
        filtered_ads = [ad for ad in filtered_ads if ad["wilaya"] == selected_wilaya]
    if search:
        filtered_ads = [ad for ad in filtered_ads if search.lower() in ad["title"].lower()]
    
    # عرض النتائج
    st.markdown(f"<p style='text-align:center; color:#666;'>عرض {len(filtered_ads)} إعلان</p>", unsafe_allow_html=True)
    
    # شبكة الإعلانات
    cols = st.columns(3)
    for i, ad in enumerate(filtered_ads):
        with cols[i % 3]:
            phone = ad["phone"]
            whatsapp = phone[1:] if phone.startswith('0') else phone
            
            st.markdown(f"""
            <div class="ad-card">
                <img src="{ad['image']}" class="ad-image" loading="lazy">
                <div class="ad-title">{ad['title']}</div>
                <div class="ad-price">{ad['price_f']}</div>
                <div style="margin: 5px 0;">
                    <span class="ad-category">{ad['category']}</span>
                    <span class="ad-category">{ad['wilaya'][:12]}</span>
                </div>
                <div class="ad-details">{ad['details']}</div>
                <div class="seller-info">
                    👤 {ad['seller']} • 📞 {ad['phone']}
                </div>
                <div class="contact-buttons">
                    <a href="https://wa.me/213{whatsapp}" target="_blank" class="whatsapp-btn">📱 واتساب</a>
                    <a href="tel:{ad['phone']}" class="call-btn">📞 اتصال</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# 9. إحصائيات
# ==========================================
def show_stats():
    """عرض إحصائيات"""
    ads_count, visitors = get_stats()
    
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
            <div class="stat-value">69</div>
            <div class="stat-label">ولاية</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{visitors}</div>
            <div class="stat-label">زائر</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{ads_count * 2}</div>
            <div class="stat-label">مشاهدة</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 10. فقاعة الدردشة
# ==========================================
def show_chat():
    """فقاعة الدردشة"""
    st.markdown("""
    <div class="chat-bubble" onclick="window.open('https://wa.me/213555555555')">
        <img src="https://img.icons8.com/ios-filled/30/000000/speech-bubble.png">
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 11. إضافة إعلان جديد
# ==========================================
def add_new_ad():
    """إضافة إعلان جديد"""
    st.markdown("### 📢 إعلان جديد")
    
    with st.form("new_ad"):
        title = st.text_input("العنوان *")
        price = st.number_input("السعر *", min_value=0, step=1000)
        category = st.selectbox("الفئة", [c for c in CATEGORIES if c != "الكل"])
        wilaya = st.selectbox("الولاية", WILAYAS)
        details = st.text_area("التفاصيل")
        seller = st.text_input("اسم البائع *")
        phone = st.text_input("رقم الهاتف *", placeholder="0555123456")
        image = st.text_input("رابط الصورة", placeholder="https://...")
        
        if st.form_submit_button("نشر", use_container_width=True) and title and price > 0 and seller and phone:
            new_ad = {
                "id": len(st.session_state.ads) + 1,
                "category": category,
                "title": title,
                "price": price,
                "price_f": f"{price:,} دج",
                "wilaya": wilaya,
                "condition": "جديد",
                "details": details,
                "seller": seller,
                "phone": phone,
                "image": image if image else "https://images.pexels.com/photos/1591337676887-a217a6970a8a?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"
            }
            st.session_state.ads.append(new_ad)
            st.success("✅ تم النشر!")
            st.balloons()
            time.sleep(1)
            st.rerun()
        elif not title or not seller or not phone:
            st.error("❌ املأ الحقول المطلوبة")

# ==========================================
# 12. الدالة الرئيسية
# ==========================================
def main():
    """الدالة الرئيسية"""
    
    # عداد الزوار
    ads_count, visitors = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span style="color:#00ffff;">●</span> {visitors} زائر • {ads_count} إعلان
    </div>
    """, unsafe_allow_html=True)
    
    # فقاعة الدردشة
    show_chat()
    
    # الشعار
    st.markdown('<div class="logo">⚡ RASSIM OS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">69 ولاية • وسيط ذكي</div>', unsafe_allow_html=True)
    
    # آخر تحديث
    st.markdown(f"<p style='text-align:center; color:#666; font-size:0.8rem;'>آخر تحديث: {st.session_state.last_update}</p>", unsafe_allow_html=True)
    
    # إحصائيات
    show_stats()
    
    # أزرار
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 تحديث", use_container_width=True):
            random.shuffle(st.session_state.ads)
            st.session_state.last_update = datetime.now().strftime("%H:%M:%S")
            st.rerun()
    with col2:
        if st.button("📢 إعلان جديد", use_container_width=True):
            st.session_state.show_form = True
    with col3:
        if st.button("🔍 بحث متقدم", use_container_width=True):
            pass
    
    # نموذج إضافة إعلان
    if st.session_state.get('show_form', False):
        add_new_ad()
        if st.button("❌ إغلاق"):
            st.session_state.show_form = False
            st.rerun()
    
    st.markdown("<hr style='border-color:#333; margin:20px 0;'>", unsafe_allow_html=True)
    
    # عرض الإعلانات
    show_ads()
    
    # تذييل
    st.markdown("""
    <div class="footer">
        RASSIM OS 2026 • منصة وسيط ذكي
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 13. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()

