#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS ULTIMATE 2026
منصة التجار الذكية - التسجيل التلقائي للبائعين
69 ولاية جزائرية
"""

import streamlit as st
import sqlite3
import random
import time
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, Any, List, Optional

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS • منصة التجار",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. الثوابت والتكوين
# ==========================================
DB_PATH = Path("rassim_os.db")
ADMIN_PASSWORD = "rassim2026"

# ==========================================
# 3. قائمة الولايات
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
    "46 - عين تموشنت", "48 - غليزان", "49 - تيميمون", "50 - برج باجي مختار"
)

# ==========================================
# 4. قائمة الفئات
# ==========================================
CATEGORIES: List[str] = [
    "🚗 قطع غيار سيارات",
    "🔧 خردة وأدوات",
    "🏠 عقارات",
    "📱 هواتف",
    "🛋️ أثاث",
    "👕 ملابس",
    "🛠️ خدمات",
    "💄 تجميل",
    "📦 أخرى"
]

# ==========================================
# 5. قاعدة البيانات
# ==========================================
@st.cache_resource
def get_connection():
    return sqlite3.connect(str(DB_PATH), check_same_thread=False)

conn = get_connection()

def init_db():
    cursor = conn.cursor()
    
    # جدول التجار
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            wilaya TEXT NOT NULL,
            categories TEXT NOT NULL,  -- JSON array
            address TEXT,
            description TEXT,
            verified INTEGER DEFAULT 0,
            views INTEGER DEFAULT 0,
            leads INTEGER DEFAULT 0,    -- عدد الزبائن المحولين
            joined_date TEXT DEFAULT CURRENT_TIMESTAMP,
            last_active TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # جدول طلبات الزبائن
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            wilaya TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',  -- pending, matched, done
            matched_vendor_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (matched_vendor_id) REFERENCES vendors (id)
        )
    """)
    
    # جدول إحصائيات البحث
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            category TEXT,
            wilaya TEXT,
            count INTEGER DEFAULT 1,
            last_searched TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()

init_db()

