#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS ULTIMATE 2026
نظام السوق العكسي - المشتري يبحث والبائع يجد
69 ولاية جزائرية
"""

import streamlit as st
import random
import time
import json
from datetime import datetime
from typing import Tuple, Dict, Any, List

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS • السوق العكسي",
    page_icon="🎯",
    layout="wide"
)

# ==========================================
# 2. قائمة الولايات
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
    "39 - الوادي", "40 - خنشلة", "43 - ميلة", "44 - عين الدفلى", "45 - النعامة",
    "46 - عين تموشنت", "48 - غليزان", "49 - تيميمون", "50 - برج باجي مختار",
    "51 - أولاد جلال", "52 - بني عباس", "53 - عين صالح", "54 - عين قزام"
)

# ==========================================
# 3. قائمة الفئات
# ==========================================
CATEGORIES: Tuple[str, ...] = (
    "🚗 قطع غيار سيارات",
    "🔧 خردة وأدوات",
    "🏠 عقارات",
    "📱 هواتف",
    "🛋️ أثاث",
    "👕 ملابس",
    "🛠️ خدمات",
    "📦 أخرى"
)

# ==========================================
# 4. طلبات المشتريين
# ==========================================
def get_sample_requests() -> List[Dict[str, Any]]:
    """طلبات تجريبية"""
    return [
        {
            "id": 1,
            "title": "محرك رونو كليو 2 ديزل 2005",
            "category": "🚗 قطع غيار سيارات",
            "wilaya": "16 - الجزائر",
            "buyer": "ناصر",
            "phone": "0555123456",
            "date": "2026-02-24 14:30",
            "status": "نشط",
            "offers": 3
        },
        {
            "id": 2,
            "title": "كراء شقة غرفتين + صالون في فوكة",
            "category": "🏠 عقارات",
            "wilaya": "42 - تيبازة",
            "buyer": "فاطمة",
            "phone": "0666123456",
            "date": "2026-02-24 13:15",
            "status": "نشط",
            "offers": 2
        },
        {
            "id": 3,
            "title": "بطارية iPhone 13 Pro Max أصلية",
            "category": "📱 هواتف",
            "wilaya": "31 - وهران",
            "buyer": "كريم",
            "phone": "0777123456",
            "date": "2026-02-24 12:00",
            "status": "نشط",
            "offers": 5
        },
        {
            "id": 4,
            "title": "طقم صالون 4 قطع مستعمل بحالة جيدة",
            "category": "🛋️ أثاث",
            "wilaya": "25 - قسنطينة",
            "buyer": "سهام",
            "phone": "0555987123",
            "date": "2026-02-24 11:30",
            "status": "نشط",
            "offers": 1
        },
        {
            "id": 5,
            "title": "عدد كهربائية (مثقاب + منشار + صاروخ)",
            "category": "🔧 خردة وأدوات",
            "wilaya": "19 - سطيف",
            "buyer": "عمار",
            "phone": "0665987123",
            "date": "2026-02-24 10:45",
            "status": "نشط",
            "offers": 4
        }
    ]

# ==========================================
# 5. حفظ البيانات في الجلسة
# ==========================================
if 'requests' not in st.session_state:
    st.session_state.requests = get_sample_requests()
    st.session_state.last_update = datetime.now().strftime("%H:%M:%S")

# ==========================================
# 6. التصميم المتطور
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');

* {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl;
    box-sizing: border-box;
}

.stApp {
    background: linear-gradient(135deg, #0a0a1a, #1a1a2a);
    color: white;
}

/* ===== الشعار ===== */
.logo {
    font-size: 3rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #00ffff, #ff00ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 20px;
}

.subtitle {
    text-align: center;
    color: #888;
    font-size: 1.1rem;
    margin-top: -10px;
}

/* ===== قسم البحث العكسي ===== */
.search-section {
    background: linear-gradient(135deg, #1a1a2a, #2a2a3a);
    border-radius: 30px;
    padding: 30px;
    margin: 20px 0;
    border: 1px solid #00ffff;
    box-shadow: 0 10px 30px rgba(0,255,255,0.1);
}

.search-title {
    color: #00ffff;
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 20px;
    text-align: center;
}

.search-subtitle {
    color: #888;
    text-align: center;
    margin-bottom: 30px;
    font-size: 1.1rem;
}

/* ===== تأثير البحث ===== */
.search-animation {
    text-align: center;
    padding: 20px;
    background: #2a2a3a;
    border-radius: 20px;
    margin: 20px 0;
}

.search-progress {
    height: 10px;
    background: linear-gradient(90deg, #00ffff, #ff00ff);
    border-radius: 10px;
    animation: progress 2s ease-in-out infinite;
}

@keyframes progress {
    0% { width: 0%; opacity: 0.5; }
    50% { width: 100%; opacity: 1; }
    100% { width: 0%; opacity: 0.5; }
}

/* ===== بطاقة الطلب ===== */
.request-card {
    background: #1a1a2a;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 15px;
    border: 1px solid #333;
    transition: all 0.3s ease;
}

.request-card:hover {
    border-color: #00ffff;
    transform: translateX(-5px);
}

.request-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.request-category {
    background: #2a2a3a;
    padding: 5px 12px;
    border-radius: 50px;
    color: #00ffff;
    font-size: 0.85rem;
}

.request-status {
    background: #00aa00;
    padding: 5px 12px;
    border-radius: 50px;
    color: white;
    font-size: 0.85rem;
}

.request-title {
    color: white;
    font-size: 1.2rem;
    font-weight: bold;
    margin: 10px 0;
}

.request-details {
    display: flex;
    gap: 15px;
    color: #888;
    font-size: 0.9rem;
    margin: 10px 0;
}

.request-offers {
    background: #2a2a3a;
    padding: 5px 12px;
    border-radius: 50px;
    color: #ff00ff;
    font-size: 0.85rem;
    display: inline-block;
}

/* ===== بطاقة البائع ===== */
.seller-card {
    background: linear-gradient(135deg, #1a1a2a, #2a2a3a);
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 10px;
    border: 1px solid #ff00ff;
    animation: slideIn 0.5s ease;
}

@keyframes slideIn {
    from { transform: translateX(50px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.seller-name {
    color: #ff00ff;
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 5px;
}

.seller-contact {
    display: flex;
    gap: 10px;
    margin-top: 10px;
}

.seller-btn {
    flex: 1;
    background: #00ffff;
    color: black;
    padding: 8px;
    border-radius: 10px;
    text-decoration: none;
    text-align: center;
    font-size: 0.9rem;
    transition: opacity 0.2s;
}

.seller-btn:hover {
    opacity: 0.8;
}

/* ===== إحصائيات ===== */
.stat-card {
    background: #1a1a2a;
    border: 1px solid #333;
    border-radius: 15px;
    padding: 15px;
    text-align: center;
}

.stat-value {
    font-size: 2rem;
    color: #00ffff;
    font-weight: bold;
}

.stat-label {
    color: #888;
    font-size: 0.9rem;
}

/* ===== أزرار ===== */
.stButton > button {
    background: linear-gradient(135deg, #00ffff, #ff00ff) !important;
    border: none !important;
    color: black !important;
    font-weight: bold !important;
    border-radius: 15px !important;
    padding: 12px !important;
    font-size: 1rem !important;
    width: 100%;
    transition: transform 0.2s !important;
}

.stButton > button:hover {
    transform: scale(1.02) !important;
}

/* ===== عداد الزوار ===== */
.live-counter {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background: #1a1a2a;
    border: 1px solid #00ffff;
    padding: 8px 15px;
    border-radius: 50px;
    z-index: 999;
    color: white;
    font-size: 0.85rem;
}

/* ===== فقاعة الدردشة ===== */
.chat-bubble {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #00ffff;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 9999;
    box-shadow: 0 5px 20px #00ffff;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

/* ===== تذييل ===== */
.footer {
    text-align: center;
    color: #666;
    font-size: 0.8rem;
    margin-top: 40px;
    padding: 20px;
    border-top: 1px solid #333;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 7. دوال المساعدة
# ==========================================
def get_stats() -> Tuple[int, int, int]:
    """إحصائيات سريعة"""
    requests_count = len(st.session_state.requests)
    sellers_count = random.randint(50, 150)
    visitors = random.randint(100, 300)
    return requests_count, sellers_count, visitors

# ==========================================
# 8. قسم البحث العكسي
# ==========================================
def search_request_section():
    """قسم عما تبحث؟"""
    st.markdown("""
    <div class="search-section">
        <div class="search-title">🔍 عما تبحث؟</div>
        <div class="search-subtitle">
            اكتب ما تريد والتجار في 69 ولاية سيتسابقون لخدمتك
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("", placeholder="مثال: محرك رونو سيمبول 2015، كراء استوديو في فوكة...", key="search_query")
    with col2:
        wilaya_req = st.selectbox("الولاية", ["كل الولايات"] + list(WILAYAS), key="search_wilaya")
    
    col1, col2, col3 = st.columns(3)
    with col2:
        search_clicked = st.button("🚀 أطلق الرادار", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if search_clicked and query:
        # محاكاة البحث
        progress_bar = st.progress(0, text="🔍 جاري البحث عن البائعين في 69 ولاية...")
        
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1, text=f"🔍 جاري البحث... {i+1}%")
        
        progress_bar.empty()
        
        # نتائج البحث
        st.markdown("""
        <div style="background: #2a2a3a; border-radius: 20px; padding: 20px; margin: 20px 0;">
            <h3 style="color: #00ffff; text-align: center;">✅ تم العثور على بائعين!</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # عرض البائعين
        sellers = [
            {"name": "محل الرونو - بومرداس", "phone": "0555123456", "distance": "12 كم"},
            {"name": "حديدو لقطع الغيار - الجزائر", "phone": "0666123456", "distance": "25 كم"},
            {"name": "خير الدين للخردة - تيبازة", "phone": "0777123456", "distance": "8 كم"}
        ]
        
        for seller in sellers:
            whatsapp = seller["phone"][1:] if seller["phone"].startswith('0') else seller["phone"]
            
            st.markdown(f"""
            <div class="seller-card">
                <div class="seller-name">{seller['name']}</div>
                <div style="color: #888; font-size: 0.9rem; margin: 5px 0;">
                    📍 {seller['distance']} من موقعك
                </div>
                <div class="seller-contact">
                    <a href="https://wa.me/213{whatsapp}" target="_blank" class="seller-btn">
                        📱 واتساب
                    </a>
                    <a href="tel:{seller['phone']}" class="seller-btn" style="background: #ff00ff;">
                        📞 اتصال
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.balloons()
        st.success("✨ تم العثور على 3 بائعين! تواصل معهم الآن.")

# ==========================================
# 9. طلبات المشتريين (للتجار)
# ==========================================
def show_buyer_requests():
    """عرض طلبات المشتريين للتجار"""
    st.markdown("## 📋 طلبات المشتريين النشطة")
    
    # فلترة
    col1, col2 = st.columns(2)
    with col1:
        filter_cat = st.selectbox("فلترة حسب الفئة", ["الكل"] + list(CATEGORIES))
    with col2:
        filter_wilaya = st.selectbox("فلترة حسب الولاية", ["كل الولايات"] + list(WILAYAS))
    
    filtered_requests = st.session_state.requests
    
    if filter_cat != "الكل":
        filtered_requests = [r for r in filtered_requests if r["category"] == filter_cat]
    if filter_wilaya != "كل الولايات":
        filtered_requests = [r for r in filtered_requests if r["wilaya"] == filter_wilaya]
    
    st.markdown(f"<p style='color: #888;'>عرض {len(filtered_requests)} طلب نشط</p>", unsafe_allow_html=True)
    
    for req in filtered_requests:
        whatsapp = req["phone"][1:] if req["phone"].startswith('0') else req["phone"]
        
        st.markdown(f"""
        <div class="request-card">
            <div class="request-header">
                <span class="request-category">{req['category']}</span>
                <span class="request-status">🟢 نشط</span>
            </div>
            <div class="request-title">{req['title']}</div>
            <div class="request-details">
                <span>📍 {req['wilaya']}</span>
                <span>👤 {req['buyer']}</span>
                <span>🕐 {req['date']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="request-offers">💰 {req['offers']} بائع تواصل</span>
                <div style="display: flex; gap: 10px;">
                    <a href="https://wa.me/213{whatsapp}" target="_blank" class="seller-btn" style="width: 100px; background: #00ffff; color: black; text-decoration: none; padding: 5px;">
                        تواصل
                    </a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 10. إضافة طلب جديد
# ==========================================
def add_new_request():
    """إضافة طلب جديد"""
    with st.form("new_request"):
        st.markdown("### 📝 طلب جديد")
        
        title = st.text_input("ما الذي تبحث عنه؟ *", placeholder="مثال: محرك رونو كليو 2 ديزل")
        category = st.selectbox("الفئة", CATEGORIES)
        wilaya = st.selectbox("الولاية", WILAYAS)
        buyer = st.text_input("اسمك *")
        phone = st.text_input("رقم الهاتف *", placeholder="0555123456")
        
        if st.form_submit_button("🔍 نشر الطلب", use_container_width=True) and title and buyer and phone:
            new_request = {
                "id": len(st.session_state.requests) + 1,
                "title": title,
                "category": category,
                "wilaya": wilaya,
                "buyer": buyer,
                "phone": phone,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status": "نشط",
                "offers": 0
            }
            st.session_state.requests.append(new_request)
            st.success("✅ تم نشر طلبك! سيتواصل معك البائعون قريباً.")
            st.balloons()
            time.sleep(1)
            st.rerun()

# ==========================================
# 11. إحصائيات
# ==========================================
def show_stats():
    """عرض إحصائيات"""
    requests_count, sellers_count, visitors = get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{requests_count}</div>
            <div class="stat-label">طلب نشط</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{sellers_count}</div>
            <div class="stat-label">تاجر متصل</div>
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
            <div class="stat-label">زائر الآن</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 12. فقاعة الدردشة
# ==========================================
def show_chat():
    """فقاعة الدردشة"""
    st.markdown("""
    <div class="chat-bubble" onclick="window.open('https://wa.me/213555555555')">
        <img src="https://img.icons8.com/ios-filled/30/000000/speech-bubble.png">
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 13. الدالة الرئيسية
# ==========================================
def main():
    """الدالة الرئيسية"""
    
    # عداد الزوار
    requests_count, sellers_count, visitors = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span style="color:#00ffff;">●</span> {visitors} زائر • {requests_count} طلب • {sellers_count} تاجر
    </div>
    """, unsafe_allow_html=True)
    
    # فقاعة الدردشة
    show_chat()
    
    # الشعار
    st.markdown("""
    <div class="logo">
        🎯 RASSIM OS
    </div>
    <div class="subtitle">
        السوق العكسي - المشتري يبحث والتاجر يجد • 69 ولاية
    </div>
    """, unsafe_allow_html=True)
    
    # آخر تحديث
    st.markdown(f"<p style='text-align:center; color:#666;'>آخر تحديث: {st.session_state.last_update}</p>", unsafe_allow_html=True)
    
    # إحصائيات
    show_stats()
    
    # تبويبات
    tab1, tab2, tab3 = st.tabs(["🎯 عما تبحث؟", "📋 طلبات المشتريين", "📝 طلب جديد"])
    
    with tab1:
        search_request_section()
    
    with tab2:
        show_buyer_requests()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 تحديث الطلبات", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("📊 إحصائيات البائعين", use_container_width=True):
                st.info(f"📈 {sellers_count} تاجر متصل الآن")
    
    with tab3:
        add_new_request()
    
    # تذييل
    st.markdown("""
    <div class="footer">
        RASSIM OS 2026 • نظام السوق العكسي • جميع الحقوق محفوظة
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 14. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()

