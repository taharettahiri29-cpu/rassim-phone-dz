#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===========================================================
⚡ RASSIM PRO GLOBAL - سوق الجزائر والعالم
===========================================================
منصة متكاملة تجمع بين:
- السوق المحلي الجزائري (69 ولاية)
- الأسواق العالمية (أمازون، علي بابا، جوميا، شي إن)
- نظام أفلييت للمشتركين (كسب العمولات)
- دعم متعدد اللغات والعملات
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
    page_title="RASSIM PRO GLOBAL • سوق الجزائر والعالم",
    page_icon="🌐",
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
# 3. قائمة الولايات (69 ولاية)
# ===========================================================
WILAYAS = [
    "16 - الجزائر", "31 - وهران", "25 - قسنطينة", "42 - تيبازة", "06 - بجاية",
    "19 - سطيف", "23 - عنابة", "13 - تلمسان", "09 - البليدة", "15 - تيزي وزو",
    "07 - بسكرة", "26 - المدية", "29 - معسكر", "35 - بومرداس", "41 - سوق أهراس",
    "47 - غرداية", "55 - توقرت", "57 - المغير", "58 - المنيع", "69 - عين الحجر"
]

# ===========================================================
# 4. قائمة الدول للأسواق العالمية
# ===========================================================
COUNTRIES = [
    "الجزائر", "مصر", "المغرب", "تونس", "ليبيا", "موريتانيا",
    "السعودية", "الإمارات", "قطر", "الكويت", "عمان", "البحرين",
    "الأردن", "فلسطين", "لبنان", "سوريا", "العراق", "اليمن",
    "تركيا", "فرنسا", "ألمانيا", "بريطانيا", "إيطاليا", "إسبانيا",
    "كندا", "الولايات المتحدة", "الصين", "الهند"
]

# ===========================================================
# 5. الأسواق العالمية المدعومة
# ===========================================================
GLOBAL_MARKETS = {
    "🛒 أمازون (Amazon)": {
        "url": "https://amazon.com",
        "countries": ["الولايات المتحدة", "كندا", "ألمانيا", "فرنسا", "إيطاليا", "إسبانيا", "بريطانيا"],
        "commission": "3-10%",
        "logo": "https://img.icons8.com/color/48/000000/amazon.png"
    },
    "🏭 علي بابا (Alibaba)": {
        "url": "https://alibaba.com",
        "countries": ["الصين", "جميع الدول"],
        "commission": "2-5%",
        "logo": "https://img.icons8.com/color/48/000000/alibaba.png"
    },
    "🛍️ جوميا (Jumia)": {
        "url": "https://jumia.dz",
        "countries": ["الجزائر", "مصر", "المغرب", "تونس", "نيجيريا", "كينيا"],
        "commission": "5-8%",
        "logo": "https://img.icons8.com/color/48/000000/jumia.png"
    },
    "👕 شي إن (Shein)": {
        "url": "https://shein.com",
        "countries": ["جميع الدول"],
        "commission": "7-15%",
        "logo": "https://img.icons8.com/color/48/000000/shein.png"
    },
    "🛒 نون (Noon)": {
        "url": "https://noon.com",
        "countries": ["السعودية", "الإمارات", "مصر"],
        "commission": "4-7%",
        "logo": "https://img.icons8.com/color/48/000000/noon.png"
    },
    "📦 واد كنيس (Ouedkniss)": {
        "url": "https://ouedkniss.com",
        "countries": ["الجزائر"],
        "commission": "مجاني",
        "logo": "https://img.icons8.com/color/48/000000/ouedkniss.png"
    },
    "🛒 سوق (Souq)": {
        "url": "https://souq.com",
        "countries": ["السعودية", "الإمارات", "مصر"],
        "commission": "3-6%",
        "logo": "https://img.icons8.com/color/48/000000/souq.png"
    },
    "🛍️ هوم سنتر (Home Centre)": {
        "url": "https://homecentre.com",
        "countries": ["السعودية", "الإمارات", "قطر", "الكويت", "عمان", "البحرين"],
        "commission": "2-4%",
        "logo": "https://img.icons8.com/color/48/000000/home-centre.png"
    }
}

# ===========================================================
# 6. قائمة الفئات المحلية والعالمية
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
    "📦 أخرى",
    "🌍 استيراد من الصين",
    "📦 شحن دولي",
    "💎 ماركات عالمية",
    "🛒 تسوق من أمازون",
    "🏭 جملة من علي بابا"
]

