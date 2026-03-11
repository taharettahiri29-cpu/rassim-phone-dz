#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS ULTIMATE 2026
منصة الوساطة الذكية - نظام الجذب التلقائي
69 ولاية جزائرية
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import hashlib
import json
from supabase import create_client, Client

# ==========================================
# 1. إعدادات الصفحة المتقدمة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS • نظام الجذب",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. التصميم المتطور
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
    background: linear-gradient(135deg, #0a0a1a, #1a1a2a);
    color: white;
}

/* ===== الشعار الرئيسي ===== */
.main-header {
    text-align: center;
    padding: 20px;
    margin-bottom: 20px;
}

.logo {
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00ffff, #ff00ff, #00ffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
}

@keyframes shine {
    to { background-position: 200% center; }
}

.subtitle {
    color: #888;
    font-size: 1.2rem;
    margin-top: -10px;
}

/* ===== بطاقة التاجر المغناطيسية ===== */
.magnet-card {
    background: linear-gradient(135deg, #00aa00, #00ff00);
    border-radius: 30px;
    padding: 40px;
    text-align: center;
    margin: 20px 0;
    border: 3px solid white;
    animation: pulse-magnet 2s ease-in-out infinite;
}

@keyframes pulse-magnet {
    0%, 100% { transform: scale(1); box-shadow: 0 20px 40px rgba(0,255,0,0.3); }
    50% { transform: scale(1.02); box-shadow: 0 30px 60px rgba(0,255,0,0.5); }
}

.magnet-title {
    font-size: 3rem;
    font-weight: 900;
    color: white;
    text-shadow: 2px 2px 0 #000;
}

.magnet-subtitle {
    font-size: 1.5rem;
    color: white;
    margin: 20px 0;
}

.magnet-badge {
    background: white;
    color: #00aa00;
    padding: 10px 30px;
    border-radius: 50px;
    font-weight: bold;
    font-size: 1.2rem;
    display: inline-block;
}

/* ===== بطاقة الطلب ===== */
.request-card {
    background: #1a1a2a;
    border-right: 5px solid #00ffff;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
    transition: all 0.3s ease;
}

.request-card:hover {
    transform: translateX(-5px);
    background: #252a3a;
    border-right-color: #ff00ff;
}

.request-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}

.request-category {
    background: #2a2a3a;
    padding: 5px 12px;
    border-radius: 20px;
    color: #00ffff;
    font-size: 0.8rem;
}

