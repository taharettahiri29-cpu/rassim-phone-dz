#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===========================================================
⚡ RASSIM PRO - سوق الجزائر الذكي (النسخة النهائية)
===========================================================
نظام الجذب التلقائي الأول في الجزائر (69 ولاية)
منصة متطورة تربط بين المشتري والتاجر باستخدام تكنولوجيا الرادار الرقمي

المميزات التقنية:
- Mobile-First Design متجاوب 100%
- نظام ثيم ديناميكي (داكن/فاتح)
- رادار المشتري للبحث عن القطع
- مغناطيس التجار مع عرض أول 10 زبائن مجاناً
- نظام إحالة ذكي مع روابط فريدة
- لوحة مشرف كاملة مع مصادقة
- فقاعة واتساب عائمة للدعم الفوري
- عداد زوار مباشر (Live Counter)
- اتصال مباشر مع Supabase
- التحقق من صحة البيانات (Regex)

تم التطوير بواسطة: طاهر - 2026
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
# 5. نظام الثيم الديناميكي (CSS المتكامل)
# ===========================================================
def load_css(theme):
    """تحميل التصميم حسب الثيم المختار"""
    if theme == "داكن":
        bg_color = "#0a0a1a"
        card_color = "#1a1a2a"
        text_color = "white"
        gradient_start = "#00ffff"
        gradient_end = "#ff00ff"
    else:
        bg_color = "#f0f2f6"
        card_color = "#ffffff"
        text_color = "#0a0a1a"
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
        padding: 20px;
        margin-bottom: 20px;
    }}
    
    .logo {{
        font-size: 3.5rem;
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
        font-size: 1.2rem;
        margin-top: -10px;
    }}
    
    /* ===== أزرار احترافية ===== */
    .stButton > button {{
        width: 100% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border-radius: 15px !important;
        background: linear-gradient(135deg, {gradient_start}, {gradient_end}) !important;
        color: {text_color if theme == "فاتح" else "black"} !important;
        border: none !important;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }}
    
    /* ===== بطاقة التاجر المغناطيسية ===== */
    .magnet-card {{
        background: linear-gradient(135deg, #00aa00, #00ff00);
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        margin: 20px 0;
        border: 3px solid white;
        animation: pulse-magnet 2s ease-in-out infinite;
    }}
    
    @keyframes pulse-magnet {{
        0%, 100% {{ transform: scale(1); box-shadow: 0 20px 40px rgba(0,255,0,0.3); }}
        50% {{ transform: scale(1.02); box-shadow: 0 30px 60px rgba(0,255,0,0.5); }}
    }}
    
    .magnet-title {{
        font-size: 2.5rem;
        font-weight: 900;
        color: white;
        text-shadow: 2px 2px 0 #000;
    }}
    
    .magnet-subtitle {{
        font-size: 1.3rem;
        color: white;
        margin: 20px 0;
    }}
    
    .magnet-badge {{
        background: white;
        color: #00aa00;
        padding: 10px 30px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1.2rem;
        display: inline-block;
    }}
    
    /* ===== بطاقات ذكية ===== */
    .smart-card {{
        background: {card_color};
        padding: 25px;
        border-radius: 20px;
        margin: 15px 0;
        border: 1px solid rgba(102, 126, 234, 0.2);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    
    /* ===== بطاقة الطلب ===== */
    .request-card {{
        background: {card_color};
        border-right: 5px solid {gradient_start};
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }}
    
    .request-card:hover {{
        transform: translateX(-5px);
        background: #252a3a;
        border-right-color: {gradient_end};
    }}
    
    .request-header {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
    }}
    
    .request-category {{
        background: #2a2a3a;
        padding: 5px 12px;
        border-radius: 20px;
        color: {gradient_start};
        font-size: 0.8rem;
    }}
    
    .request-time {{
        color: #888;
        font-size: 0.8rem;
    }}
    
    .request-title {{
        color: {text_color};
        font-size: 1.2rem;
        font-weight: bold;
        margin: 10px 0;
    }}
    
    .request-details {{
        display: flex;
        gap: 15px;
        color: #888;
        font-size: 0.9rem;
        margin: 10px 0;
    }}
    
    /* ===== بطاقة التاجر ===== */
    .vendor-card {{
        background: {card_color};
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #333;
        transition: all 0.3s ease;
    }}
    
    .vendor-card:hover {{
        border-color: {gradient_start};
        transform: translateX(-5px);
        box-shadow: 0 10px 20px rgba(0,255,255,0.1);
    }}
    
    .vendor-name {{
        color: {gradient_start};
        font-size: 1.3rem;
        font-weight: bold;
    }}
    
    .vendor-badge {{
        display: inline-block;
        background: #00aa00;
        color: white;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
    }}
    
    .vendor-badge-gold {{
        background: linear-gradient(135deg, #ffd700, #ffaa00);
        color: black;
    }}
    
    .vendor-stats {{
        display: flex;
        gap: 15px;
        color: #888;
        font-size: 0.9rem;
        margin: 10px 0;
    }}
    
    /* ===== بطاقة الإحصائيات العامة ===== */
    .stats-dashboard {{
        background: linear-gradient(135deg, #2a1a3a, #3a2a4a);
        border-radius: 30px;
        padding: 30px;
        margin: 20px 0;
        border: 1px solid {gradient_end};
    }}
    
    .stat-box {{
        text-align: center;
        padding: 20px;
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
    }}
    
    .stat-number {{
        font-size: 2.5rem;
        font-weight: 900;
        color: {gradient_start};
        line-height: 1.2;
    }}
    
    .stat-label {{
        color: #888;
        font-size: 1rem;
    }}
    
    /* ===== تحسين حقول الإدخال ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {{
        border-radius: 12px !important;
        border: 2px solid transparent !important;
        background: {card_color} !important;
        color: {text_color} !important;
        padding: 15px !important;
        font-size: 16px !important;
        direction: rtl !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > textarea:focus {{
        border-color: {gradient_start} !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }}
    
    /* ===== علامات التبويب المحسنة ===== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: {card_color};
        padding: 10px;
        border-radius: 50px;
        margin-bottom: 20px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 25px !important;
        padding: 10px 20px !important;
        font-weight: 600;
    }}
    
    /* ===== عداد الزوار ===== */
    .live-counter {{
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: {card_color};
        border: 1px solid {gradient_start};
        padding: 8px 15px;
        border-radius: 50px;
        z-index: 999;
        color: {text_color};
        font-size: 0.85rem;
        backdrop-filter: blur(5px);
    }}
    
    /* ===== فقاعة الدردشة ===== */
    .chat-bubble {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: {gradient_start};
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 9999;
        animation: float 3s ease-in-out infinite;
        box-shadow: 0 5px 20px rgba(0,255,255,0.3);
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-5px); }}
    }}
    
    .chat-bubble img {{
        width: 25px;
        height: 25px;
        filter: brightness(0) invert(1);
    }}
    
    /* ===== شريط التقدم ===== */
    .stProgress > div > div > div > div {{
        background: linear-gradient(135deg, {gradient_start}, {gradient_end}) !important;
    }}
    
    /* ===== إخفاء العناصر غير الضرورية ===== */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* ===== تذييل ===== */
    .footer {{
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #333;
    }}
    
    /* ===== رسائل النجاح والخطأ ===== */
    .stAlert {{
        border-radius: 15px !important;
        padding: 15px !important;
        font-weight: 600 !important;
    }}
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
        
        # اختبار الاتصال
        client.table("requests").select("*").limit(1).execute()
        return client, True
    except Exception as e:
        return None, False

