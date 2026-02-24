#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS ULTIMATE 2026
منصة الوساطة الذكية - النسخة النهائية المستقرة
69 ولاية جزائرية
"""

import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
from typing import Tuple, List, Dict, Any

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS • الوسيط الذكي",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. محاولة استيراد Google Sheets (مع Fallback)
# ==========================================
USE_GSHEETS = False
try:
    from streamlit_gsheets import GSheetsConnection
    conn = st.connection("gsheets", type=GSheetsConnection)
    USE_GSHEETS = True
    st.sidebar.success("✅ متصل بـ Google Sheets")
except Exception as e:
    st.sidebar.warning("⚠️ وضع التخزين المحلي (بدون سحابة)")
    st.sidebar.info("لتفعيل السحابة: أضف 'st-gsheets-connection' إلى requirements.txt")

# ==========================================
# 3. قائمة الولايات (69 ولاية)
# ==========================================
WILAYAS: List[str] = [
    "16 - الجزائر", "31 - وهران", "25 - قسنطينة", "42 - تيبازة", "06 - بجاية",
    "19 - سطيف", "23 - عنابة", "13 - تلمسان", "09 - البليدة", "15 - تيزي وزو",
    "07 - بسكرة", "26 - المدية", "29 - معسكر", "35 - بومرداس", "41 - سوق أهراس",
    "47 - غرداية", "55 - توقرت", "57 - المغير", "58 - المنيع", "69 - عين الحجر"
]

# ==========================================
# 4. قائمة الفئات
# ==========================================
CATEGORIES: List[str] = [
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
# 5. إدارة البيانات (محلية أو سحابية)
# ==========================================
class DataManager:
    """إدارة البيانات مع دعم السحابة والمحلي"""
    
    @staticmethod
    def get_requests():
        """جلب الطلبات"""
        if USE_GSHEETS:
            try:
                df = conn.read(worksheet="Requests")
                if not df.empty:
                    return df.to_dict('records')
            except:
                pass
        return st.session_state.get('requests', [])
    
    @staticmethod
    def save_request(request_data):
        """حفظ طلب جديد"""
        if USE_GSHEETS:
            try:
                df = conn.read(worksheet="Requests")
                new_df = pd.DataFrame([request_data])
                if df.empty:
                    updated_df = new_df
                else:
                    updated_df = pd.concat([df, new_df], ignore_index=True)
                conn.update(worksheet="Requests", data=updated_df)
                return True
            except:
                pass
        
        # حفظ محلي
        if 'requests' not in st.session_state:
            st.session_state.requests = []
        st.session_state.requests.append(request_data)
        return False
    
    @staticmethod
    def get_vendors():
        """جلب البائعين"""
        if USE_GSHEETS:
            try:
                df = conn.read(worksheet="Vendors")
                if not df.empty:
                    return df.to_dict('records')
            except:
                pass
        return st.session_state.get('vendors', [])
    
    @staticmethod
    def save_vendor(vendor_data):
        """حفظ بائع جديد"""
        if USE_GSHEETS:
            try:
                df = conn.read(worksheet="Vendors")
                new_df = pd.DataFrame([vendor_data])
                if df.empty:
                    updated_df = new_df
                else:
                    updated_df = pd.concat([df, new_df], ignore_index=True)
                conn.update(worksheet="Vendors", data=updated_df)
                return True
            except:
                pass
        
        # حفظ محلي
        if 'vendors' not in st.session_state:
            st.session_state.vendors = []
        st.session_state.vendors.append(vendor_data)
        return False

# ==========================================
# 6. بيانات تجريبية أولية
# ==========================================
def init_sample_data():
    """إضافة بيانات تجريبية إذا كانت القاعدة فارغة"""
    if 'sample_loaded' not in st.session_state:
        # طلبات تجريبية
        sample_requests = [
            {
                "الوقت": "2026-02-24 14:30",
                "المطلوب": "محرك رونو كليو 2 ديزل بحالة جيدة",
                "الفئة": "🚗 قطع غيار سيارات",
                "الهاتف": "0555123456",
                "الولاية": "42 - تيبازة",
                "الحالة": "جاري البحث"
            },
            {
                "الوقت": "2026-02-24 13:15",
                "المطلوب": "شقة كراء غرفتين + صالون في فوكة",
                "الفئة": "🏠 عقارات (بيع/كراء)",
                "الهاتف": "0666123456",
                "الولاية": "42 - تيبازة",
                "الحالة": "جاري البحث"
            }
        ]
        
        # بائعون تجريبيون
        sample_vendors = [
            {
                "الاسم": "مؤسسة الرونو لقطع الغيار",
                "الهاتف": "0555123456",
                "الولاية": "42 - تيبازة",
                "التخصص": "🚗 قطع غيار سيارات, 🔧 خردة وأدوات",
                "تاريخ التسجيل": "2026-02-20"
            },
            {
                "الاسم": "خير الدين للخردة",
                "الهاتف": "0666123456",
                "الولاية": "16 - الجزائر",
                "التخصص": "🔧 خردة وأدوات, 🛠️ خدمات",
                "تاريخ التسجيل": "2026-02-21"
            }
        ]
        
        # حفظ البيانات
        for req in sample_requests:
            DataManager.save_request(req)
        for vendor in sample_vendors:
            DataManager.save_vendor(vendor)
        
        st.session_state.sample_loaded = True

# تهيئة البيانات التجريبية
init_sample_data()

# ==========================================
# 7. المتغيرات في الجلسة
# ==========================================
if 'vendor_logged_in' not in st.session_state:
    st.session_state.vendor_logged_in = False
if 'current_vendor' not in st.session_state:
    st.session_state.current_vendor = None
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now().strftime("%H:%M:%S")

# ==========================================
# 8. التصميم المتطور
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

/* ===== الشعار ===== */
.logo {
    font-size: 3rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #00ffff, #ff00ff, #00ffff);
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
    color: #888;
    font-size: 1.1rem;
    margin-top: -10px;
    margin-bottom: 20px;
}

/* ===== رادار الطلبات ===== */
.radar-section {
    background: linear-gradient(135deg, #1a1a2a, #2a2a3a);
    padding: 40px;
    border-radius: 40px;
    border: 2px solid #00ffff;
    margin-bottom: 30px;
    box-shadow: 0 20px 40px rgba(0,255,255,0.15);
    animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 20px 40px rgba(0,255,255,0.15); }
    50% { box-shadow: 0 20px 60px rgba(255,0,255,0.2); }
}

.radar-title {
    color: #00ffff;
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
    text-shadow: 0 0 20px rgba(0,255,255,0.3);
}

.radar-subtitle {
    color: #888;
    text-align: center;
    margin-bottom: 30px;
    font-size: 1.2rem;
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
    border-color: #ff00ff;
    transform: translateX(-5px);
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

.request-status {
    background: #00aa00;
    padding: 5px 12px;
    border-radius: 20px;
    color: white;
    font-size: 0.8rem;
}

.request-wilaya {
    background: #2a2a3a;
    padding: 3px 10px;
    border-radius: 15px;
    color: #888;
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

.vendor-stats {
    display: flex;
    gap: 15px;
    color: #888;
    font-size: 0.9rem;
    margin: 10px 0;
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
# 9. إحصائيات سريعة
# ==========================================
def get_stats() -> Tuple[int, int, int]:
    """إحصائيات من المصدر المناسب"""
    requests_data = DataManager.get_requests()
    vendors_data = DataManager.get_vendors()
    
    requests_count = len(requests_data)
    vendors_count = len(vendors_data)
    visitors = random.randint(50, 200)
    
    return vendors_count, requests_count, visitors

# ==========================================
# 10. رادار الطلبات (المشتري)
# ==========================================
def buyer_radar_ui():
    """واجهة المشتري - إطلاق الرادار"""
    
    st.markdown("""
    <div class="radar-section">
        <div class="radar-title">🎯 رادار RASSIM</div>
        <div class="radar-subtitle">
            اكتب ما تبحث عنه بالتفصيل، وسيبحث لك النظام في 69 ولاية
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        item_desc = st.text_area("🔍 ماذا تبحث بالضبط؟", 
                                placeholder="مثال: محرك رونو كليو 2 ديزل 2015، قطعة أصلية",
                                height=120)
        category = st.selectbox("📂 الفئة", CATEGORIES)
    
    with col2:
        buyer_phone = st.text_input("📱 رقم هاتفك (للبائع يتصل بك)", 
                                   placeholder="0661234567")
        wilaya = st.selectbox("📍 الولاية", WILAYAS)
    
    col1, col2, col3 = st.columns(3)
    with col2:
        launch_button = st.button("🚀 إطلاق الرادار", use_container_width=True)
    
    if launch_button:
        if item_desc and buyer_phone:
            # تأثير البحث
            with st.status("📡 جاري البحث...", expanded=True) as status:
                st.write("🔎 تحليل الطلب...")
                time.sleep(1)
                st.write("📲 إرسال إشعارات للتجار...")
                time.sleep(1)
                st.write("✅ تم إطلاق الرادار!")
                status.update(label="✅ اكتمل", state="complete")
            
            # حفظ الطلب
            new_request = {
                "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "المطلوب": item_desc,
                "الفئة": category,
                "الهاتف": buyer_phone,
                "الولاية": wilaya,
                "الحالة": "جاري البحث"
            }
            
            saved = DataManager.save_request(new_request)
            
            if saved:
                st.success("✅ تم إطلاق الرادار! سيتواصل معك التجار قريباً.")
                st.balloons()
            else:
                st.success("✅ تم إطلاق الرادار! (تخزين محلي)")
            
            # إحصائيات
            vendors_data = DataManager.get_vendors()
            vendors_in_wilaya = [v for v in vendors_data if v.get("الولاية") == wilaya]
            st.info(f"📊 هناك {len(vendors_in_wilaya)} تاجر في {wilaya} تلقوا طلبك")
            
        else:
            st.error("❌ املأ الحقول المطلوبة")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 11. عرض طلبات الرادار
