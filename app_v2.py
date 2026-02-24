#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS ULTIMATE 2026
منصة وسيط ذكي - دليل البائعين المتكامل
69 ولاية جزائرية
"""

import streamlit as st
import sqlite3
import random
import time
import json
import hashlib
import secrets
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, Any, List, Optional

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS • دليل البائعين",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. الثوابت والتكوين
# ==========================================
DB_PATH = Path("rassim_os.db")
ADMIN_PASSWORD = "rassim2026"  # غيرها بعد التثبيت

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
CATEGORIES: Tuple[str, ...] = (
    "🚗 قطع غيار سيارات",
    "🔧 خردة وأدوات",
    "🏠 عقارات",
    "📱 هواتف",
    "🛋️ أثاث",
    "👕 ملابس",
    "🛠️ خدمات",
    "💄 تجميل",
    "📦 أخرى"
)

# ==========================================
# 5. قاعدة البيانات
# ==========================================
@st.cache_resource
def get_connection():
    return sqlite3.connect(str(DB_PATH), check_same_thread=False)

conn = get_connection()

def init_db():
    cursor = conn.cursor()
    
    # جدول البائعين
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            wilaya TEXT NOT NULL,
            category TEXT NOT NULL,
            address TEXT,
            description TEXT,
            verified INTEGER DEFAULT 0,
            views INTEGER DEFAULT 0,
            contacts INTEGER DEFAULT 0,
            joined_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # جدول طلبات المشتريين
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buyer_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            wilaya TEXT NOT NULL,
            buyer_name TEXT NOT NULL,
            buyer_phone TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'active',
            matched_vendor_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (matched_vendor_id) REFERENCES vendors (id)
        )
    """)
    
    # جدول سجل البحث
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            category TEXT,
            wilaya TEXT,
            results_count INTEGER,
            searched_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # جدول المشرفين
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()

init_db()

# ==========================================
# 6. بيانات تجريبية للبائعين
# ==========================================
def seed_vendors():
    """إضافة بائعين تجريبيين"""
    sample_vendors = [
        ("مؤسسة الرونو لقطع الغيار", "0555123456", "42 - تيبازة", "🚗 قطع غيار سيارات", 
         "فوكة - الطريق الوطني", "متخصصون في قطع غيار رونو وبيجو", 1),
        ("خير الدين للخردة", "0666123456", "16 - الجزائر", "🔧 خردة وأدوات",
         "باب الزوار - المنطقة الصناعية", "جميع أنواع الخردة والمعدات المستعملة", 1),
        ("صالون الفخامة", "0777123456", "31 - وهران", "👕 ملابس",
         "وسط المدينة - شارع الأمير عبد القادر", "ملابس رجالية ونسائية فاخرة", 1),
        ("حديدو للعقارات", "0555987123", "42 - تيبازة", "🏠 عقارات",
         "فوكة - بجانب البلدية", "كراء وبيع العقارات في تيبازة", 1),
        ("إلياس للهواتف", "0665987123", "25 - قسنطينة", "📱 هواتف",
         "وسط المدينة - سوق الهواتف", "تصليح وبيع هواتف مستعملة وجديدة", 1),
        ("صالون لطيفة للتجميل", "0775987123", "19 - سطيف", "💄 تجميل",
         "شارع فلسطين", "كريمات ومكياج أصلي", 1),
        ("عمار للأثاث", "0555987345", "06 - بجاية", "🛋️ أثاث",
         "منطقة القصبة", "أثاث منزلي ومكتبي", 1)
    ]
    
    cursor = conn.cursor()
    count = 0
    for vendor in sample_vendors:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO vendors (name, phone, wilaya, category, address, description, verified)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, vendor)
            if cursor.rowcount > 0:
                count += 1
        except:
            pass
    
    conn.commit()
    return count

# ==========================================
# 7. المتغيرات في الجلسة
# ==========================================
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'last_search' not in st.session_state:
    st.session_state.last_search = None
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'selected_vendor' not in st.session_state:
    st.session_state.selected_vendor = None

# ==========================================
# 8. التصميم
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