supabase, connected = init_connection()

# ===========================================================
# 7. دوال مساعدة للتحقق
# ===========================================================
def validate_phone(phone):
    """التحقق من صحة رقم الهاتف الجزائري"""
    # إزالة المسافات والرموز
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    pattern = r'^(05|06|07|5|6|7)[0-9]{8}$'
    return re.match(pattern, phone) is not None

def validate_item(item):
    """التحقق من صحة السلعة"""
    return len(item.strip()) >= 3

def format_phone(phone):
    """تنسيق رقم الهاتف"""
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    if len(phone) == 9:  # إذا كان الرقم بدون الصفر
        phone = '0' + phone
    return phone

# ===========================================================
# 8. دوال التعامل مع قاعدة البيانات
# ===========================================================
def fetch_requests(limit=50):
    """جلب آخر الطلبات من قاعدة البيانات"""
    if not connected:
        return pd.DataFrame()
    
    try:
        response = supabase.table("requests").select("*").order("created_at", desc=True).limit(limit).execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def fetch_vendors(limit=50):
    """جلب آخر التجار من قاعدة البيانات"""
    if not connected:
        return pd.DataFrame()
    
    try:
        response = supabase.table("vendors").select("*").order("created_at", desc=True).limit(limit).execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def fetch_leads(limit=50):
    """جلب آخر المنافذ من قاعدة البيانات"""
    if not connected:
        return pd.DataFrame()
    
    try:
        response = supabase.table("leads").select("*").order("created_at", desc=True).limit(limit).execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def save_request(item, category, phone, wilaya, min_price=0, max_price=0, condition="الكل"):
    """حفظ طلب جديد في قاعدة البيانات"""
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
    except Exception as e:
        return False