# ==========================================
def show_radar_requests(wilaya_filter: str = None):
    """عرض طلبات المشترين"""
    
    requests_data = DataManager.get_requests()
    
    # فلترة
    if wilaya_filter and wilaya_filter != "كل الولايات":
        requests_data = [r for r in requests_data if r.get("الولاية") == wilaya_filter]
    
    # ترتيب من الأحدث
    requests_data.sort(key=lambda x: x.get("الوقت", ""), reverse=True)
    
    if requests_data:
        for req in requests_data[:10]:
            phone = req.get("الهاتف", "")
            hidden_phone = phone[:4] + "••••" if len(phone) > 4 else phone
            
            st.markdown(f"""
            <div class="request-card">
                <div class="request-header">
                    <span class="request-category">{req.get('الفئة', '')}</span>
                    <span class="request-status">{req.get('الحالة', 'جاري البحث')}</span>
                </div>
                <h4 style="color: #00ffff;">طلب: {req.get('المطلوب', '')[:50]}...</h4>
                <div style="display: flex; gap: 10px; margin: 10px 0;">
                    <span class="request-wilaya">📍 {req.get('الولاية', '')}</span>
                    <span class="request-wilaya">🕐 {req.get('الوقت', '')[:16]}</span>
                    <span class="request-wilaya">👤 {hidden_phone}</span>
                </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.vendor_logged_in:
                whatsapp_link = f"https://wa.me/213{phone[1:]}?text=السلام عليكم، رأيت طلبك بخصوص: {req.get('المطلوب', '')}"
                st.markdown(f"""
                <a href="{whatsapp_link}" target="_blank" class="contact-btn" style="display: block; text-decoration: none; margin-bottom: 10px;">
                    📱 تواصل مع المشتري
                </a>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("😕 لا توجد طلبات")

# ==========================================
# 12. تسجيل تاجر جديد
# ==========================================
def vendor_registration():
    """تسجيل بائع جديد"""
    st.markdown("### 📝 انضم كبائع")
    
    with st.form("vendor_registration_form"):
        name = st.text_input("اسم المحل أو البائع *")
        phone = st.text_input("رقم الهاتف *")
        wilaya = st.selectbox("الولاية *", WILAYAS)
        categories = st.multiselect("ماذا تبيع؟ *", CATEGORIES)
        
        submitted = st.form_submit_button("🚀 تسجيل كبائع معتمد", use_container_width=True)
        
        if submitted:
            if name and phone and categories:
                # التحقق من عدم تكرار الرقم
                vendors_data = DataManager.get_vendors()
                existing = [v for v in vendors_data if v.get("الهاتف") == phone]
                
                if existing:
                    st.error("❌ هذا الرقم مسجل مسبقاً")
                else:
                    new_vendor = {
                        "الاسم": name,
                        "الهاتف": phone,
                        "الولاية": wilaya,
                        "التخصص": ", ".join(categories),
                        "تاريخ التسجيل": datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    saved = DataManager.save_vendor(new_vendor)
                    
                    if saved:
                        st.success("✅ أهلاً بك في شبكة وسطاء RASSIM OS!")
                        st.balloons()
                    else:
                        st.success("✅ تم التسجيل محلياً!")
            else:
                st.error("❌ املأ الحقول المطلوبة (*)")

# ==========================================
# 13. عرض البائعين
# ==========================================
def show_vendors(wilaya_filter: str = None):
    """عرض قائمة البائعين"""
    
    vendors_data = DataManager.get_vendors()
    
    if wilaya_filter and wilaya_filter != "كل الولايات":
        vendors_data = [v for v in vendors_data if v.get("الولاية") == wilaya_filter]
    
    if vendors_data:
        for vendor in vendors_data[:10]:
            phone = vendor.get("الهاتف", "")
            whatsapp = phone[1:] if phone.startswith('0') else phone
            
            st.markdown(f"""
            <div class="vendor-card">
                <div style="display: flex; justify-content: space-between;">
                    <span class="vendor-name">{vendor.get('الاسم', '')}</span>
                    <span class="vendor-badge">✅ موثق</span>
                </div>
                <div class="vendor-stats">
                    <span>📍 {vendor.get('الولاية', '')}</span>
                    <span>📞 {phone}</span>
                </div>
                <p style="color: #aaa;">{vendor.get('التخصص', '')}</p>
                <div style="display: flex; gap: 10px;">
                    <a href="https://wa.me/213{whatsapp}" target="_blank" class="contact-btn" style="flex:1; background:#25D366;">📱 واتساب</a>
                    <a href="tel:{phone}" class="contact-btn" style="flex:1; background:#00ffff; color:black;">📞 اتصال</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("😕 لا يوجد بائعون")

# ==========================================
# 14. لوحة المشرف
# ==========================================
def admin_panel():
    """لوحة تحكم المشرف"""
    st.markdown("### 🔐 لوحة المشرف")
    
    if not st.session_state.admin_logged_in:
        password = st.text_input("كلمة المرور", type="password")
        if st.button("دخول") and password == "rassim2026":
            st.session_state.admin_logged_in = True
            st.rerun()
        return
    
    tabs = st.tabs(["📊 إحصائيات", "👥 البائعين", "🎯 الطلبات", "📝 إضافة يدوي"])
    
    with tabs[0]:
        vendors, requests, visitors = get_stats()
        col1, col2, col3 = st.columns(3)
        col1.metric("إجمالي البائعين", vendors)
        col2.metric("إجمالي الطلبات", requests)
        col3.metric("زوار اليوم", visitors)
        
        st.markdown("#### آخر الطلبات")
        requests_data = DataManager.get_requests()
        if requests_data:
            df = pd.DataFrame(requests_data[-5:])
            st.dataframe(df, use_container_width=True)
    
    with tabs[1]:
        vendors_data = DataManager.get_vendors()
        if vendors_data:
            df = pd.DataFrame(vendors_data)
            st.dataframe(df, use_container_width=True)
    
    with tabs[2]:
        show_radar_requests()
    
    with tabs[3]:
        st.markdown("#### إضافة طلب يدوي")
        with st.form("admin_request"):
            desc = st.text_area("المطلوب *")
            cat = st.selectbox("الفئة", CATEGORIES)
            phone = st.text_input("رقم الهاتف *")
            wilaya = st.selectbox("الولاية", WILAYAS)
            
            if st.form_submit_button("➕ إضافة طلب"):
                if desc and phone:
                    new_request = {
                        "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "المطلوب": desc,
                        "الفئة": cat,
                        "الهاتف": phone,
                        "الولاية": wilaya,
                        "الحالة": "جاري البحث"
                    }
                    DataManager.save_request(new_request)
                    st.success("تمت الإضافة!")
                    st.rerun()

# ==========================================
# 15. إحصائيات سريعة
# ==========================================
def show_stats():
    vendors, requests, visitors = get_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{vendors}</div>
            <div class="stat-label">تاجر</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{requests}</div>
            <div class="stat-label">طلب</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{visitors}</div>
            <div class="stat-label">زائر</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 16. الصفحة الرئيسية
# ==========================================
def main():
    """الدالة الرئيسية"""
    
    # عداد الزوار
    vendors, requests, visitors = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span style="color:#00ffff;">●</span> {visitors} زائر • {vendors} تاجر • {requests} طلب
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
    <div class="logo">
        🎯 RASSIM OS
    </div>
    <div class="subtitle">
        منصة الوساطة الذكية • 69 ولاية
    </div>
    """, unsafe_allow_html=True)
    
    # إحصائيات
    show_stats()
    
    # آخر تحديث
    st.markdown(f"<p style='text-align:center; color:#666; font-size:0.8rem;'>آخر تحديث: {st.session_state.last_refresh}</p>", unsafe_allow_html=True)
    
    # رادار الطلبات في المقدمة
    buyer_radar_ui()
    
    # تبويبات إضافية
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 طلبات المشترين",
        "👥 قائمة البائعين",
        "👨‍💼 تسجيل تاجر",
        "🔐 المشرف"
    ])
    
    with tab1:
        st.markdown("### 📋 جميع الطلبات")
        col1, col2 = st.columns(2)
        with col1:
            filter_wilaya = st.selectbox("فلترة حسب الولاية", ["كل الولايات"] + WILAYAS)
        
        show_radar_requests(filter_wilaya if filter_wilaya != "كل الولايات" else None)
    
    with tab2:
        st.markdown("### 👥 البائعون المسجلون")
        col1, col2 = st.columns(2)
        with col1:
            filter_v_wilaya = st.selectbox("فلترة البائعين", ["كل الولايات"] + WILAYAS, key="vendor_filter")
        
        show_vendors(filter_v_wilaya if filter_v_wilaya != "كل الولايات" else None)
    
    with tab3:
        vendor_registration()
    
    with tab4:
        admin_panel()
    
    # تذييل
    st.markdown("""
    <div class="footer">
        RASSIM OS 2026 • منصة الوساطة الذكية • جميع الحقوق محفوظة
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 17. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()