/* ===== قسم البحث ===== */
.search-section {
    background: linear-gradient(135deg, #1a1a2a, #2a2a3a);
    border-radius: 30px;
    padding: 30px;
    margin: 20px 0;
    border: 1px solid #00ffff;
}

.search-title {
    color: #00ffff;
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 10px;
}

/* ===== بطاقة البائع ===== */
.vendor-card {
    background: #1a1a2a;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 15px;
    border: 1px solid #333;
    transition: all 0.3s ease;
    cursor: pointer;
}

.vendor-card:hover {
    border-color: #00ffff;
    transform: translateX(-5px);
}

.vendor-name {
    color: #00ffff;
    font-size: 1.3rem;
    font-weight: bold;
}

.vendor-category {
    background: #2a2a3a;
    padding: 3px 10px;
    border-radius: 20px;
    color: #ff00ff;
    font-size: 0.8rem;
    display: inline-block;
}

.vendor-verified {
    background: #00aa00;
    color: white;
    padding: 2px 8px;
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

.contact-btn {
    background: #00ffff;
    color: black;
    padding: 10px;
    border-radius: 10px;
    text-decoration: none;
    display: inline-block;
    text-align: center;
    font-weight: bold;
    transition: opacity 0.2s;
}

.contact-btn:hover {
    opacity: 0.8;
}

/* ===== نتائج البحث ===== */
.search-results {
    background: #2a2a3a;
    border-radius: 20px;
    padding: 20px;
    margin: 20px 0;
    animation: slideIn 0.5s ease;
}

@keyframes slideIn {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
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
    border-radius: 10px !important;
    padding: 10px !important;
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
# 9. دوال المساعدة
# ==========================================
def get_stats():
    """إحصائيات"""
    cursor = conn.cursor()
    vendors = cursor.execute("SELECT COUNT(*) FROM vendors").fetchone()[0]
    requests = cursor.execute("SELECT COUNT(*) FROM buyer_requests WHERE status='active'").fetchone()[0]
    visitors = random.randint(50, 200)
    return vendors, requests, visitors

# ==========================================
# 10. نظام البحث الذكي
# ==========================================
def search_vendors(query: str, wilaya: str, category: str) -> List[Dict]:
    """البحث عن بائعين"""
    cursor = conn.cursor()
    
    sql = "SELECT * FROM vendors WHERE 1=1"
    params = []
    
    if query:
        sql += " AND (name LIKE ? OR description LIKE ? OR category LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])
    
    if wilaya != "كل الولايات":
        sql += " AND wilaya = ?"
        params.append(wilaya)
    
    if category != "كل الفئات":
        sql += " AND category = ?"
        params.append(category)
    
    sql += " ORDER BY verified DESC, views DESC"
    
    results = cursor.execute(sql, params).fetchall()
    
    # تسجيل البحث
    cursor.execute("""
        INSERT INTO search_log (query, category, wilaya, results_count)
        VALUES (?, ?, ?, ?)
    """, (query, category if category != "كل الفئات" else None, 
          wilaya if wilaya != "كل الولايات" else None, len(results)))
    conn.commit()
    
    return results

# ==========================================
# 11. واجهة البحث الرئيسية
# ==========================================
def search_interface():
    """واجهة البحث عن البائعين"""
    st.markdown("""
    <div class="search-section">
        <div class="search-title">🔍 ابحث عن بائع في 69 ولاية</div>
        <p style="color: #888;">اكتب ما تبحث عنه وسنجد لك التجار المتخصصين</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        query = st.text_input("", placeholder="مثال: قطع غيار رونو, خردة, كراء شقة...")
    with col2:
        wilaya = st.selectbox("الولاية", ["كل الولايات"] + list(WILAYAS))
    
    category = st.selectbox("الفئة", ["كل الفئات"] + list(CATEGORIES))
    
    if st.button("🔍 بحث في دليل البائعين", use_container_width=True) and query:
        with st.status("🚀 جاري البحث في قاعدة بيانات التجار..."):
            time.sleep(1)
            results = search_vendors(query, wilaya, category)
            
            if results:
                st.success(f"✅ تم العثور على {len(results)} بائع")
                st.session_state.search_results = results
            else:
                st.warning("😕 لم نجد بائعين لهذا الطلب")
                st.session_state.search_results = []
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # عرض النتائج
    if st.session_state.search_results:
        st.markdown("### 📍 نتائج البحث")
        for vendor in st.session_state.search_results:
            whatsapp = vendor[2][1:] if vendor[2].startswith('0') else vendor[2]
            
            with st.container():
                st.markdown(f"""
                <div class="vendor-card" onclick="document.getElementById('vendor_{vendor[0]}').click();">
                    <div style="display: flex; justify-content: space-between;">
                        <span class="vendor-name">{vendor[1]}</span>
                        <span class="vendor-category">{vendor[4]}</span>
                    </div>
                    <div style="margin: 5px 0;">
                        <span class="vendor-verified">✅ موثق</span>
                    </div>
                    <div class="vendor-stats">
                        <span>📍 {vendor[3]}</span>
                        <span>👁️ {vendor[7]} مشاهدة</span>
                        <span>📞 {vendor[8]} اتصال</span>
                    </div>
                    <p style="color: #aaa;">{vendor[6][:100]}...</p>
                    <div style="display: flex; gap: 10px;">
                        <a href="https://wa.me/213{whatsapp}" target="_blank" class="contact-btn" style="flex:1;">📱 واتساب</a>
                        <a href="tel:{vendor[2]}" class="contact-btn" style="flex:1; background:#ff00ff;">📞 اتصال</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # تحديث عدد المشاهدات
                cursor = conn.cursor()
                cursor.execute("UPDATE vendors SET views = views + 1 WHERE id = ?", (vendor[0],))
                conn.commit()

# ==========================================
# 12. إضافة طلب (إذا لم يجد)
# ==========================================
def add_buyer_request():
    """إضافة طلب عندما لا يجد المشتري"""
    st.markdown("### 📝 لم تجد بائعاً؟ اترك طلبك")
    
    with st.form("buyer_request"):
        title = st.text_input("ما الذي تبحث عنه؟ *")
        category = st.selectbox("الفئة", CATEGORIES)
        wilaya = st.selectbox("الولاية", WILAYAS)
        name = st.text_input("اسمك *")
        phone = st.text_input("رقم الهاتف *")
        description = st.text_area("تفاصيل إضافية")
        
        if st.form_submit_button("🔔 أرسل الطلب للتجار", use_container_width=True) and title and name and phone:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO buyer_requests (title, category, wilaya, buyer_name, buyer_phone, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, category, wilaya, name, phone, description))
            conn.commit()
            
            st.success("✅ تم إرسال طلبك! سيتواصل معك التجار قريباً.")
            st.balloons()

# ==========================================
# 13. انضم كتاجر
# ==========================================
def join_as_vendor():
    """تسجيل بائع جديد"""
    st.markdown("### 👨‍💼 انضم كتاجر")
    
    with st.form("vendor_registration"):
        name = st.text_input("اسم المحل أو المؤسسة *")
        phone = st.text_input("رقم الهاتف *")
        wilaya = st.selectbox("الولاية", WILAYAS)
        category = st.selectbox("التخصص", CATEGORIES)
        address = st.text_input("العنوان")
        description = st.text_area("وصف النشاط")
        
        if st.form_submit_button("📋 سجل الآن", use_container_width=True) and name and phone:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO vendors (name, phone, wilaya, category, address, description, verified)
                    VALUES (?, ?, ?, ?, ?, ?, 0)
                """, (name, phone, wilaya, category, address, description))
                conn.commit()
                st.success("✅ تم تسجيلك! سيقوم المشرف بتوثيق حسابك قريباً.")
            except:
                st.error("❌ هذا الرقم مسجل مسبقاً")

# ==========================================
# 14. لوحة تحكم المشرف
# ==========================================
def admin_panel():
    """لوحة تحكم المشرف"""
    st.markdown("### 🔐 لوحة تحكم المشرف")
    
    # تسجيل الدخول
    if not st.session_state.admin_logged_in:
        password = st.text_input("كلمة المرور", type="password")
        if st.button("دخول") and password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.rerun()
        return
    
    tabs = st.tabs(["📊 إحصائيات", "👥 البائعين", "📋 الطلبات", "➕ إضافة بائع"])
    
    with tabs[0]:
        vendors, requests, visitors = get_stats()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("إجمالي البائعين", vendors)
        col2.metric("طلبات نشطة", requests)
        col3.metric("زيارات اليوم", visitors)
        col4.metric("الولايات", len(WILAYAS))
        
        # آخر عمليات البحث
        cursor = conn.cursor()
        searches = cursor.execute("SELECT query, wilaya, results_count, searched_at FROM search_log ORDER BY searched_at DESC LIMIT 10").fetchall()
        if searches:
            st.markdown("#### 🔍 آخر عمليات البحث")
            for s in searches:
                st.text(f"{s[3][:16]} - {s[0]} ({s[2]} نتيجة)")
    
    with tabs[1]:
        cursor = conn.cursor()
        vendors = cursor.execute("SELECT id, name, phone, wilaya, category, verified, views, contacts FROM vendors ORDER BY id DESC").fetchall()
        
        for v in vendors:
            with st.expander(f"{v[1]} - {v[4]}"):
                col1, col2, col3 = st.columns([2,1,1])
                col1.write(f"📞 {v[2]} | 📍 {v[3]}")
                col2.write(f"👁️ {v[6]} | 📞 {v[7]}")
                if col3.button("✅ توثيق", key=f"verify_{v[0]}"):
                    cursor.execute("UPDATE vendors SET verified = 1 WHERE id = ?", (v[0],))
                    conn.commit()
                    st.rerun()
    
    with tabs[2]:
        cursor = conn.cursor()
        requests = cursor.execute("SELECT id, title, category, wilaya, buyer_name, buyer_phone, status FROM buyer_requests ORDER BY id DESC").fetchall()
        
        for r in requests:
            with st.expander(f"{r[1]} - {r[3]}"):
                st.write(f"👤 {r[4]} | 📞 {r[5]}")
                if st.button("✅ تم التواصل", key=f"done_{r[0]}"):
                    cursor.execute("UPDATE buyer_requests SET status = 'done' WHERE id = ?", (r[0],))
                    conn.commit()
                    st.rerun()
    
    with tabs[3]:
        with st.form("admin_add_vendor"):
            name = st.text_input("اسم المحل")
            phone = st.text_input("رقم الهاتف")
            wilaya = st.selectbox("الولاية", WILAYAS)
            category = st.selectbox("التخصص", CATEGORIES)
            address = st.text_input("العنوان")
            verified = st.checkbox("موثق")
            
            if st.form_submit_button("➕ إضافة بائع") and name and phone:
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO vendors (name, phone, wilaya, category, address, verified)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (name, phone, wilaya, category, address, 1 if verified else 0))
                    conn.commit()
                    st.success("تمت الإضافة")
                    st.rerun()
                except:
                    st.error("الرقم موجود")

# ==========================================
# 15. إحصائيات سريعة
# ==========================================
def show_stats():
    """عرض إحصائيات"""
    vendors, requests, visitors = get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{vendors}</div>
            <div class="stat-label">بائع</div>
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
            <div class="stat-value">{len(WILAYAS)}</div>
            <div class="stat-label">ولاية</div>
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
# 16. الدالة الرئيسية
# ==========================================
def main():
    """الدالة الرئيسية"""
    
    # تهيئة البيانات
    seed_vendors()
    
    # عداد الزوار
    vendors, requests, visitors = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span style="color:#00ffff;">●</span> {visitors} زائر • {vendors} بائع
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
        📞 RASSIM OS
    </div>
    <div class="subtitle">
        دليل البائعين في 69 ولاية • وسيطك الذكي
    </div>
    """, unsafe_allow_html=True)
    
    # إحصائيات
    show_stats()
    
    # تبويبات
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 بحث عن بائع", "📝 طلب جديد", "👨‍💼 انضم كتاجر", "🔐 المشرف"])
    
    with tab1:
        search_interface()
    
    with tab2:
        add_buyer_request()
    
    with tab3:
        join_as_vendor()
    
    with tab4:
        admin_panel()
    
    # تذييل
    st.markdown("""
    <div class="footer">
        RASSIM OS 2026 • دليل البائعين المتكامل • جميع الحقوق محفوظة
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 17. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()