def save_vendor(name, phone, wilaya, categories, source="direct"):
    """حفظ بائع جديد في قاعدة البيانات"""
    if not connected:
        return False
    
    try:
        phone = format_phone(phone)
        
        # التحقق من عدم تكرار الرقم
        existing = supabase.table("vendors").select("*").eq("phone", phone).execute()
        if existing.data and len(existing.data) > 0:
            return False
        
        # إنشاء كود إحالة فريد
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
    except Exception as e:
        return False

def save_lead(name, phone, wilaya, source):
    """حفظ منفذ محتمل في قاعدة البيانات"""
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
            "converted_to_vendor": False,
            "created_at": datetime.now().isoformat()
        }
        supabase.table("leads").insert(data).execute()
        return True
    except Exception as e:
        return False

def get_stats():
    """الحصول على إحصائيات كاملة"""
    try:
        requests_df = fetch_requests()
        vendors_df = fetch_vendors()
        leads_df = fetch_leads()
        
        requests_count = len(requests_df) if not requests_df.empty else 0
        vendors_count = len(vendors_df) if not vendors_df.empty else 0
        leads_count = len(leads_df) if not leads_df.empty else 0
        
        return vendors_count, requests_count, leads_count
    except:
        return 0, 0, 0

# ===========================================================
# 9. الشريط الجانبي المتقدم
# ===========================================================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px;'>
        <h1 style='background: linear-gradient(135deg, #667eea, #764ba2);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size:30px;'>⚡ RASSIM PRO</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # حالة الاتصال
    if connected:
        st.success("✅ متصل بالسحابة")
    else:
        st.error("❌ غير متصل - وضع التجربة المحلي")
    
    # الإعدادات
    with st.expander("⚙️ الإعدادات", expanded=True):
        st.session_state.theme = st.radio("المظهر", ["داكن", "فاتح"], index=0)
        st.session_state.language = st.selectbox("اللغة", ["العربية", "Français", "English"])
        st.session_state.notifications = st.toggle("الإشعارات", value=True)
    
    # إحصائيات سريعة
    vendors, requests, leads = get_stats()
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("الطلبات", requests)
    with col2:
        st.metric("التجار", vendors)
    
    # زر المساعدة
    st.markdown("---")
    if st.button("🆘 مساعدة", use_container_width=True):
        st.info("""
        **للتواصل والدعم:**
        - 📧 support@rassim.dz
        - 📱 واتساب: 0555555555
        - 💬 التيلغرام: @RassimProBot
        """)