# ==========================================
# 6. بيانات تجريبية
# ==========================================
def seed_data():
    cursor = conn.cursor()
    
    # تجار تجريبيين
    sample_vendors = [
        ("مؤسسة الرونو لقطع الغيار", "0555123456", "42 - تيبازة", 
         json.dumps(["🚗 قطع غيار سيارات", "🔧 خردة وأدوات"]),
         "فوكة - الطريق الوطني", "متخصصون في جميع قطع غيار رونو وبيجو", 1),
        ("خير الدين للخردة", "0666123456", "16 - الجزائر",
         json.dumps(["🔧 خردة وأدوات", "🛠️ خدمات"]),
         "باب الزوار - المنطقة الصناعية", "نشتري ونبيع جميع أنواع الخردة", 1),
        ("صالون الفخامة", "0777123456", "31 - وهران",
         json.dumps(["👕 ملابس", "💄 تجميل"]),
         "وسط المدينة", "أحدث صيحات الموضة والتجميل", 1),
    ]
    
    for vendor in sample_vendors:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO vendors 
                (name, phone, wilaya, categories, address, description, verified)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, vendor)
        except:
            pass
    
    # طلبات تجريبية
    sample_requests = [
        ("محرك رونو كليو 2 ديزل", "🚗 قطع غيار سيارات", "42 - تيبازة",
         "ناصر", "0555123456", "محرك بحالة جيدة"),
        ("شقة كراء غرفتين + صالون", "🏠 عقارات", "16 - الجزائر",
         "فاطمة", "0666123456", "في وسط المدينة"),
        ("بطارية iPhone 13 Pro Max", "📱 هواتف", "31 - وهران",
         "كريم", "0777123456", "أصلية فقط"),
    ]
    
    for req in sample_requests:
        cursor.execute("""
            INSERT OR IGNORE INTO customer_requests 
            (title, category, wilaya, customer_name, customer_phone, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, req)
    
    conn.commit()

seed_data()

# ==========================================
# 7. المتغيرات في الجلسة
# ==========================================
if 'vendor_logged_in' not in st.session_state:
    st.session_state.vendor_logged_in = False
if 'current_vendor' not in st.session_state:
    st.session_state.current_vendor = None
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'last_search' not in st.session_state:
    st.session_state.last_search = None

# ==========================================
# 8. التصميم
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
    font-size: 3.5rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #00ffff, #ff00ff, #ffff00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 20px;
    animation: glow 3s ease-in-out infinite;
}

@keyframes glow {
    0%, 100% { filter: drop-shadow(0 0 10px #00ffff); }
    50% { filter: drop-shadow(0 0 20px #ff00ff); }
}

.subtitle {
    text-align: center;
    color: #888;
    font-size: 1.1rem;
    margin-top: -10px;
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
    font-size: 1.4rem;
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

/* ===== إعلانات التجار ===== */
.landing-page {
    background: linear-gradient(135deg, #2a2a3a, #1a1a2a);
    border-radius: 30px;
    padding: 40px;
    margin: 20px 0;
    text-align: center;
    border: 1px solid #00ffff;
}

.landing-title {
    font-size: 2.5rem;
    font-weight: bold;
    color: #00ffff;
    margin-bottom: 20px;
}

.landing-stats {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin: 30px 0;
}

.stat-circle {
    background: #2a2a3a;
    border: 2px solid #ff00ff;
    border-radius: 50%;
    width: 120px;
    height: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.stat-number {
    font-size: 2rem;
    color: #00ffff;
    font-weight: bold;
}

.stat-text {
    font-size: 0.9rem;
    color: white;
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
def get_stats():
    cursor = conn.cursor()
    vendors = cursor.execute("SELECT COUNT(*) FROM vendors").fetchone()[0]
    requests = cursor.execute("SELECT COUNT(*) FROM customer_requests WHERE status='pending'").fetchone()[0]
    searches = cursor.execute("SELECT SUM(count) FROM search_stats").fetchone()[0] or 0
    visitors = random.randint(100, 300)
    return vendors, requests, searches, visitors

# ==========================================
# 10. صفحة هبوط التجار
# ==========================================
def vendor_landing_page():
    """صفحة مخصصة لجذب التجار"""
    vendors, requests, searches, _ = get_stats()
    
    st.markdown("""
    <div class="landing-page">
        <div class="landing-title">🏪 انضم لشبكة تجار RASSIM OS</div>
        <p style="font-size: 1.2rem; color: #888;">
            أكثر من <span style="color: #00ffff; font-weight: bold;">69 ولاية</span> جزائرية تبحث عن خدماتك
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-circle">
            <div class="stat-number">{vendors}+</div>
            <div class="stat-text">تاجر</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-circle">
            <div class="stat-number">{requests}</div>
            <div class="stat-text">طلب</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-circle">
            <div class="stat-number">{searches}+</div>
            <div class="stat-text">بحث</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # فوائد التسجيل
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📱 **زبائن مباشرون**\n\nيأتيك الزبائن دون جهد")
    with col2:
        st.info("📊 **إحصائيات دقيقة**\n\nتعرف كم شخص يبحث عن منتجك")
    with col3:
        st.info("🚀 **ظهور فوري**\n\nتسجيلك ينشط خلال دقائق")

# ==========================================
# 11. تسجيل تاجر جديد
# ==========================================
def vendor_auto_registration():
    """تسجيل سريع للتجار"""
    st.markdown("### 📝 سجل محلك الآن")
    
    with st.form("vendor_registration"):
        name = st.text_input("اسم المحل *")
        phone = st.text_input("رقم الهاتف *")
        wilaya = st.selectbox("الولاية *", WILAYAS)
        categories = st.multiselect("ماذا تبيع؟ *", CATEGORIES)
        address = st.text_input("العنوان")
        description = st.text_area("وصف النشاط")
        
        if st.form_submit_button("🚀 انضم لشبكة راسم مجاناً", use_container_width=True):
            if name and phone and categories:
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO vendors (name, phone, wilaya, categories, address, description, verified)
                        VALUES (?, ?, ?, ?, ?, ?, 0)
                    """, (name, phone, wilaya, json.dumps(categories), address, description))
                    conn.commit()
                    
                    st.success("✅ تم تسجيلك بنجاح! ستظهر للزبائن بعد التوثيق")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("❌ هذا الرقم مسجل مسبقاً")
            else:
                st.error("❌ املأ الحقول المطلوبة")

# ==========================================
# 12. لوحة تحكم التاجر
# ==========================================
def vendor_dashboard(vendor_id):
    """لوحة تحكم التاجر"""
    cursor = conn.cursor()
    vendor = cursor.execute("SELECT * FROM vendors WHERE id = ?", (vendor_id,)).fetchone()
    
    if not vendor:
        st.error("تاجر غير موجود")
        return
    
    st.markdown(f"### مرحباً {vendor[1]} 👋")
    
    # إحصائيات التاجر
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("مشاهدات ملفك", vendor[7])
    with col2:
        st.metric("زبائن تواصلوا", vendor[8])
    with col3:
        st.metric("آخر ظهور", vendor[10][:10])
    
    # طلبات في ولايته
    st.markdown("### 🔍 طلبات في منطقتك")
    requests = cursor.execute("""
        SELECT * FROM customer_requests 
        WHERE wilaya = ? AND status = 'pending'
        ORDER BY created_at DESC
    """, (vendor[3],)).fetchall()
    
    if requests:
        for req in requests:
            with st.container():
                st.markdown(f"""
                <div class="vendor-card">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #00ffff;">{req[1]}</span>
                        <span style="color: #ff00ff;">{req[2]}</span>
                    </div>
                    <p>{req[5]}</p>
                    <div style="display: flex; gap: 10px;">
                        <a href="https://wa.me/213{req[4][1:]}" target="_blank" class="contact-btn" style="background:#25D366; color:white; padding:8px; border-radius:10px; text-decoration:none;">تواصل مع الزبون</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("✅ لدي هذا المنتج", key=f"have_{req[0]}"):
                    cursor.execute("UPDATE customer_requests SET status='matched', matched_vendor_id=? WHERE id=?", 
                                 (vendor_id, req[0]))
                    cursor.execute("UPDATE vendors SET leads = leads + 1 WHERE id=?", (vendor_id,))
                    conn.commit()
                    st.success("تم إبلاغ الزبون!")
                    st.rerun()
    else:
        st.info("لا توجد طلبات في منطقتك حالياً")

# ==========================================
# 13. البحث عن تاجر
# ==========================================
def search_vendors(query: str, wilaya: str, category: str):
    """البحث عن تجار"""
    cursor = conn.cursor()
    
    sql = "SELECT * FROM vendors WHERE verified = 1"
    params = []
    
    if query:
        sql += " AND (name LIKE ? OR description LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%"])
    
    if wilaya != "كل الولايات":
        sql += " AND wilaya = ?"
        params.append(wilaya)
    
    if category != "كل الفئات":
        sql += " AND categories LIKE ?"
        params.append(f"%{category}%")
    
    sql += " ORDER BY views DESC"
    
    results = cursor.execute(sql, params).fetchall()
    
    # تسجيل البحث للإحصائيات
    cursor.execute("""
        INSERT INTO search_stats (keyword, category, wilaya)
        VALUES (?, ?, ?)
    """, (query, category if category != "كل الفئات" else None, 
          wilaya if wilaya != "كل الولايات" else None))
    conn.commit()
    
    return results