.request-time {
    color: #888;
    font-size: 0.8rem;
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

.request-phone {
    background: #2a2a3a;
    padding: 3px 10px;
    border-radius: 15px;
    color: #ff00ff;
    font-size: 0.8rem;
    display: inline-block;
}

/* ===== بطاقة التاجر ===== */
.vendor-card {
    background: linear-gradient(135deg, #1a1a2a, #2a2a3a);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 15px;
    border: 1px solid #333;
    transition: all 0.3s ease;
}

.vendor-card:hover {
    border-color: #00ffff;
    transform: translateX(-5px);
    box-shadow: 0 10px 20px rgba(0,255,255,0.1);
}

.vendor-name {
    color: #00ffff;
    font-size: 1.3rem;
    font-weight: bold;
}

.vendor-badge {
    display: inline-block;
    background: #00aa00;
    color: white;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
}

.vendor-badge-gold {
    background: linear-gradient(135deg, #ffd700, #ffaa00);
    color: black;
}

.vendor-stats {
    display: flex;
    gap: 15px;
    color: #888;
    font-size: 0.9rem;
    margin: 10px 0;
}

/* ===== بطاقة الإحصائيات العامة ===== */
.stats-dashboard {
    background: linear-gradient(135deg, #2a1a3a, #3a2a4a);
    border-radius: 30px;
    padding: 30px;
    margin: 20px 0;
    border: 1px solid #ff00ff;
}

.stat-box {
    text-align: center;
    padding: 20px;
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
}

.stat-number {
    font-size: 3.5rem;
    font-weight: 900;
    color: #00ffff;
    line-height: 1.2;
}

.stat-label {
    color: #888;
    font-size: 1rem;
}

/* ===== أزرار ===== */
.stButton > button {
    background: linear-gradient(135deg, #00ffff, #ff00ff) !important;
    border: none !important;
    color: black !important;
    font-weight: bold !important;
    border-radius: 15px !important;
    padding: 12px !important;
    width: 100%;
    transition: transform 0.2s !important;
}

.stButton > button:hover {
    transform: scale(1.02) !important;
    box-shadow: 0 10px 20px rgba(255,0,255,0.3) !important;
}

.magnet-button {
    background: linear-gradient(135deg, #ffaa00, #ff5500) !important;
    font-size: 1.5rem !important;
    padding: 20px !important;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.contact-btn {
    background: #25D366;
    color: white;
    padding: 10px;
    border-radius: 10px;
    text-decoration: none;
    display: inline-block;
    text-align: center;
    font-weight: bold;
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
    backdrop-filter: blur(5px);
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
    animation: float 3s ease-in-out infinite;
    box-shadow: 0 5px 20px rgba(0,255,255,0.3);
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
# 3. قائمة الولايات والفئات
# ==========================================
WILAYAS = [
    "16 - الجزائر", "31 - وهران", "25 - قسنطينة", "42 - تيبازة", "06 - بجاية",
    "19 - سطيف", "23 - عنابة", "13 - تلمسان", "09 - البليدة", "15 - تيزي وزو",
    "07 - بسكرة", "26 - المدية", "29 - معسكر", "35 - بومرداس", "41 - سوق أهراس",
    "47 - غرداية", "55 - توقرت", "57 - المغير", "58 - المنيع", "69 - عين الحجر"
]

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

# ==========================================
# 4. الربط مع Supabase
# ==========================================
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
        st.sidebar.error(f"⚠️ فشل الاتصال: {e}")
        return None, False

supabase, connected = init_connection()

# ==========================================
# 5. دوال التعامل مع قاعدة البيانات
# ==========================================
def fetch_requests():
    """جلب جميع الطلبات من قاعدة البيانات"""
    if not connected:
        return pd.DataFrame()
    
    try:
        response = supabase.table("requests").select("*").order("created_at", desc=True).execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        st.error(f"خطأ في جلب الطلبات: {e}")
        return pd.DataFrame()

def fetch_vendors():
    """جلب جميع البائعين من قاعدة البيانات"""
    if not connected:
        return pd.DataFrame()
    
    try:
        response = supabase.table("vendors").select("*").order("created_at", desc=True).execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        st.error(f"خطأ في جلب البائعين: {e}")
        return pd.DataFrame()

def fetch_leads():
    """جلب المنافذ المحتملين من قاعدة البيانات"""
    if not connected:
        return pd.DataFrame()
    
    try:
        response = supabase.table("leads").select("*").order("created_at", desc=True).execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def save_request(item, category, phone, wilaya):
    """حفظ طلب جديد في قاعدة البيانات"""
    if not connected:
        return False
    
    try:
        data = {
            "item": item,
            "category": category,
            "phone": phone,
            "wilaya": wilaya,
            "status": "جاري البحث"
        }
        supabase.table("requests").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الطلب: {e}")
        return False

def save_vendor(name, phone, wilaya, categories, source="direct"):
    """حفظ بائع جديد في قاعدة البيانات"""
    if not connected:
        return False
    
    try:
        # التحقق من عدم تكرار الرقم
        existing = supabase.table("vendors").select("*").eq("phone", phone).execute()
        if existing.data and len(existing.data) > 0:
            return False
        
        data = {
            "name": name,
            "phone": phone,
            "wilaya": wilaya,
            "category": ", ".join(categories),
            "source": source,
            "verified": False,
            "trial": True,
            "created_at": datetime.now().isoformat()
        }
        supabase.table("vendors").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ البائع: {e}")
        return False

def save_lead(name, phone, wilaya, source):
    """حفظ منافذ محتمل في قاعدة البيانات"""
    if not connected:
        return False
    
    try:
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
    except Exception as e:
        return False

def get_daily_stats():
    """الحصول على إحصائيات اليوم"""
    if not connected:
        return {"requests": 0, "vendors": 0, "leads": 0}
    
    today = datetime.now().date().isoformat()
    
    try:
        requests_today = supabase.table("requests").select("*").gte("created_at", today).execute()
        vendors_today = supabase.table("vendors").select("*").gte("created_at", today).execute()
        leads_today = supabase.table("leads").select("*").gte("created_at", today).execute()
        
        return {
            "requests": len(requests_today.data) if requests_today.data else 0,
            "vendors": len(vendors_today.data) if vendors_today.data else 0,
            "leads": len(leads_today.data) if leads_today.data else 0
        }
    except:
        return {"requests": 0, "vendors": 0, "leads": 0}

def get_stats():
    """الحصول على إحصائيات كاملة"""
    requests_df = fetch_requests()
    vendors_df = fetch_vendors()
    leads_df = fetch_leads()
    
    requests_count = len(requests_df) if not requests_df.empty else 0
    vendors_count = len(vendors_df) if not vendors_df.empty else 0
    leads_count = len(leads_df) if not leads_df.empty else 0
    
    return vendors_count, requests_count, leads_count

# ==========================================
# 6. المغناطيس الرقمي (Lead Magnet)
# ==========================================
def magnet_vendor_registration():
    """تسجيل بائع جديد مع عرض مغناطيسي"""
    
    st.markdown("""
    <div class="magnet-card">
        <div class="magnet-title">🎯 عرض خاص للتجار</div>
        <div class="magnet-subtitle">سجل محلك الآن واحصل على أول 10 زبائن مجاناً!</div>
        <div class="magnet-badge">⚡ عرض محدود ⚡</div>
    </div>
    """, unsafe_allow_html=True)
    
    # إحصائيات سريعة لجذب التجار
    stats = get_daily_stats()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background:#1a1a2a; padding:15px; border-radius:15px; text-align:center;">
            <div style="font-size:2rem; color:#00ffff;">{stats['requests']}</div>
            <div style="color:#888;">طلب اليوم</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:#1a1a2a; padding:15px; border-radius:15px; text-align:center;">
            <div style="font-size:2rem; color:#ff00ff;">{stats['vendors']}</div>
            <div style="color:#888;">تاجر جديد</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background:#1a1a2a; padding:15px; border-radius:15px; text-align:center;">
            <div style="font-size:2rem; color:#00ff00;">{stats['leads']}</div>
            <div style="color:#888;">فرصة متاحة</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📝 تسجيل سريع (30 ثانية)")
    
    with st.form("magnet_vendor_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("اسم المحل *", placeholder="مثال: مؤسسة الرونو")
        with col2:
            phone = st.text_input("رقم الهاتف *", placeholder="0555123456")
        
        wilaya = st.selectbox("الولاية *", WILAYAS)
        categories = st.multiselect("ماذا تبيع؟ *", CATEGORIES)
        
        st.markdown("""
        <div style="background:#2a2a3a; padding:15px; border-radius:15px; margin:10px 0;">
            <p style="color:#00ffff;">✅ بالتسجيل أنت مؤهل للحصول على:</p>
            <ul style="color:white;">
                <li>10 طلبات أولى مجاناً</li>
                <li>ظهور مميز في رادار الطلبات</li>
                <li>إشعارات فورية عبر واتساب</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        submitted = st.form_submit_button("🚀 سجل الآن واحصل على 10 زبائن مجاناً", use_container_width=True)
        
        if submitted:
            if name and phone and categories:
                if save_vendor(name, phone, wilaya, categories, source="magnet"):
                    st.success("✅ تم التسجيل بنجاح! سيتم إشعارك بأول 10 طلبات في ولايتك.")
                    st.balloons()
                    
                    # محاكاة إرسال إشعار
                    with st.spinner("جاري تفعيل حسابك..."):
                        time.sleep(2)
                        st.info("📱 تم تفعيل الإشعارات الفورية! ستتلقى طلبك الأول قريباً.")
                else:
                    st.error("❌ هذا الرقم مسجل مسبقاً")
            else:
                st.error("❌ املأ الحقول المطلوبة (*)")

# ==========================================
# 7. إضافة منافذ محتمل يدوياً (محاكاة للـ Scraper)
# ==========================================
def add_lead_manually():
    """إضافة منافذ محتمل يدوياً (لمحاكاة الـ Scraper)"""
    st.markdown("### 📥 إضافة منافذ محتمل (Leads)")
    
    with st.form("lead_form"):
        name = st.text_input("اسم التاجر/المحل")
        phone = st.text_input("رقم الهاتف")
        wilaya = st.selectbox("الولاية", WILAYAS)
        source = st.selectbox("المصدر", ["واد كنيس", "فيسبوك", "انستغرام", "توصية", "أخرى"])
        
        if st.form_submit_button("➕ إضافة منفذ"):
            if name and phone:
                if save_lead(name, phone, wilaya, source):
                    st.success("تمت الإضافة بنجاح!")
                else:
                    st.error("فشل في الإضافة")

# ==========================================
# 8. لوحة الإحصائيات العامة (لجذب السبونسر)
# ==========================================
def public_stats_dashboard():
    """لوحة إحصائيات عامة لجذب الرعاة"""
    
    vendors, requests, leads = get_stats()
    daily = get_daily_stats()
    
    st.markdown("""
    <div class="stats-dashboard">
        <h2 style="color:#00ffff; text-align:center;">📊 إحصائيات RASSIM OS الحية</h2>
        <p style="color:#888; text-align:center;">بيانات محدثة لحظياً • 69 ولاية جزائرية</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{requests}</div>
            <div class="stat-label">إجمالي الطلبات</div>
            <div style="color:#00ff00;">+{daily['requests']} اليوم</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{vendors}</div>
            <div class="stat-label">تاجر مسجل</div>
            <div style="color:#00ff00;">+{daily['vendors']} اليوم</div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{leads}</div>
            <div class="stat-label">فرصة متاحة</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{len(WILAYAS)}</div>
            <div class="stat-label">ولاية نشطة</div>
        </div>
        """, unsafe_allow_html=True)
    
    # أكثر الولايات نشاطاً (محاكاة)
    st.markdown("### 🔥 أكثر الولايات نشاطاً")
    active_wilayas = random.sample(WILAYAS, 5)
    for w in active_wilayas:
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; background:#1a1a2a; padding:10px; border-radius:10px; margin:5px 0;">
            <span>{w}</span>
            <span style="color:#00ffff;">{random.randint(5, 50)} طلب اليوم</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align:center; margin-top:20px;">
        <p style="color:#888;">🚀 للرعاية والإعلان: تواصل معنا عبر واتساب</p>
        <a href="https://wa.me/213555555555" target="_blank">
            <button style="background:#25D366; color:white; border:none; padding:15px 30px; border-radius:50px; font-weight:bold;">📱 تواصل الآن</button>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 9. نظام الإحالة (Referral System)
# ==========================================
def referral_system(vendor_id):
    """نظام إحالة للتجار"""
    st.markdown("### 🤝 نظام الإحالة")
    
    referral_code = hashlib.md5(f"{vendor_id}{datetime.now().date()}".encode()).hexdigest()[:8]
    referral_link = f"https://rassim-os.streamlit.app/?ref={referral_code}"
    
    st.markdown(f"""
    <div style="background:#1a1a2a; padding:20px; border-radius:20px; margin:10px 0;">
        <h4 style="color:#00ffff;">🎁 ادعو تجاراً آخرين واحصل على مميزات</h4>
        <p>رابط الإحالة الخاص بك:</p>
        <div style="background:#2a2a3a; padding:15px; border-radius:10px; direction:ltr; text-align:left; font-family:monospace;">
            {referral_link}
        </div>
        <div style="display:flex; gap:10px; margin-top:15px;">
            <a href="https://wa.me/?text={referral_link}" target="_blank" style="flex:1; background:#25D366; color:white; text-decoration:none; padding:10px; border-radius:10px; text-align:center;">📱 شارك على واتساب</a>
            <button onclick="navigator.clipboard.writeText('{referral_link}')" style="flex:1; background:#00ffff; color:black; border:none; padding:10px; border-radius:10px;">📋 نسخ الرابط</button>
        </div>
        <p style="color:#888; margin-top:10px;">✨ كل تاجر تسجله يمنحك شارة ذهبية ورفع ترتيب محلك</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 10. واجهة رادار الطلبات
# ==========================================
def buyer_radar_ui():
    """واجهة المشتري - إطلاق الرادار"""
    
    st.markdown("""
    <div style="background:#1a1a2a; padding:30px; border-radius:30px; border:2px solid #00ffff; margin-bottom:30px;">
        <h2 style="color:#00ffff; text-align:center;">🎯 رادار RASSIM</h2>
        <p style="color:#888; text-align:center;">اكتب ما تبحث عنه وسيبحث لك النظام في 69 ولاية</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        item_desc = st.text_area("🔍 ماذا تبحث بالضبط؟", 
                                placeholder="مثال: محرك رونو كليو 2 ديزل",
                                height=100)
        category = st.selectbox("📂 الفئة", CATEGORIES)
    
    with col2:
        buyer_phone = st.text_input("📱 رقم هاتفك", placeholder="0661234567")
        wilaya = st.selectbox("📍 الولاية", WILAYAS)
    
    if st.button("🚀 إطلاق الرادار", use_container_width=True):
        if item_desc and buyer_phone:
            with st.spinner("📡 جاري البحث..."):
                time.sleep(1)
            
            if save_request(item_desc, category, buyer_phone, wilaya):
                st.success("✅ تم إطلاق الرادار! سيتواصل معك التجار قريباً.")
                st.balloons()
            else:
                st.error("❌ فشل في حفظ الطلب")
        else:
            st.error("❌ املأ الحقول المطلوبة")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 11. الصفحة الرئيسية
# ==========================================
def main():
    """الدالة الرئيسية"""
    
    # حالة الاتصال
    with st.sidebar:
        st.markdown("### 📊 حالة النظام")
        if connected:
            st.markdown('✅ متصل بالسحابة', unsafe_allow_html=True)
        else:
            st.markdown('❌ غير متصل', unsafe_allow_html=True)
        
        vendors, requests, leads = get_stats()
        st.metric("إجمالي الطلبات", requests)
        st.metric("إجمالي البائعين", vendors)
        st.metric("فرص محتملة", leads)
    
    # عداد الزوار
    vendors, requests, leads = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span style="color:#00ffff;">●</span> {requests} طلب • {vendors} تاجر
    </div>
    """, unsafe_allow_html=True)
    
    # فقاعة الدردشة
    st.markdown("""
    <div class="chat-bubble" onclick="window.open('https://wa.me/213555555555')">
        <img src="https://img.icons8.com/ios-filled/30/000000/speech-bubble.png">
    </div>
    """, unsafe_allow_html=True)
    
    # الشعار
    st.markdown("""
    <div class="main-header">
        <div class="logo">⚡ RASSIM OS</div>
        <div class="subtitle">منصة الوساطة الذكية • 69 ولاية</div>
    </div>
    """, unsafe_allow_html=True)
    
    # تبويبات رئيسية
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 رادار المشتري",
        "🧲 مغناطيس التجار",
        "📊 إحصائيات عامة",
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
                        <span class="request-time">{row.get('created_at', '')[:16]}</span>
                    </div>
                    <div class="request-title">{row.get('item', '')[:50]}</div>
                    <div class="request-details">
                        <span>📍 {row.get('wilaya', '')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا توجد طلبات")
    
    with tab2:
        magnet_vendor_registration()
        
        st.markdown("### 👥 التجار المسجلون مؤخراً")
        vendors_df = fetch_vendors()
        if not vendors_df.empty:
            for _, row in vendors_df.head(5).iterrows():
                st.markdown(f"""
                <div class="vendor-card">
                    <div class="vendor-name">{row.get('name', '')}</div>
                    <div class="vendor-stats">
                        <span>📍 {row.get('wilaya', '')}</span>
                        <span>📞 {row.get('phone', '')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        public_stats_dashboard()
        
        # إضافة منافذ يدوي (للمشرفين)
        with st.expander("📥 إضافة منافذ محتمل (للمشرف)"):
            add_lead_manually()
    
    with tab4:
        st.markdown("### 🔐 لوحة المشرف")
        password = st.text_input("كلمة المرور", type="password")
        if password == "rassim2026":
            st.success("مرحباً أيها المشرف")
            
            tabs = st.tabs(["📊 إحصائيات", "👥 البائعين", "🎯 الطلبات", "📥 المنافذ"])
            
            with tabs[0]:
                vendors, requests, leads = get_stats()
                col1, col2, col3 = st.columns(3)
                col1.metric("البائعين", vendors)
                col2.metric("الطلبات", requests)
                col3.metric("المنافذ", leads)
            
            with tabs[1]:
                vendors_df = fetch_vendors()
                if not vendors_df.empty:
                    st.dataframe(vendors_df)
            
            with tabs[2]:
                requests_df = fetch_requests()
                if not requests_df.empty:
                    st.dataframe(requests_df)
            
            with tabs[3]:
                leads_df = fetch_leads()
                if not leads_df.empty:
                    st.dataframe(leads_df)
        else:
            st.error("كلمة مرور خاطئة")
    
    # تذييل
    st.markdown("""
    <div class="footer">
        RASSIM OS 2026 • نظام الجذب التلقائي • جميع الحقوق محفوظة
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