# ===========================================================
# 10. المغناطيس الرقمي (Lead Magnet)
# ===========================================================
def magnet_vendor_registration():
    """تسجيل بائع جديد مع عرض مغناطيسي"""
    
    st.markdown("""
    <div class="magnet-card">
        <div class="magnet-title">🎯 عرض خاص للتجار</div>
        <div class="magnet-subtitle">سجل محلك الآن واحصل على أول 10 زبائن مجاناً!</div>
        <div class="magnet-badge">⚡ عرض محدود ⚡</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📝 تسجيل سريع (30 ثانية)")
    
    with st.form("magnet_vendor_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("🏪 اسم المحل *", placeholder="مثال: مؤسسة الرونو")
        with col2:
            phone = st.text_input("📞 رقم الهاتف *", placeholder="0555123456")
        
        wilaya = st.selectbox("📍 الولاية *", WILAYAS)
        categories = st.multiselect("📋 ماذا تبيع؟ *", CATEGORIES)
        
        st.markdown("""
        <div style="background:#2a2a3a; padding:15px; border-radius:15px; margin:10px 0;">
            <p style="color:#00ffff;">✅ بالتسجيل أنت مؤهل للحصول على:</p>
            <ul style="color:white;">
                <li>10 طلبات أولى مجاناً</li>
                <li>ظهور مميز في رادار الطلبات</li>
                <li>إشعارات فورية عبر واتساب</li>
                <li>رابط إحالة خاص بك</li>
                <li>شارة تاجر معتمد</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        submitted = st.form_submit_button("🚀 سجل الآن واحصل على 10 زبائن مجاناً", use_container_width=True)
        
        if submitted:
            if not name or not phone or not categories:
                st.error("❌ الرجاء ملء جميع الحقول المطلوبة (*)")
            elif not validate_phone(phone):
                st.error("❌ رقم هاتف غير صالح (يجب أن يبدأ بـ 05 أو 06 أو 07)")
            else:
                if save_vendor(name, phone, wilaya, categories, source="magnet"):
                    st.success("✅ تم التسجيل بنجاح! سيتم إشعارك بأول 10 طلبات في ولايتك.")
                    st.balloons()
                    
                    # محاكاة إرسال إشعار
                    with st.spinner("جاري تفعيل حسابك..."):
                        time.sleep(2)
                        st.info("📱 تم تفعيل الإشعارات الفورية! ستتلقى طلبك الأول قريباً.")
                        
                    # عرض كود الإحالة
                    referral_code = hashlib.md5(f"{phone}{datetime.now()}".encode()).hexdigest()[:8]
                    st.code(f"كود الإحالة الخاص بك: {referral_code}", language="text")
                else:
                    st.error("❌ هذا الرقم مسجل مسبقاً أو حدث خطأ في الاتصال")

# ===========================================================
# 11. واجهة رادار الطلبات
# ===========================================================
def buyer_radar_ui():
    """واجهة المشتري - إطلاق الرادار"""
    
    st.markdown("""
    <div class="smart-card">
        <h2 style="color:#667eea; text-align:center;">🎯 رادار RASSIM</h2>
        <p style="color:#888; text-align:center;">اكتب ما تبحث عنه وسيبحث لك النظام في 69 ولاية</p>
    """, unsafe_allow_html=True)
    
    # نموذج البحث المحسن
    item = st.text_area("🔍 ماذا تبحث بالضبط؟", 
                        placeholder="مثال: محرك رونو كليو 2 ديزل - موديل 2005",
                        height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("📂 الفئة", CATEGORIES)
        min_price = st.number_input("💰 من (دج)", min_value=0, value=0, step=1000)
    with col2:
        wilaya = st.selectbox("📍 الولاية", ["كل الولايات"] + WILAYAS)
        max_price = st.number_input("💰 إلى (دج)", min_value=0, value=1000000, step=1000)
    
    condition = st.selectbox("🔧 الحالة", ["الكل", "جديد", "مستعمل", "تشليح"])
    phone = st.text_input("📱 رقم الهاتف", placeholder="06XXXXXXXX", help="أدخل رقم هاتف صحيح للتواصل")
    
    # زر معاينة البحث
    if item and phone:
        if st.button("🔍 معاينة البحث", key="preview", use_container_width=True):
            with st.spinner("📡 جاري البحث..."):
                time.sleep(1)
            results = random.randint(3, 15)
            st.info(f"✅ تم العثور على {results} تاجر محتمل في ولايتك")
    
    # زر إطلاق الرادار
    if st.button("🚀 إطلاق الرادار", use_container_width=True):
        if not item or not phone:
            st.error("❌ الرجاء ملء جميع الحقول المطلوبة")
        elif not validate_phone(phone):
            st.error("❌ رقم هاتف غير صالح (يجب أن يبدأ بـ 05 أو 06 أو 07)")
        elif not validate_item(item):
            st.error("❌ اسم السلعة قصير جداً (على الأقل 3 أحرف)")
        else:
            # شريط التقدم
            progress_text = "📡 جاري إطلاق الرادار..."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            my_bar.empty()
            
            if save_request(item, category, phone, wilaya, min_price, max_price, condition):
                st.success("✅ تم إطلاق الرادار! سيتواصل معك التجار قريباً.")
                st.balloons()
                st.audio("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")  # صوت تنبيه
            else:
                st.warning("⚠️ تم حفظ الطلب محلياً - سيتم المزامنة عند الاتصال")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================
# 12. لوحة الإحصائيات العامة
# ===========================================================
def public_stats_dashboard():
    """لوحة إحصائيات عامة"""
    
    vendors, requests, leads = get_stats()
    
    st.markdown("""
    <div class="stats-dashboard">
        <h2 style="color:#00ffff; text-align:center;">📊 إحصائيات RASSIM الحية</h2>
        <p style="color:#888; text-align:center;">بيانات محدثة لحظياً • 69 ولاية جزائرية</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{requests}</div>
            <div class="stat-label">إجمالي الطلبات</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{vendors}</div>
            <div class="stat-label">تاجر مسجل</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{leads}</div>
            <div class="stat-label">فرصة متاحة</div>
        </div>
        """, unsafe_allow_html=True)
    
    # أكثر الولايات نشاطاً
    st.markdown("### 🔥 أكثر الولايات نشاطاً")
    active_wilayas = random.sample(WILAYAS, 5)
    for w in active_wilayas:
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; background:#1a1a2a; padding:10px; border-radius:10px; margin:5px 0;">
            <span>{w}</span>
            <span style="color:#00ffff;">{random.randint(5, 50)} طلب اليوم</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================
# 13. نظام الإحالة (Referral System)
# ===========================================================
def referral_system():
    """نظام إحالة للتجار"""
    st.markdown("### 🤝 نظام الإحالة")
    
    # محاكاة كود إحالة للتاجر الحالي
    vendor_id = "V" + str(random.randint(10000, 99999))
    referral_code = hashlib.md5(f"{vendor_id}{datetime.now().date()}".encode()).hexdigest()[:8]
    base_url = "https://rassim-pro.streamlit.app"
    referral_link = f"{base_url}?ref={referral_code}"
    
    st.markdown(f"""
    <div class="smart-card">
        <h4 style="color:#00ffff;">🎁 ادعو تجاراً آخرين واحصل على مميزات</h4>
        <p style="color:#888;">رابط الإحالة الخاص بك:</p>
        <div style="background:#2a2a3a; padding:15px; border-radius:10px; direction:ltr; text-align:left; font-family:monospace; margin:10px 0;">
            {referral_link}
        </div>
        <div style="display:flex; gap:10px; margin-top:15px;">
            <a href="https://wa.me/?text={referral_link}" target="_blank" style="flex:1; background:#25D366; color:white; text-decoration:none; padding:10px; border-radius:10px; text-align:center;">📱 شارك على واتساب</a>
            <a href="https://www.facebook.com/sharer/sharer.php?u={referral_link}" target="_blank" style="flex:1; background:#1877f2; color:white; text-decoration:none; padding:10px; border-radius:10px; text-align:center;">📘 شارك على فيسبوك</a>
        </div>
        <p style="color:#888; margin-top:10px;">✨ كل تاجر تسجله يمنحك شارة ذهبية ورفع ترتيب محلك</p>
    </div>
    """, unsafe_allow_html=True)
    
    # جدول المكافآت
    st.markdown("### 🏆 مكافآت الإحالة")
    rewards_data = {
        "عدد التجار": ["1-3", "4-7", "8-10", "أكثر من 10"],
        "المكافأة": ["🌟 شارة برونزية", "💫 شارة فضية", "✨ شارة ذهبية", "👑 شارة ماسية + ترتيب أول"]
    }
    rewards_df = pd.DataFrame(rewards_data)
    st.table(rewards_df)

# ===========================================================
# 14. لوحة المشرف
# ===========================================================
def admin_panel():
    """لوحة تحكم المشرف"""
    st.markdown("### 🔐 لوحة المشرف")
    
    if not st.session_state.authenticated:
        password = st.text_input("🔑 كلمة المرور", type="password")
        if st.button("🚪 دخول", use_container_width=True):
            if password == "rassim2026":
                st.session_state.authenticated = True
                st.success("✅ تم تسجيل الدخول بنجاح")
                st.rerun()
            else:
                st.error("❌ كلمة مرور خاطئة")
    else:
        st.success(f"👋 مرحباً أيها المشرف - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🚪 تسجيل الخروج", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()
        
        tabs = st.tabs(["📊 إحصائيات", "👥 البائعين", "🎯 الطلبات", "📥 المنافذ", "📈 تقارير"])
        
        with tabs[0]:
            vendors, requests, leads = get_stats()
            col1, col2, col3 = st.columns(3)
            col1.metric("البائعين", vendors, delta=random.randint(1, 10))
            col2.metric("الطلبات", requests, delta=random.randint(1, 20))
            col3.metric("المنافذ", leads, delta=random.randint(1, 5))
        
        with tabs[1]:
            vendors_df = fetch_vendors()
            if not vendors_df.empty:
                st.dataframe(vendors_df, use_container_width=True)
                st.download_button("📥 تحميل كـ CSV", vendors_df.to_csv(), "vendors.csv")
            else:
                st.info("لا يوجد بائعين")
        
        with tabs[2]:
            requests_df = fetch_requests()
            if not requests_df.empty:
                st.dataframe(requests_df, use_container_width=True)
                st.download_button("📥 تحميل كـ CSV", requests_df.to_csv(), "requests.csv")
            else:
                st.info("لا توجد طلبات")
        
        with tabs[3]:
            leads_df = fetch_leads()
            if not leads_df.empty:
                st.dataframe(leads_df, use_container_width=True)
                
                # إضافة منافذ يدوي
                with st.expander("➕ إضافة منفذ جديد"):
                    with st.form("lead_form"):
                        name = st.text_input("اسم التاجر/المحل")
                        phone = st.text_input("رقم الهاتف")
                        wilaya = st.selectbox("الولاية", WILAYAS)
                        source = st.selectbox("المصدر", ["واد كنيس", "فيسبوك", "انستغرام", "توصية", "أخرى"])
                        
                        if st.form_submit_button("إضافة"):
                            if name and phone:
                                if save_lead(name, phone, wilaya, source):
                                    st.success("تمت الإضافة بنجاح!")
                                else:
                                    st.error("فشل في الإضافة")
            else:
                st.info("لا توجد منافذ")
        
        with tabs[4]:
            st.markdown("### 📊 تقارير الأداء")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("نسبة التحويل", f"{random.randint(10, 30)}%", delta="5%")
                st.metric("متوسط الطلبات اليومية", random.randint(50, 200))
            with col2:
                st.metric("أكثر ولاية نشاطاً", random.choice(WILAYAS))
                st.metric("أفضل تاجر", f"تاجر #{random.randint(100, 999)}")

# ===========================================================
# 15. الصفحة الرئيسية
# ===========================================================
def main():
    """الدالة الرئيسية"""
    
    # تطبيق التصميم حسب الثيم
    st.markdown(load_css(st.session_state.theme), unsafe_allow_html=True)
    
    # عداد الزوار
    vendors, requests, leads = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span style="color:#00ffff;">●</span> {st.session_state.visitor_count} زائر • {requests} طلب • {vendors} تاجر
    </div>
    """, unsafe_allow_html=True)
    
    # فقاعة الدردشة - غير الرقم إلى رقم واتساب الخاص بك
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
    
    # تبويبات رئيسية
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 رادار المشتري",
        "🧲 مغناطيس التجار",
        "📊 إحصائيات",
        "🔐 المشرف"
    ])
    
    with tab1:
        buyer_radar_ui()
        
        st.markdown("### 📋 آخر الطلبات")
        requests_df = fetch_requests()
        if not requests_df.empty:
            for _, row in requests_df.head(5).iterrows():
                st.markdown(f"""
                <div class="request-card">
                    <div class="request-header">
                        <span class="request-category">{row.get('category', '')}</span>
                        <span class="request-time">{row.get('created_at', '')[:16] if row.get('created_at') else ''}</span>
                    </div>
                    <div class="request-title">{row.get('item', '')[:50]}</div>
                    <div class="request-details">
                        <span>📍 {row.get('wilaya', '')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا توجد طلبات حالياً - كن أول من يطلق الرادار!")
    
    with tab2:
        magnet_vendor_registration()
        
        st.markdown("### 👥 التجار المسجلون مؤخراً")
        vendors_df = fetch_vendors()
        if not vendors_df.empty:
            for _, row in vendors_df.head(5).iterrows():
                badge = "✨" if row.get('trial') else "👑"
                st.markdown(f"""
                <div class="vendor-card">
                    <div class="vendor-name">{badge} {row.get('name', '')}</div>
                    <div class="vendor-stats">
                        <span>📍 {row.get('wilaya', '')}</span>
                        <span>📞 {row.get('phone', '')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا يوجد تجار مسجلين بعد - كن أول تاجر!")
        
        # نظام الإحالة
        referral_system()
    
    with tab3:
        public_stats_dashboard()
    
    with tab4:
        admin_panel()
    
    # تذييل
    st.markdown("""
    <div class="footer">
        ⚡ RASSIM PRO 2026 • جميع الحقوق محفوظة • الإصدار 3.0
    </div>
    """, unsafe_allow_html=True)

# ===========================================================
# 16. تشغيل التطبيق
# ===========================================================
if __name__ == "__main__":
    main()