# ==========================================
# 14. البحث عن تاجر (واجهة)
# ==========================================
def search_interface():
    st.markdown("### 🔍 ابحث عن تاجر")
    
    col1, col2 = st.columns(2)
    with col1:
        query = st.text_input("", placeholder="مثال: قطع غيار رونو")
    with col2:
        wilaya = st.selectbox("الولاية", ["كل الولايات"] + list(WILAYAS))
    
    category = st.selectbox("الفئة", ["كل الفئات"] + CATEGORIES)
    
    if st.button("🔍 بحث", use_container_width=True) and query:
        with st.spinner("جاري البحث..."):
            results = search_vendors(query, wilaya, category)
            
            if results:
                st.success(f"✅ تم العثور على {len(results)} تاجر")
                for vendor in results:
                    categories = json.loads(vendor[4])
                    cats = " • ".join(categories)
                    whatsapp = vendor[2][1:] if vendor[2].startswith('0') else vendor[2]
                    
                    st.markdown(f"""
                    <div class="vendor-card">
                        <div style="display: flex; justify-content: space-between;">
                            <span class="vendor-name">{vendor[1]}</span>
                            <span class="vendor-badge">✅ موثق</span>
                        </div>
                        <div class="vendor-stats">
                            <span>📍 {vendor[3]}</span>
                            <span>👁️ {vendor[7]}</span>
                            <span>📞 {vendor[8]} زبون</span>
                        </div>
                        <p style="color: #aaa;">{cats}</p>
                        <p>{vendor[6]}</p>
                        <div style="display: flex; gap: 10px;">
                            <a href="https://wa.me/213{whatsapp}" target="_blank" class="contact-btn" style="background:#25D366; color:white; padding:10px; border-radius:10px; text-decoration:none; flex:1; text-align:center;">📱 واتساب</a>
                            <a href="tel:{vendor[2]}" class="contact-btn" style="background:#ff00ff; color:white; padding:10px; border-radius:10px; text-decoration:none; flex:1; text-align:center;">📞 اتصال</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # تحديث المشاهدات
                    cursor = conn.cursor()
                    cursor.execute("UPDATE vendors SET views = views + 1 WHERE id = ?", (vendor[0],))
                    conn.commit()
            else:
                st.warning("😕 لم نجد تجار متخصصين")
                
                # عرض خيار إضافة طلب
                st.markdown("### 📝 لم تجد؟ اترك طلبك")
                with st.form("quick_request"):
                    req_title = st.text_input("ما الذي تبحث عنه؟")
                    req_name = st.text_input("اسمك")
                    req_phone = st.text_input("رقم هاتفك")
                    
                    if st.form_submit_button("🔔 أبلغ التجار") and req_title and req_name and req_phone:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO customer_requests (title, category, wilaya, customer_name, customer_phone)
                            VALUES (?, ?, ?, ?, ?)
                        """, (req_title, category, wilaya, req_name, req_phone))
                        conn.commit()
                        st.success("تم إرسال طلبك! سيتواصل معك التجار قريباً")

