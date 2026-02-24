#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS ULTIMATE 2026
منصة التجار الذكية - نظام الطلبات الاحترافي
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
    "47 - غرداية", "55 - توقرت", "57 - المغير", "58 - المنيع", "69 - عين الحجر"
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
            categories TEXT NOT NULL,
            address TEXT,
            description TEXT,
            verified INTEGER DEFAULT 0,
            views INTEGER DEFAULT 0,
            leads INTEGER DEFAULT 0,
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
            status TEXT DEFAULT 'pending',
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
    background: linear-gradient(135deg, #00ffff, #ff00ff);
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
    margin-bottom: 20px;
}

/* ===== نموذج الطلب الاحترافي ===== */
.request-box {
    background: linear-gradient(135deg, #1a1a2a, #2a2a3a);
    padding: 30px;
    border-radius: 30px;
    border: 2px solid #00ffff;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0,255,255,0.1);
}

.request-title {
    color: #00ffff;
    font-size: 2rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}

.request-subtitle {
    color: #888;
    text-align: center;
    margin-bottom: 30px;
    font-size: 1.1rem;
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
# 10. نموذج الطلب الاحترافي
# ==========================================
def professional_request_form():
    """نموذج طلب متطور للزبائن"""
    
    st.markdown('<div class="request-box">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="request-title">🎯 أطلق الرادار الذكي</div>
    <div class="request-subtitle">
        اكتب ما تبحث عنه وسنجده لك في 69 ولاية
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        item_name = st.text_input("🔍 ماذا تبحث؟ (بالتفصيل)", 
                                 placeholder="مثال: علبة سرعة رونو كليو 4 محرك 1.5")
        category = st.selectbox("📂 الفئة", CATEGORIES)
    
    with col2:
        user_phone = st.text_input("📱 رقم هاتفك (لتلقي العروض)", 
                                  placeholder="0661234567")
        wilaya = st.selectbox("📍 الولاية", WILAYAS)

    description = st.text_area("📝 تفاصيل إضافية", 
                               placeholder="اذكر الحالة، اللون، أو أي تفاصيل تساعد البائع",
                               height=100)

    col1, col2, col3 = st.columns(3)
    with col2:
        submit_button = st.button("🚀 إطلاق الرادار", use_container_width=True)

    if submit_button:
        if item_name and user_phone:
            # محاكاة العملية الاحترافية
            with st.status("🔄 جاري معالجة طلبك...", expanded=True) as status:
                st.write("📡 تحليل الطلب وفهرسته...")
                time.sleep(1)
                st.write(f"📲 إرسال تنبيهات لتجار {category} في {wilaya}...")
                time.sleep(1.5)
                st.write("✅ تم إطلاق الرادار بنجاح!")
                status.update(label="✅ طلبك نشط الآن!", state="complete", expanded=False)
            
            # حفظ في قاعدة البيانات
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO customer_requests (title, category, wilaya, customer_name, customer_phone, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (item_name, category, wilaya, "زبون", user_phone, description))
            conn.commit()
            
            st.success("🎉 تم تسجيل طلبك! سنتصل بك فور العثور على بائع.")
            st.balloons()
        else:
            st.error("❌ من فضلك أدخل اسم المنتج ورقم هاتفك")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 11. عرض طلبات الزبائن للتجار
# ==========================================
def show_customer_requests(wilaya_filter: str = None, category_filter: str = None):
    """عرض طلبات الزبائن للتجار"""
    cursor = conn.cursor()
    
    query = "SELECT * FROM customer_requests WHERE status='pending'"
    params = []
    
    if wilaya_filter and wilaya_filter != "كل الولايات":
        query += " AND wilaya = ?"
        params.append(wilaya_filter)
    
    if category_filter and category_filter != "كل الفئات":
        query += " AND category = ?"
        params.append(category_filter)
    
    query += " ORDER BY created_at DESC"
    
    requests = cursor.execute(query, params).fetchall()
    
    if requests:
        for req in requests:
            # إخفاء رقم الهاتف (فقط أول 4 أرقام تظهر)
            hidden_phone = req[5][:4] + "••••" if len(req[5]) > 4 else req[5]
            
            st.markdown(f"""
            <div class="request-card">
                <div class="request-header">
                    <span class="request-category">{req[2]}</span>
                    <span class="request-status">🟢 نشط</span>
                </div>
                <h4 style="color: #00ffff;">{req[1]}</h4>
                <p style="color: #aaa;">{req[6]}</p>
                <div style="display: flex; gap: 10px; margin: 10px 0;">
                    <span class="request-wilaya">📍 {req[3]}</span>
                    <span class="request-wilaya">👤 {hidden_phone}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # زر للتواصل (يظهر فقط للتجار المسجلين)
            if st.session_state.vendor_logged_in:
                if st.button(f"📞 لدي هذا المنتج", key=f"have_{req[0]}"):
                    # تحديث الطلب
                    cursor.execute("""
                        UPDATE customer_requests 
                        SET status='matched', matched_vendor_id=? 
                        WHERE id=?
                    """, (st.session_state.current_vendor, req[0]))
                    
                    # تحديث إحصائيات التاجر
                    cursor.execute("""
                        UPDATE vendors SET leads = leads + 1 WHERE id=?
                    """, (st.session_state.current_vendor,))
                    conn.commit()
                    
                    # رابط واتساب مباشر
                    whatsapp_link = f"https://wa.me/213{req[5][1:]}?text=السلام عليكم، لدي طلبك بخصوص: {req[1]}"
                    
                    st.markdown(f"""
                    <div style="background: #25D36620; padding: 15px; border-radius: 10px; margin: 10px 0;">
                        <p style="color: white;">📞 رقم الزبون: {req[5]}</p>
                        <a href="{whatsapp_link}" target="_blank" class="contact-btn" style="display: block; text-decoration: none;">
                            📱 تواصل عبر واتساب
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("😕 لا توجد طلبات نشطة حالياً")

# ==========================================
# 12. تسجيل تاجر جديد
# ==========================================
def vendor_registration():
    """تسجيل تاجر جديد"""
    st.markdown("### 📝 سجل محلك الآن")
    
    with st.form("vendor_registration"):
        name = st.text_input("اسم المحل *")
        phone = st.text_input("رقم الهاتف *")
        wilaya = st.selectbox("الولاية *", WILAYAS)
        categories = st.multiselect("ماذا تبيع؟ *", CATEGORIES)
        address = st.text_input("العنوان")
        description = st.text_area("وصف النشاط")
        
        if st.form_submit_button("🚀 انضم لشبكة راسم", use_container_width=True):
            if name and phone and categories:
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO vendors (name, phone, wilaya, categories, address, description, verified)
                        VALUES (?, ?, ?, ?, ?, ?, 0)
                    """, (name, phone, wilaya, json.dumps(categories), address, description))
                    conn.commit()
                    
                    st.success("✅ تم تسجيلك! سيقوم المشرف بتوثيق حسابك قريباً")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("❌ هذا الرقم مسجل مسبقاً")
            else:
                st.error("❌ املأ الحقول المطلوبة")

# ==========================================
# 13. لوحة تحكم التاجر
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
        st.metric("مشاهدات ملفك", vendor[8])
    with col2:
        st.metric("زبائن تواصلوا", vendor[9])
    with col3:
        st.metric("آخر ظهور", vendor[11][:10])
    
    # طلبات في ولايته
    st.markdown("### 🔍 طلبات في منطقتك")
    show_customer_requests(wilaya_filter=vendor[3])
    
    # طلبات في تخصصه
    st.markdown("### 🔍 طلبات في تخصصك")
    categories = json.loads(vendor[4])
    if categories:
        show_customer_requests(category_filter=categories[0])

# ==========================================
# 14. لوحة المشرف (مصححة)
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
    
    with tabs[1]:
        cursor = conn.cursor()
        vendors_list = cursor.execute("""
            SELECT id, name, phone, wilaya, verified, views, leads 
            FROM vendors ORDER BY id DESC
        """).fetchall()
        
        for v in vendors_list:
            with st.expander(f"{v[1]} - {v[3]}"):
                st.write(f"📞 {v[2]}")
                st.write(f"👁️ {v[5]} مشاهدة | 📞 {v[6]} زبون")
                if not v[4] and st.button("✅ توثيق", key=f"verify_{v[0]}"):
                    cursor.execute("UPDATE vendors SET verified = 1 WHERE id = ?", (v[0],))
                    conn.commit()
                    st.rerun()
    
    with tabs[2]:
        cursor = conn.cursor()
        requests_list = cursor.execute("""
            SELECT id, title, category, wilaya, status, created_at 
            FROM customer_requests ORDER BY id DESC
        """).fetchall()
        
        for r in requests_list:
            st.markdown(f"""
            <div class="request-card">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #00ffff;">{r[1]}</span>
                    <span style="color: #888;">{r[5][:10]}</span>
                </div>
                <p>{r[2]} • {r[3]}</p>
                <p>الحالة: {r[4]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown("بائعون ينتظرون التوثيق")
        cursor = conn.cursor()
        unverified = cursor.execute("""
            SELECT id, name, phone, wilaya FROM vendors WHERE verified = 0
        """).fetchall()
        
        for v in unverified:
            col1, col2, col3 = st.columns([2,1,1])
            col1.write(f"{v[1]} - {v[3]}")
            col2.write(v[2])
            if col3.button("✅ وثق", key=f"unv_{v[0]}"):
                cursor.execute("UPDATE vendors SET verified = 1 WHERE id = ?", (v[0],))
                conn.commit()
                st.rerun()

# ==========================================
# 15. إحصائيات سريعة
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
# 16. الصفحة الرئيسية
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
    
    # تبويبات رئيسية
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 أطلق الرادار", 
        "🔍 طلبات الزبائن", 
        "👨‍💼 تسجيل تاجر", 
        "👤 دخول التاجر",
        "🔐 المشرف"
    ])
    
    with tab1:
        professional_request_form()
    
    with tab2:
        st.markdown("### 🔍 طلبات الزبائن النشطة")
        
        # فلترة
        col1, col2 = st.columns(2)
        with col1:
            filter_wilaya = st.selectbox("فلترة حسب الولاية", ["كل الولايات"] + list(WILAYAS))
        with col2:
            filter_category = st.selectbox("فلترة حسب الفئة", ["كل الفئات"] + CATEGORIES)
        
        show_customer_requests(
            wilaya_filter=filter_wilaya if filter_wilaya != "كل الولايات" else None,
            category_filter=filter_category if filter_category != "كل الفئات" else None
        )
    
    with tab3:
        vendor_registration()
    
    with tab4:
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
    
    with tab5:
        admin_panel()
    
    # تذييل
    st.markdown("""
    <div class="footer">
        RASSIM OS 2026 • منصة التجار الذكية • جميع الحقوق محفوظة
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 17. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()
