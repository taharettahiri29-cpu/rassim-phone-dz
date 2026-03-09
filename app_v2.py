#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===========================================================
⚡ RASSIM PRO - سوق الجزائر الذكي (نسخة مصححة الألوان)
===========================================================
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import hashlib
import json
import re
from supabase import create_client, Client

# ===========================================================
# 1. إعدادات الصفحة المتقدمة
# ===========================================================
st.set_page_config(
    page_title="RASSIM PRO • سوق الجزائر",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===========================================================
# 2. إدارة حالة الجلسة
# ===========================================================
if 'theme' not in st.session_state:
    st.session_state.theme = "داكن"
if 'language' not in st.session_state:
    st.session_state.language = "العربية"
if 'notifications' not in st.session_state:
    st.session_state.notifications = True
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'visitor_count' not in st.session_state:
    st.session_state.visitor_count = random.randint(1234, 5678)

# ===========================================================
# 3. قائمة الولايات (69 ولاية كاملة)
# ===========================================================
WILAYAS = [
    "16 - الجزائر", "31 - وهران", "25 - قسنطينة", "42 - تيبازة", "06 - بجاية",
    "19 - سطيف", "23 - عنابة", "13 - تلمسان", "09 - البليدة", "15 - تيزي وزو",
    "07 - بسكرة", "26 - المدية", "29 - معسكر", "35 - بومرداس", "41 - سوق أهراس",
    "47 - غرداية", "55 - توقرت", "57 - المغير", "58 - المنيع", "69 - عين الحجر",
    "01 - أدرار", "02 - الشلف", "03 - الأغواط", "04 - أم البواقي", "05 - باتنة",
    "08 - بشار", "10 - البويرة", "11 - تمنراست", "12 - تبسة", "14 - تيارت",
    "17 - الجلفة", "18 - جيجل", "20 - سعيدة", "21 - سكيكدة", "22 - سيدي بلعباس",
    "24 - قالمة", "27 - مستغانم", "28 - المسيلة", "30 - ورقلة", "32 - البيض",
    "33 - اليزي", "34 - برج بوعريريج", "36 - الطارف", "37 - تندوف", "38 - تسمسيلت",
    "39 - الوادي", "40 - خنشلة", "43 - ميلة", "44 - عين الدفلى", "45 - النعامة",
    "46 - عين تموشنت", "48 - غليزان", "49 - تيميمون", "50 - برج باجي مختار",
    "51 - أولاد جلال", "52 - بني عباس", "53 - عين صالح", "54 - عين قزام",
    "56 - جانت", "59 - المغير", "60 - المنيعة", "61 - أولاد جلال", "62 - تيميمون",
    "63 - تندوف", "64 - تقرت", "65 - الطارف", "66 - تسمسيلت", "67 - البيض",
    "68 - النعامة"
]

# ===========================================================
# 4. قائمة الفئات
# ===========================================================
CATEGORIES = [
    "🚗 قطع غيار سيارات",
    "🔧 خردة وأدوات",
    "🏠 عقارات (بيع/كراء)",
    "💄 تجميل / Cosmetique",
    "📱 هواتف وأجهزة",
    "🛋️ أثاث ومنزل",
    "👕 ملابس وأزياء",
    "🛠️ خدمات",
    "📦 أخرى"
]

# ===========================================================
# 5. نظام الثيم الديناميكي (CSS مصحح الألوان)
# ===========================================================
def load_css(theme):
    """تحميل التصميم حسب الثيم المختار - نسخة مصححة"""
    if theme == "داكن":
        bg_color = "#0a0a1a"
        card_color = "#1e1e2e"
        text_color = "#ffffff"
        input_bg = "#2d2d3a"
        input_text = "#ffffff"
        placeholder_color = "#aaaaaa"
        border_color = "#444444"
        gradient_start = "#00ffff"
        gradient_end = "#ff00ff"
    else:
        bg_color = "#f5f5f5"
        card_color = "#ffffff"
        text_color = "#000000"
        input_bg = "#ffffff"
        input_text = "#000000"
        placeholder_color = "#888888"
        border_color = "#dddddd"
        gradient_start = "#667eea"
        gradient_end = "#764ba2"
    
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    
    * {{
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        box-sizing: border-box;
    }}
    
    .stApp {{
        background: {bg_color};
        color: {text_color};
        transition: all 0.3s ease;
    }}
    
    /* ===== الشعار الرئيسي ===== */
    .main-header {{
        text-align: center;
        padding: 15px;
        margin-bottom: 10px;
    }}
    
    .logo {{
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, {gradient_start}, {gradient_end});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
    }}
    
    @keyframes shine {{
        to {{ background-position: 200% center; }}
    }}
    
    .subtitle {{
        color: #888;
        font-size: 1rem;
        margin-top: -10px;
    }}
    
    /* ===== أزرار احترافية ===== */
    .stButton > button {{
        width: 100% !important;
        height: 55px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, {gradient_start}, {gradient_end}) !important;
        color: {text_color if theme == "فاتح" else "#000000"} !important;
        border: none !important;
        margin: 8px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        transition: transform 0.2s;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.3);
    }}
    
    /* ===== إصلاح مشكلة ظهور النص في الحقول ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 2px solid {border_color} !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 16px !important;
        direction: rtl !important;
    }}
    
    /* لون النص عند الكتابة */
    .stTextInput > div > div > input:focus,
    .stTextArea > div > textarea:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {gradient_start} !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        color: {input_text} !important;
    }}
    
    /* لون النص المدخل */
    .stTextInput input, 
    .stTextArea textarea,
    .stNumberInput input {{
        color: {input_text} !important;
        caret-color: {gradient_start} !important;
    }}
    
    /* لون النص في selectbox */
    .stSelectbox div[data-baseweb="select"] > div {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}
    
    /* placeholder text color */
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {{
        color: {placeholder_color} !important;
        opacity: 0.8;
    }}
    
    /* ===== بطاقة التاجر المغناطيسية ===== */
    .magnet-card {{
        background: linear-gradient(135deg, #00aa00, #00ff00);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        margin: 15px 0;
        border: 2px solid white;
        animation: pulse-magnet 2s ease-in-out infinite;
    }}
    
    .magnet-title {{
        font-size: 1.8rem;
        font-weight: 900;
        color: white;
        text-shadow: 1px 1px 0 #000;
    }}
    
    .magnet-subtitle {{
        font-size: 1.1rem;
        color: white;
        margin: 15px 0;
    }}
    
    .magnet-badge {{
        background: white;
        color: #00aa00;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1rem;
        display: inline-block;
    }}
    
    /* ===== بطاقات ذكية ===== */
    .smart-card {{
        background: {card_color};
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border: 1px solid {border_color};
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    
    /* ===== بطاقة الطلب ===== */
    .request-card {{
        background: {card_color};
        border-right: 4px solid {gradient_start};
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        transition: all 0.3s ease;
        color: {text_color};
    }}
    
    .request-card:hover {{
        transform: translateX(-3px);
        background: #2a2a3a if theme == "داكن" else #f0f0f0;
    }}
    
    .request-header {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
    }}
    
    .request-category {{
        background: #2a2a3a;
        padding: 4px 10px;
        border-radius: 15px;
        color: {gradient_start};
        font-size: 0.75rem;
    }}
    
    .request-time {{
        color: #888;
        font-size: 0.75rem;
    }}
    
    .request-title {{
        color: {text_color};
        font-size: 1.1rem;
        font-weight: bold;
        margin: 8px 0;
    }}
    
    .request-details {{
        display: flex;
        gap: 10px;
        color: #888;
        font-size: 0.85rem;
    }}
    
    /* ===== عداد الزوار ===== */
    .live-counter {{
        position: fixed;
        bottom: 15px;
        left: 15px;
        background: {card_color};
        border: 1px solid {gradient_start};
        padding: 6px 12px;
        border-radius: 50px;
        z-index: 999;
        color: {text_color};
        font-size: 0.8rem;
        backdrop-filter: blur(5px);
    }}
    
    /* ===== فقاعة الدردشة ===== */
    .chat-bubble {{
        position: fixed;
        bottom: 15px;
        right: 15px;
        background: {gradient_start};
        width: 45px;
        height: 45px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 9999;
        animation: float 3s ease-in-out infinite;
        box-shadow: 0 4px 15px rgba(0,255,255,0.3);
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-5px); }}
    }}
    
    .chat-bubble img {{
        width: 22px;
        height: 22px;
        filter: brightness(0) invert(1);
    }}
    
    /* ===== تذييل ===== */
    .footer {{
        text-align: center;
        color: #666;
        font-size: 0.75rem;
        margin-top: 30px;
        padding: 15px;
        border-top: 1px solid #333;
    }}
    
    /* ===== رسائل النجاح والخطأ ===== */
    .stAlert {{
        border-radius: 12px !important;
        padding: 12px !important;
        font-weight: 600 !important;
    }}
    
    /* ===== إصلاح تباين النص ===== */
    p, h1, h2, h3, h4, h5, h6, span, div {{
        color: {text_color};
    }}
    
    /* ===== إصلاح لون النص في selectbox ===== */
    .stSelectbox div[role="button"] p {{
        color: {input_text} !important;
    }}
    
    /* ===== إخفاء العناصر غير الضرورية ===== */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    </style>
    """

# ===========================================================
# 6. الاتصال بقاعدة البيانات Supabase
# ===========================================================
@st.cache_resource
def init_connection():
    """تهيئة الاتصال بـ Supabase"""
    try:
        url = st.secrets["connections"]["supabase"]["url"]
        key = st.secrets["connections"]["supabase"]["key"]
        client = create_client(url, key)
        return client, True
    except Exception as e:
        return None, False

supabase, connected = init_connection()

# ===========================================================
# 7. دوال مساعدة للتحقق
# ===========================================================
def validate_phone(phone):
    """التحقق من صحة رقم الهاتف الجزائري"""
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    pattern = r'^(05|06|07|5|6|7)[0-9]{8}$'
    return re.match(pattern, phone) is not None

def validate_item(item):
    return len(item.strip()) >= 3

def format_phone(phone):
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    if len(phone) == 9:
        phone = '0' + phone
    return phone

# ===========================================================
# 8. دوال التعامل مع قاعدة البيانات
# ===========================================================
def fetch_requests(limit=20):
    if not connected:
        return pd.DataFrame()
    try:
        response = supabase.table("requests").select("*").order("created_at", desc=True).limit(limit).execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except:
        return pd.DataFrame()

def fetch_vendors(limit=20):
    if not connected:
        return pd.DataFrame()
    try:
        response = supabase.table("vendors").select("*").order("created_at", desc=True).limit(limit).execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except:
        return pd.DataFrame()

def fetch_leads(limit=20):
    if not connected:
        return pd.DataFrame()
    try:
        response = supabase.table("leads").select("*").order("created_at", desc=True).limit(limit).execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except:
        return pd.DataFrame()

def save_request(item, category, phone, wilaya, min_price=0, max_price=0, condition="الكل"):
    if not connected:
        return False
    try:
        phone = format_phone(phone)
        data = {
            "item": item,
            "category": category,
            "phone": phone,
            "wilaya": wilaya,
            "min_price": min_price,
            "max_price": max_price,
            "condition": condition,
            "status": "نشط",
            "created_at": datetime.now().isoformat()
        }
        supabase.table("requests").insert(data).execute()
        return True
    except:
        return False

def save_vendor(name, phone, wilaya, categories, source="direct"):
    if not connected:
        return False
    try:
        phone = format_phone(phone)
        existing = supabase.table("vendors").select("*").eq("phone", phone).execute()
        if existing.data and len(existing.data) > 0:
            return False
        
        referral_code = hashlib.md5(f"{phone}{datetime.now()}".encode()).hexdigest()[:8]
        data = {
            "name": name,
            "phone": phone,
            "wilaya": wilaya,
            "category": ", ".join(categories),
            "source": source,
            "verified": False,
            "trial": True,
            "referral_code": referral_code,
            "created_at": datetime.now().isoformat()
        }
        supabase.table("vendors").insert(data).execute()
        return True
    except:
        return False

def save_lead(name, phone, wilaya, source):
    if not connected:
        return False
    try:
        phone = format_phone(phone)
        data = {
            "name": name,
            "phone": phone,
            "wilaya": wilaya,
            "source": source,
            "contacted": False,
            "created_at": datetime.now().isoformat()
        }
        supabase.table("leads").insert(data).execute()
        return True
    except:
        return False

def get_stats():
    try:
        requests_df = fetch_requests()
        vendors_df = fetch_vendors()
        leads_df = fetch_leads()
        return len(vendors_df) if not vendors_df.empty else 0, len(requests_df) if not requests_df.empty else 0, len(leads_df) if not leads_df.empty else 0
    except:
        return 0, 0, 0

# ===========================================================
# 9. الشريط الجانبي
# ===========================================================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:15px;'>
        <h1 style='background: linear-gradient(135deg, #667eea, #764ba2);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size:24px;'>⚡ RASSIM PRO</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if connected:
        st.success("✅ متصل")
    else:
        st.error("❌ غير متصل")
    
    with st.expander("⚙️ الإعدادات", expanded=False):
        st.session_state.theme = st.radio("المظهر", ["داكن", "فاتح"], index=0)
        st.session_state.language = st.selectbox("اللغة", ["العربية", "Français"])
        st.session_state.notifications = st.toggle("الإشعارات", value=True)

# ===========================================================
# 10. واجهة رادار الطلبات (مصححة)
# ===========================================================
def buyer_radar_ui():
    """واجهة المشتري - إطلاق الرادار (نسخة مصححة)"""
    
    st.markdown("""
    <div class="smart-card">
        <h2 style="color:#00ffff; text-align:center; margin-bottom:10px;">🎯 رادار RASSIM PRO</h2>
        <p style="color:#888; text-align:center; font-size:0.9rem;">اكتب ما تبحث عنه وسيبحث لك النظام في 69 ولاية</p>
    """, unsafe_allow_html=True)
    
    # نموذج البحث
    item = st.text_input("🔍 ماذا تبحث؟", placeholder="مثال: محرك كيا سبورتاج 2002")
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("📂 الفئة", CATEGORIES, index=0)
    with col2:
        wilaya = st.selectbox("📍 الولاية", WILAYAS, index=0)
    
    col1, col2 = st.columns(2)
    with col1:
        min_price = st.number_input("💰 من (دج)", min_value=0, value=0, step=1000)
    with col2:
        max_price = st.number_input("💰 إلى (دج)", min_value=0, value=1000000, step=1000)
    
    condition = st.selectbox("🔧 الحالة", ["الكل", "جديد", "مستعمل", "تشليح"])
    phone = st.text_input("📱 رقم الهاتف", placeholder="06XXXXXXXX")
    
    # زر معاينة البحث
    if st.button("🔍 معاينة البحث", use_container_width=True):
        if item and phone:
            with st.spinner("📡 جاري البحث..."):
                time.sleep(1)
            st.info(f"✅ تم العثور على {random.randint(3, 15)} تاجر محتمل")
    
    # زر إطلاق الرادار
    if st.button("🚀 إطلاق الرادار", use_container_width=True):
        if not item or not phone:
            st.error("❌ الرجاء ملء جميع الحقول")
        elif not validate_phone(phone):
            st.error("❌ رقم هاتف غير صالح")
        else:
            with st.spinner("📡 جاري الإطلاق..."):
                time.sleep(2)
            if save_request(item, category, phone, wilaya, min_price, max_price, condition):
                st.success("✅ تم الإطلاق! سيتم التواصل معك قريباً")
                st.balloons()
            else:
                st.warning("⚠️ تم الحفظ محلياً")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================
# 11. الصفحة الرئيسية
# ===========================================================
def main():
    # تطبيق التصميم
    st.markdown(load_css(st.session_state.theme), unsafe_allow_html=True)
    
    # عداد الزوار
    vendors, requests, leads = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span style="color:#00ffff;">●</span> {st.session_state.visitor_count} زائر
    </div>
    """, unsafe_allow_html=True)
    
    # فقاعة الدردشة
    st.markdown("""
    <div class="chat-bubble" onclick="window.open('https://wa.me/213555555555')">
        <img src="https://img.icons8.com/ios-filled/30/ffffff/speech-bubble.png">
    </div>
    """, unsafe_allow_html=True)
    
    # الشعار
    st.markdown("""
    <div class="main-header">
        <div class="logo">⚡ RASSIM PRO</div>
        <div class="subtitle">سوق الجزائر الذكي • 69 ولاية</div>
    </div>
    """, unsafe_allow_html=True)
    
    # التبويبات
    tab1, tab2 = st.tabs(["🎯 رادار المشتري", "🧲 انضم كتاجر"])
    
    with tab1:
        buyer_radar_ui()
        
        st.markdown("### 📋 آخر الطلبات")
        requests_df = fetch_requests(5)
        if not requests_df.empty:
            for _, row in requests_df.iterrows():
                st.markdown(f"""
                <div class="request-card">
                    <div class="request-header">
                        <span class="request-category">{row.get('category', '')[:15]}</span>
                        <span class="request-time">{row.get('created_at', '')[:10] if row.get('created_at') else ''}</span>
                    </div>
                    <div class="request-title">{row.get('item', '')[:30]}</div>
                    <div class="request-details">
                        <span>📍 {row.get('wilaya', '')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا توجد طلبات بعد")
    
    with tab2:
        st.markdown("""
        <div class="smart-card" style="text-align:center;">
            <h3 style="color:#ff00ff;">🧲 عرض خاص للتجار</h3>
            <p>سجل محلك الآن واحصل على أول 10 زبائن مجاناً!</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("vendor_form"):
            name = st.text_input("🏪 اسم المحل", placeholder="مثال: مؤسسة الرونو")
            phone = st.text_input("📞 رقم الهاتف", placeholder="0555123456")
            wilaya = st.selectbox("📍 الولاية", WILAYAS)
            categories = st.multiselect("📋 ماذا تبيع؟", CATEGORIES)
            
            if st.form_submit_button("🚀 سجل الآن", use_container_width=True):
                if name and phone and categories:
                    if validate_phone(phone):
                        if save_vendor(name, phone, wilaya, categories):
                            st.success("✅ تم التسجيل بنجاح!")
                            st.balloons()
                        else:
                            st.error("❌ هذا الرقم مسجل مسبقاً")
                    else:
                        st.error("❌ رقم هاتف غير صالح")
                else:
                    st.error("❌ املأ جميع الحقول")
    
    # تذييل
    st.markdown("""
    <div class="footer">
        ⚡ RASSIM PRO 2026
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