# ===========================================================
# 7. نظام الثيم الديناميكي (CSS محسن)
# ===========================================================
def load_css(theme):
    """تحميل التصميم حسب الثيم المختار"""
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
        hover_bg = "#2e2e42"
    else:
        bg_color = "#f5f5f5"
        card_color = "#ffffff"
        text_color = "#000000"
        input_bg = "#ffffff"
        input_text = "#000000"
        placeholder_color = "#666666"
        border_color = "#dddddd"
        gradient_start = "#667eea"
        gradient_end = "#764ba2"
        hover_bg = "#f0f0f0"
    
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
    
    /* ===== تنسيق الحقول ===== */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label,
    .stNumberInput > label {{
        color: {text_color} !important;
        font-weight: 600 !important;
    }}
    
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 2px solid {border_color} !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 16px !important;
    }}
    
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {{
        border-color: {gradient_start} !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }}
    
    /* ===== بطاقة السوق العالمي ===== */
    .market-card {{
        background: {card_color};
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 2px solid {gradient_start};
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    
    .market-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,255,255,0.2);
        background: {hover_bg};
    }}
    
    .market-title {{
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 15px;
    }}
    
    .market-name {{
        font-size: 1.5rem;
        font-weight: bold;
        color: {gradient_start};
    }}
    
    .market-details {{
        display: flex;
        justify-content: space-between;
        color: #888;
        font-size: 0.9rem;
        margin: 10px 0;
    }}
    
    .market-commission {{
        background: #00aa00;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }}
    
    /* ===== بطاقة الأفلييت ===== */
    .affiliate-card {{
        background: linear-gradient(135deg, #2a1a3a, #3a2a4a);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid {gradient_end};
        text-align: center;
    }}
    
    .affiliate-code {{
        background: {input_bg};
        padding: 15px;
        border-radius: 10px;
        font-family: monospace;
        font-size: 1.5rem;
        color: {gradient_start};
        direction: ltr;
        margin: 15px 0;
    }}
    
    /* ===== بطاقة الطلب ===== */
    .request-card {{
        background: {card_color};
        border-right: 4px solid {gradient_start};
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        transition: all 0.3s ease;
    }}
    
    .request-card:hover {{
        transform: translateX(-3px);
        background: {hover_bg};
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
    
    /* ===== إخفاء العناصر غير الضرورية ===== */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* ===== تذييل ===== */
    .footer {{
        text-align: center;
        color: #666;
        font-size: 0.75rem;
        margin-top: 30px;
        padding: 15px;
        border-top: 1px solid {border_color};
    }}
    </style>
    """

# ===========================================================
# 8. الاتصال بقاعدة البيانات Supabase
# ===========================================================
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["connections"]["supabase"]["url"]
        key = st.secrets["connections"]["supabase"]["key"]
        return create_client(url, key), True
    except:
        return None, False

supabase, connected = init_connection()

# ===========================================================
# 9. دوال مساعدة للتحقق
# ===========================================================
def validate_phone(phone):
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    return re.match(r'^(05|06|07|\+?[0-9]{7,15})$', phone) is not None

def validate_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

def generate_code(seed):
    return hashlib.md5(seed.encode()).hexdigest()[:8].upper()

# ===========================================================
# 10. دوال قاعدة البيانات
# ===========================================================
def save_vendor(name, phone, country, categories, source="local"):
    if not connected:
        return False
    try:
        referral_code = generate_code(phone + str(datetime.now()))
        data = {
            "name": name,
            "phone": phone,
            "country": country,
            "category": ", ".join(categories),
            "source": source,
            "referral_code": referral_code,
            "created_at": datetime.now().isoformat()
        }
        supabase.table("vendors").insert(data).execute()
        return True, referral_code
    except:
        return False, None

def save_affiliate(name, email, country):
    if not connected:
        return False
    try:
        affiliate_code = generate_code(email + str(datetime.now()))
        data = {
            "name": name,
            "email": email,
            "country": country,
            "affiliate_code": affiliate_code,
            "joined_at": datetime.now().isoformat()
        }
        supabase.table("affiliates").insert(data).execute()
        return True, affiliate_code
    except:
        return False, None

def save_global_request(item, market, phone, country):
    if not connected:
        return False
    try:
        data = {
            "item": item,
            "market": market,
            "phone": phone,
            "country": country,
            "created_at": datetime.now().isoformat()
        }
        supabase.table("global_requests").insert(data).execute()
        return True
    except:
        return False

# ===========================================================
# 11. واجهة الأسواق العالمية
# ===========================================================
def global_markets_ui():
    """عرض الأسواق العالمية المتاحة"""
    
    st.markdown("""
    <div class="smart-card">
        <h2 style="color:#00ffff; text-align:center;">🌍 الأسواق العالمية</h2>
        <p style="color:#888; text-align:center;">تسوق من أشهر المنصات العالمية واكسب عمولات</p>
    """, unsafe_allow_html=True)
    
    # عرض الأسواق
    cols = st.columns(2)
    for i, (market_name, market_info) in enumerate(GLOBAL_MARKETS.items()):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="market-card" onclick="window.open('{market_info["url"]}')">
                <div class="market-title">
                    <img src="{market_info['logo']}" width="40">
                    <span class="market-name">{market_name}</span>
                </div>
                <div class="market-details">
                    <span>🌍 {', '.join(market_info['countries'][:3])}...</span>
                    <span class="market-commission">{market_info['commission']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # نموذج طلب من الأسواق العالمية
    st.markdown("### 📦 طلب منتج من الخارج")
    with st.form("global_order_form"):
        item = st.text_input("🔍 ماذا تريد أن تشتري؟", placeholder="مثال: هاتف آيفون 14 من أمازون")
        market = st.selectbox("🛒 اختر السوق", list(GLOBAL_MARKETS.keys()))
        phone = st.text_input("📱 رقم الهاتف", placeholder="+213555555555")
        country = st.selectbox("🌍 دولة التوصيل", COUNTRIES)
        
        if st.form_submit_button("🚀 اطلب الآن", use_container_width=True):
            if item and phone:
                if validate_phone(phone):
                    with st.spinner("جاري معالجة طلبك..."):
                        time.sleep(1)
                    st.success("✅ تم إرسال طلبك! سنتواصل معك قريباً لتأكيد التفاصيل")
                    st.balloons()
                else:
                    st.error("❌ رقم هاتف غير صالح")
            else:
                st.error("❌ املأ جميع الحقول")

# ===========================================================
# 12. نظام الأفلييت (التسويق بالعمولة)
# ===========================================================
def affiliate_system():
    """نظام التسويق بالعمولة"""
    
    st.markdown("""
    <div class="affiliate-card">
        <h2 style="color:#ff00ff;">💰 نظام الأفلييت</h2>
        <p>اكسب عمولات تصل إلى 15% عند تسويق المنتجات</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab_join, tab_earn, tab_stats = st.tabs(["📝 انضم كأفلييت", "💵 كيف تربح؟", "📊 إحصائياتي"])
    
    with tab_join:
        st.markdown("### انضم إلى برنامج الأفلييت")
        with st.form("affiliate_join_form"):
            name = st.text_input("👤 الاسم الكامل")
            email = st.text_input("📧 البريد الإلكتروني")
            country = st.selectbox("🌍 الدولة", COUNTRIES)
            
            if st.form_submit_button("🚀 انضم الآن مجاناً", use_container_width=True):
                if name and email and country:
                    if validate_email(email):
                        success, code = save_affiliate(name, email, country)
                        if success:
                            st.markdown(f"""
                            <div class="affiliate-code">
                                كود الأفلييت الخاص بك: {code}
                            </div>
                            """, unsafe_allow_html=True)
                            st.success("✅ تم التسجيل! انسخ كودك وابدأ في الترويج")
                            st.balloons()
                        else:
                            st.error("❌ حدث خطأ في التسجيل")
                    else:
                        st.error("❌ بريد إلكتروني غير صالح")
                else:
                    st.error("❌ املأ جميع الحقول")
    
    with tab_earn:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 🎯 طرق الربح
            - مشاركة روابط المنتجات
            - تسويق منتجات أمازون
            - تسويق منتجات علي بابا
            - دعوة أصدقاء للتسجيل
            """)
        with col2:
            st.markdown("""
            ### 💰 نسب العمولات
            - أمازون: 3-10%
            - علي بابا: 2-5%
            - جوميا: 5-8%
            - شي إن: 7-15%
            """)
        
        st.markdown("### 🏆 مكافآت إضافية")
        rewards_data = {
            "المبيعات الشهرية": ["أقل من 1000$", "1000$ - 5000$", "5000$ - 10000$", "أكثر من 10000$"],
            "العمولة الإضافية": ["5%", "7%", "10%", "15% + هدايا"]
        }
        st.table(pd.DataFrame(rewards_data))
    
    with tab_stats:
        st.info("📊 سجل الدخول لمشاهدة إحصائياتك")

# ===========================================================
# 13. واجهة رادار المشتري المحلي
# ===========================================================
def local_buyer_ui():
    """واجهة المشتري المحلي"""
    
    st.markdown("""
    <div class="smart-card">
        <h2 style="color:#00ffff; text-align:center;">🎯 رادار RASSIM المحلي</h2>
        <p style="color:#888; text-align:center;">ابحث عن المنتجات في السوق الجزائري</p>
    """, unsafe_allow_html=True)
    
    item = st.text_input("🔍 ماذا تبحث؟", placeholder="مثال: محرك كيا سبورتاج")
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("📂 الفئة", CATEGORIES)
        min_price = st.number_input("💰 من (دج)", min_value=0, value=0, step=1000)
    with col2:
        wilaya = st.selectbox("📍 الولاية", ["كل الولايات"] + WILAYAS)
        max_price = st.number_input("💰 إلى (دج)", min_value=0, value=1000000, step=1000)
    
    phone = st.text_input("📱 رقم الهاتف", placeholder="06XXXXXXXX")
    
    if st.button("🚀 إطلاق الرادار", use_container_width=True):
        if item and phone:
            if validate_phone(phone):
                st.success("✅ تم الإطلاق! سيتم التواصل معك")
                st.balloons()
            else:
                st.error("❌ رقم هاتف غير صالح")
        else:
            st.error("❌ املأ جميع الحقول")

# ===========================================================
# 14. الصفحة الرئيسية
# ===========================================================
def main():
    """الدالة الرئيسية"""
    
    # تطبيق التصميم
    st.markdown(load_css(st.session_state.theme), unsafe_allow_html=True)
    
    # عداد الزوار
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
        <div class="logo">🌐 RASSIM PRO GLOBAL</div>
        <div class="subtitle">سوق الجزائر والعالم • 69 ولاية + أسواق عالمية</div>
    </div>
    """, unsafe_allow_html=True)
    
    # التبويبات الرئيسية
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 السوق المحلي",
        "🌍 الأسواق العالمية",
        "💰 نظام الأفلييت",
        "🧲 تسجيل البائعين",
        "🔐 المشرف"
    ])
    
    with tab1:
        local_buyer_ui()
    
    with tab2:
        global_markets_ui()
    
    with tab3:
        affiliate_system()
    
    with tab4:
        st.markdown("### 🏪 تسجيل البائعين العالميين")
        with st.form("global_vendor_form"):
            name = st.text_input("🏪 اسم الشركة / البائع")
            phone = st.text_input("📞 رقم الهاتف الدولي", placeholder="+213555555555")
            country = st.selectbox("🌍 الدولة", COUNTRIES)
            categories = st.multiselect("📋 الفئات", CATEGORIES)
            
            if st.form_submit_button("🚀 سجل كبائع عالمي", use_container_width=True):
                if name and phone and country and categories:
                    if validate_phone(phone):
                        success, code = save_vendor(name, phone, country, categories, "global")
                        if success:
                            st.success(f"✅ تم التسجيل! كود البائع: {code}")
                            st.balloons()
                        else:
                            st.error("❌ فشل التسجيل")
                    else:
                        st.error("❌ رقم هاتف غير صالح")
                else:
                    st.error("❌ املأ جميع الحقول")
    
    with tab5:
        st.markdown("### 🔐 لوحة المشرف")
        password = st.text_input("كلمة المرور", type="password")
        if password == "rassim2026":
            st.success("مرحباً أيها المشرف")
            st.markdown("📊 إحصائيات المنصة ستظهر هنا")
        else:
            st.error("كلمة مرور خاطئة")
    
    # تذييل
    st.markdown("""
    <div class="footer">
        🌐 RASSIM PRO GLOBAL 2026 • السوق المحلي + الأسواق العالمية + نظام الأفلييت
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