# ==========================================
# 15. لوحة المشرف
# ==========================================
def admin_panel():
    st.markdown("### 🔐 لوحة المشرف")
    
    if not st.session_state.admin_logged_in:
        password = st.text_input("كلمة المرور", type="password")
        if st.button("دخول") and password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.rerun()
        return
    
    tabs = st.tabs(["📊 إحصائيات", "👥 التجار", "📋 الطلبات", "✅ توثيق"])
    
    with tabs[0]:
        vendors, requests, searches, visitors = get_stats()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("إجمالي التجار", vendors)
        col2.metric("طلبات معلقة", requests)
        col3.metric("عمليات بحث", searches)
        col4.metric("زوار اليوم", visitors)
        
        # إحصائيات حسب الولاية
        st.markdown("#### 📊 إحصائيات الولايات")
        cursor = conn.cursor()
        wilaya_stats = cursor.execute("""
            SELECT wilaya, COUNT(*) FROM vendors GROUP BY wilaya ORDER BY COUNT(*) DESC
        """).fetchall()
        
        for w in wilaya_stats[:5]:
            st.text(f"{w[0]}: {w[1]} تاجر")
    
    with tabs[1]:
        cursor = conn.cursor()
        vendors = cursor.execute("SELECT id, name, phone, wilaya, verified, views, leads FROM vendors ORDER BY id DESC").fetchall()
        
        for v in vendors:
            with st.expander(f"{v[1]} - {v[3]}"):
                st.write(f"📞 {v[2]}")
                st.write(f"👁️ {v[5]} مشاهدة | 📞 {v[6]} زبون")
                if not v[4] and st.button("✅ توثيق", key=f"verify_{v[0]}"):
                    cursor.execute("UPDATE vendors SET verified = 1 WHERE id = ?", (v[0],))
                    conn.commit()
                    st.rerun()
    
    with tabs[2]:
        cursor = conn.cursor()
        requests = cursor.execute("SELECT id, title, category, wilaya, customer_name, status FROM customer_requests ORDER BY id DESC").fetchall()
        
        for r in requests:
            st.text(f"{r[1]} - {r[3]} - {r[4]} - {r[5]}")
    
    with tabs[3]:
        st.markdown("بائعون ينتظرون التوثيق")
        cursor = conn.cursor()
        unverified = cursor.execute("SELECT id, name, phone, wilaya FROM vendors WHERE verified = 0").fetchall()
        
        for v in unverified:
            col1, col2, col3 = st.columns([2,1,1])
            col1.write(f"{v[1]} - {v[3]}")
            col2.write(v[2])
            if col3.button("✅ وثق", key=f"unv_{v[0]}"):
                cursor.execute("UPDATE vendors SET verified = 1 WHERE id = ?", (v[0],))
                conn.commit()
                st.rerun()

# ==========================================
# 16. إحصائيات
# ==========================================
def show_stats():
    vendors, requests, searches, visitors = get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
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
            <div class="stat-value">{searches}</div>
            <div class="stat-label">بحث</div>
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
# 17. الدالة الرئيسية
# ==========================================
def main():
    """الدالة الرئيسية"""
    
    # عداد الزوار
    vendors, requests, searches, visitors = get_stats()
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
        🏪 RASSIM OS
    </div>
    <div class="subtitle">
        منصة التجار الذكية • 69 ولاية
    </div>
    """, unsafe_allow_html=True)
    
    # إحصائيات
    show_stats()
    
    # تسجيل تاجر في الشريط الجانبي
    with st.sidebar:
        st.markdown("## 🏪 هل أنت تاجر؟")
        with st.expander("سجل محلك الآن مجاناً", expanded=False):
            vendor_auto_registration()
        
        if st.session_state.vendor_logged_in:
            st.markdown("---")
            if st.button("🚪 تسجيل خروج التاجر"):
                st.session_state.vendor_logged_in = False
                st.session_state.current_vendor = None
                st.rerun()
    
    # تبويبات رئيسية
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 الصفحة الرئيسية", "🔍 بحث عن تاجر", "👤 دخول التاجر", "🔐 المشرف"])
    
    with tab1:
        vendor_landing_page()
    
    with tab2:
        search_interface()
    
    with tab3:
        st.markdown("### 👤 دخول التاجر")
        phone = st.text_input("رقم الهاتف")
        if st.button("دخول", use_container_width=True) and phone:
            cursor = conn.cursor()
            vendor = cursor.execute("SELECT * FROM vendors WHERE phone = ?", (phone,)).fetchone()
            if vendor:
                st.session_state.vendor_logged_in = True
                st.session_state.current_vendor = vendor[0]
                st.rerun()
            else:
                st.error("رقم غير مسجل")
        
        if st.session_state.vendor_logged_in:
            vendor_dashboard(st.session_state.current_vendor)
    
    with tab4:
        admin_panel()
    
    # تذييل
    st.markdown("""
    <div class="footer">
        RASSIM OS 2026 • منصة التجار الذكية • جميع الحقوق محفوظة
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 18. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()

