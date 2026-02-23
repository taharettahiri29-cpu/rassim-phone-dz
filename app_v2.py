import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import re
import datetime
import secrets
import os
import time
import plotly.express as px
import plotly.graph_objects as go
import warnings
from functools import wraps

warnings.filterwarnings('ignore')

# ==========================================
# 1. إعدادات الصفحة - Sleek OS Style
# ==========================================
st.set_page_config(
    page_title="RASSIM OS • الجزائر",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. SEO Meta Tags
# ==========================================
st.markdown("""
<meta name="description" content="RASSIM OS - أول سوق إلكتروني جزائري بتقنية OS Style">
<meta name="keywords" content="واد كنيس, هواتف الجزائر, OS, sleek design">
<meta name="author" content="RASSIM DZ">
""", unsafe_allow_html=True)

# ==========================================
# 3. Sleek OS Style - تصميم عصري متطور
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    direction: rtl;
    box-sizing: border-box;
}

/* ===== خلفية OS Style ===== */
.stApp {
    background: #0a0a0f;
    background-image: 
        radial-gradient(circle at 20% 20%, rgba(0, 255, 255, 0.03) 0%, transparent 30%),
        radial-gradient(circle at 80% 70%, rgba(255, 0, 255, 0.03) 0%, transparent 30%);
    color: #ffffff;
}

/* ===== Glass Morphism Effects ===== */
.glass-panel {
    background: rgba(20, 20, 30, 0.6);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

/* ===== الهيدر ===== */
.os-header {
    background: rgba(10, 10, 20, 0.8);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding: 20px 30px;
    margin-bottom: 30px;
    position: sticky;
    top: 0;
    z-index: 100;
}

.os-title {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #00ffff, #ff00ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
}

.os-version {
    background: rgba(255, 255, 255, 0.1);
    padding: 4px 12px;
    border-radius: 30px;
    font-size: 0.8rem;
    color: #888;
    margin-right: 10px;
}

/* ===== كروت إحصائية OS Style ===== */
.stMetric {
    background: rgba(20, 20, 30, 0.6) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 20px !important;
    padding: 25px 20px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stMetric:hover {
    transform: translateY(-4px);
    border-color: rgba(0, 255, 255, 0.3) !important;
    box-shadow: 0 12px 48px rgba(0, 255, 255, 0.15) !important;
}

.stMetric label {
    color: rgba(255, 255, 255, 0.5) !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px;
}

.stMetric [data-testid="stMetricValue"] {
    color: white !important;
    font-size: 2.4rem !important;
    font-weight: 600 !important;
    text-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

/* ===== أزرار OS Style ===== */
.stButton > button {
    background: rgba(30, 30, 40, 0.8) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 50px !important;
    color: white !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    padding: 12px 24px !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
}

.stButton > button:hover {
    background: rgba(50, 50, 60, 0.9) !important;
    border-color: rgba(0, 255, 255, 0.3) !important;
    transform: scale(0.98);
}

/* ===== صناديق الإدخال ===== */
.stTextInput input, 
.stTextArea textarea,
.stSelectbox select {
    background: rgba(20, 20, 30, 0.6) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 50px !important;
    color: white !important;
    padding: 12px 20px !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease;
}

.stTextInput input:focus, 
.stTextArea textarea:focus,
.stSelectbox select:focus {
    border-color: rgba(0, 255, 255, 0.3) !important;
    box-shadow: 0 0 0 2px rgba(0, 255, 255, 0.1) !important;
}

.stTextInput label, 
.stTextArea label,
.stSelectbox label {
    color: rgba(255, 255, 255, 0.7) !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
}

/* ===== التبويبات OS Style ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(20, 20, 30, 0.6);
    backdrop-filter: blur(10px);
    padding: 8px;
    border-radius: 60px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 50px !important;
    padding: 10px 24px !important;
    color: rgba(255, 255, 255, 0.6) !important;
    font-weight: 500 !important;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    background: rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border-color: rgba(0, 255, 255, 0.3) !important;
}

/* ===== الشريط الجانبي ===== */
section[data-testid="stSidebar"] {
    background: rgba(10, 10, 15, 0.8) !important;
    backdrop-filter: blur(20px);
    border-left: 1px solid rgba(255, 255, 255, 0.05);
}

/* ===== بطاقات الإعلانات OS Style ===== */
.os-card {
    background: rgba(20, 20, 30, 0.6);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 24px;
    padding: 24px;
    margin-bottom: 16px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.os-card:hover {
    border-color: rgba(0, 255, 255, 0.2);
    transform: translateX(-4px);
    box-shadow: 0 12px 48px rgba(0, 255, 255, 0.1);
}

.os-card-title {
    font-size: 1.4rem;
    font-weight: 600;
    color: white;
    margin-bottom: 12px;
}

.os-card-price {
    background: rgba(0, 255, 255, 0.1);
    border: 1px solid rgba(0, 255, 255, 0.2);
    color: #00ffff;
    padding: 8px 20px;
    border-radius: 50px;
    display: inline-block;
    font-weight: 600;
    font-size: 1.2rem;
}

.os-card-details {
    display: flex;
    gap: 24px;
    color: rgba(255, 255, 255, 0.5);
    font-size: 0.9rem;
    margin: 16px 0;
}

.os-card-details span {
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ===== أزرار المشاركة OS Style ===== */
.os-share {
    background: rgba(20, 20, 30, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 60px;
    padding: 12px 20px;
    margin: 20px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}

.os-share-icons {
    display: flex;
    gap: 8px;
}

.os-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.os-icon:hover {
    background: rgba(0, 255, 255, 0.1);
    border-color: rgba(0, 255, 255, 0.3);
    transform: scale(1.1);
}

.os-icon img {
    width: 20px;
    height: 20px;
    opacity: 0.7;
    transition: all 0.2s ease;
}

.os-icon:hover img {
    opacity: 1;
    filter: brightness(0) invert(1);
}

.os-badge {
    background: rgba(0, 255, 255, 0.1);
    border: 1px solid rgba(0, 255, 255, 0.2);
    color: #00ffff;
    padding: 6px 16px;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 500;
}

/* ===== قسم تيك توك OS Style ===== */
.os-tiktok {
    background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 60px;
    padding: 12px 24px;
    margin: 20px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}

.os-tiktok-text {
    color: white;
    font-size: 0.95rem;
    font-weight: 500;
}

.os-tags {
    display: flex;
    gap: 8px;
}

.os-tag {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.8);
    padding: 4px 12px;
    border-radius: 50px;
    font-size: 0.8rem;
}

/* ===== فقاعات الدردشة OS Style ===== */
.os-chat-sent {
    background: rgba(0, 255, 255, 0.1);
    border: 1px solid rgba(0, 255, 255, 0.2);
    color: white;
    padding: 12px 18px;
    border-radius: 20px 20px 5px 20px;
    margin: 10px 0;
    max-width: 80%;
    margin-left: auto;
}

.os-chat-received {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    padding: 12px 18px;
    border-radius: 20px 20px 20px 5px;
    margin: 10px 0;
    max-width: 80%;
    margin-right: auto;
}

/* ===== العناوين ===== */
h1, h2, h3 {
    color: white !important;
    font-weight: 600 !important;
}

h1 {
    font-size: 2.2rem !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 16px;
    margin-bottom: 24px !important;
}

/* ===== شريط التمرير ===== */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.02);
}

::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 255, 255, 0.3);
}

/* ===== التجاوب مع الجوال ===== */
@media screen and (max-width: 768px) {
    .os-header {
        padding: 15px 20px;
    }
    
    .os-title {
        font-size: 1.6rem;
    }
    
    .os-share {
        flex-direction: column;
        align-items: stretch;
    }
    
    .os-tiktok {
        flex-direction: column;
        text-align: center;
    }
}
</style>

<!-- OS Header -->
<div class="os-header">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
            <span class="os-title">RASSIM OS</span>
            <span class="os-version">v2.0.4 • الجزائر</span>
        </div>
        <div style="display: flex; gap: 12px;">
            <span style="color: rgba(255,255,255,0.3);">⚡</span>
            <span style="color: rgba(255,255,255,0.3);">🔋 100%</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. إعدادات قاعدة البيانات
# ==========================================
DB = "rassim_os.db"

def init_db():
    """تهيئة قاعدة البيانات"""
    try:
        conn = sqlite3.connect(DB, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                salt TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                role TEXT DEFAULT 'user',
                verified INTEGER DEFAULT 0,
                banned INTEGER DEFAULT 0,
                ad_count INTEGER DEFAULT 0,
                last_login TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price INTEGER NOT NULL,
                phone TEXT NOT NULL,
                wilaya TEXT NOT NULL,
                description TEXT,
                category TEXT DEFAULT 'أخرى',
                images TEXT,
                views INTEGER DEFAULT 0,
                featured INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                owner TEXT NOT NULL,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner) REFERENCES users(username)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                message TEXT NOT NULL,
                read INTEGER DEFAULT 0,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender) REFERENCES users(username),
                FOREIGN KEY (receiver) REFERENCES users(username)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                ad_id INTEGER NOT NULL,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username),
                FOREIGN KEY (ad_id) REFERENCES ads(id),
                UNIQUE(username, ad_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT DEFAULT 'info',
                read INTEGER DEFAULT 0,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad_id INTEGER NOT NULL,
                reporter TEXT NOT NULL,
                reason TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ad_id) REFERENCES ads(id),
                FOREIGN KEY (reporter) REFERENCES users(username)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                page TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        return conn
    except Exception as e:
        st.error(f"OS Error: {e}")
        return None

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)

init_db()

# ==========================================
# 5. دوال المساعدة
# ==========================================
def hash_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

def create_notification(username, message, notif_type="info"):
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO notifications (username, message, type) VALUES (?, ?, ?)",
            (username, message, notif_type)
        )
        conn.commit()
    except:
        pass

def log_visitor():
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO visitors (ip, page) VALUES (?, ?)",
            (st.session_state.get('ip', 'unknown'), st.session_state.get('page', 'main'))
        )
        conn.commit()
    except:
        pass

def get_stats():
    try:
        conn = get_connection()
        users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        ads = conn.execute("SELECT COUNT(*) FROM ads WHERE status='active'").fetchone()[0]
        visitors = conn.execute("SELECT COUNT(*) FROM visitors").fetchone()[0]
        views = conn.execute("SELECT SUM(views) FROM ads").fetchone()[0] or 0
        return users, ads, visitors, views
    except:
        return 0, 0, 0, 0

# ==========================================
# 6. أزرار المشاركة OS Style
# ==========================================
def show_social_share():
    site_url = "https://racim-phone.streamlit.app/"
    
    st.markdown(f"""
    <div class="os-share">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="color: rgba(255,255,255,0.5);">📱 شارك</span>
            <div class="os-share-icons">
                <a href="https://www.facebook.com/sharer/sharer.php?u={site_url}" target="_blank">
                    <div class="os-icon"><img src="https://img.icons8.com/color/48/facebook-new.png"></div>
                </a>
                <a href="https://api.whatsapp.com/send?text=شوف هاد الموقع: {site_url}" target="_blank">
                    <div class="os-icon"><img src="https://img.icons8.com/color/48/whatsapp--v1.png"></div>
                </a>
                <a href="https://t.me/share/url?url={site_url}" target="_blank">
                    <div class="os-icon"><img src="https://img.icons8.com/color/48/telegram-app--v1.png"></div>
                </a>
                <a href="#" onclick="navigator.clipboard.writeText('{site_url}'); alert('✅ تم النسخ'); return false;">
                    <div class="os-icon"><img src="https://img.icons8.com/color/48/link--v1.png"></div>
                </a>
            </div>
        </div>
        <div class="os-badge">👥 +10</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 7. قسم تيك توك OS Style
# ==========================================
def show_tiktok_section():
    st.markdown("""
    <div class="os-tiktok">
        <div class="os-tiktok-text">🎵 "تهنينا من التقرعيج، الدزة راهو واجد!"</div>
        <div class="os-tags">
            <span class="os-tag">#واد_كنيس</span>
            <span class="os-tag">#الجزائر</span>
            <span class="os-tag">#هواتف</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 8. بطاقات الإحصائيات
# ==========================================
def show_stats_cards():
    users, ads, visitors, views = get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("المستخدمين", f"{users:,}")
    with col2:
        st.metric("الإعلانات", f"{ads:,}")
    with col3:
        st.metric("الزيارات", f"{visitors:,}")
    with col4:
        st.metric("المشاهدات", f"{views:,}")

# ==========================================
# 9. صفحة تسجيل الدخول
# ==========================================
def login_page():
    show_stats_cards()
    show_social_share()
    show_tiktok_section()
    
    tab1, tab2 = st.tabs(["🔑 تسجيل الدخول", "📝 حساب جديد"])
    conn = get_connection()
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")
            submitted = st.form_submit_button("دخول", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.error("❌ يرجى ملء جميع الحقول")
                else:
                    try:
                        user = conn.execute(
                            "SELECT password, salt, role FROM users WHERE username=?",
                            (username,)
                        ).fetchone()
                        
                        if user and user[0] == hash_password(password, user[1]):
                            st.session_state.user = username
                            st.session_state.role = user[2]
                            st.rerun()
                        else:
                            st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
                    except Exception as e:
                        st.error(f"❌ خطأ في تسجيل الدخول: {e}")
    
    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("اسم المستخدم الجديد")
            new_pass = st.text_input("كلمة المرور الجديدة", type="password")
            email = st.text_input("البريد الإلكتروني (اختياري)")
            phone = st.text_input("رقم الهاتف (اختياري)")
            submitted = st.form_submit_button("تسجيل", use_container_width=True)
            
            if submitted:
                if not new_user or not new_pass:
                    st.error("❌ اسم المستخدم وكلمة المرور مطلوبان")
                elif len(new_user) < 3:
                    st.error("❌ اسم المستخدم قصير جداً")
                elif len(new_pass) < 6:
                    st.error("❌ كلمة المرور قصيرة جداً")
                else:
                    try:
                        salt = secrets.token_hex(16)
                        hashed = hash_password(new_pass, salt)
                        
                        conn.execute("""
                            INSERT INTO users (username, password, salt, email, phone, role)
                            VALUES (?, ?, ?, ?, ?, 'user')
                        """, (new_user, hashed, salt, email, phone))
                        conn.commit()
                        
                        st.success("✅ تم التسجيل بنجاح!")
                    except sqlite3.IntegrityError:
                        st.error("❌ اسم المستخدم موجود مسبقاً")
                    except Exception as e:
                        st.error(f"❌ حدث خطأ: {e}")

# ==========================================
# 10. صفحة السوق الذكي
# ==========================================
def show_market(conn):
    st.header("🛍️ السوق الذكي")
    
    show_stats_cards()
    show_social_share()
    show_tiktok_section()
    
    with st.expander("🔍 فلترة البحث", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            wilaya = st.selectbox("الولاية", ["الكل"] + [f"{i:02d}" for i in range(1, 59)])
        with col2:
            category = st.selectbox("القسم", ["الكل", "سامسونج", "آيفون", "هواوي", "شاومي", "أخرى"])
        
        search = st.text_input("🔎 بحث عن هاتف", placeholder="اكتب اسم الهاتف...")
        
        if st.button("🔍 بحث", use_container_width=True):
            st.success("جاري البحث...")
    
    try:
        query = "SELECT * FROM ads WHERE status='active'"
        params = []
        
        if wilaya != "الكل":
            query += " AND wilaya=?"
            params.append(wilaya)
        if category != "الكل":
            query += " AND category=?"
            params.append(category)
        if search:
            query += " AND (title LIKE ? OR description LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])
        
        query += " ORDER BY featured DESC, date DESC LIMIT 10"
        
        ads = conn.execute(query, params).fetchall()
        
        if ads:
            for ad in ads:
                st.markdown(f"""
                <div class="os-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div class="os-card-title">{ad[1]}</div>
                        <div class="os-card-price">{ad[2]:,} دج</div>
                    </div>
                    
                    <div class="os-card-details">
                        <span>📍 {ad[4]}</span>
                        <span>👁️ {ad[8]}</span>
                        {f'<span>📅 {ad[12][:10]}</span>' if ad[12] else ''}
                    </div>
                    
                    <div style="color: rgba(255,255,255,0.6); margin: 16px 0;">
                        {ad[5][:150]}...
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📞 واتساب", key=f"wa_{ad[0]}", use_container_width=True):
                        st.info(f"📱 {ad[3]}")
                with col2:
                    if st.button("💬 مراسلة", key=f"msg_{ad[0]}", use_container_width=True):
                        st.session_state[f"chat_{ad[7]}"] = True
                
                st.divider()
        else:
            st.info("لا توجد إعلانات حالياً")
    except Exception as e:
        st.error(f"خطأ في تحميل الإعلانات: {e}")

# ==========================================
# 11. صفحة إضافة إعلان
# ==========================================
def post_ad(conn):
    st.header("📢 إضافة إعلان جديد")
    
    with st.form("new_ad_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("اسم الهاتف *")
            category = st.selectbox("الفئة", ["سامسونج", "آيفون", "هواوي", "شاومي", "أخرى"])
        with col2:
            price = st.number_input("السعر (دج) *", min_value=0, step=1000)
            wilaya = st.selectbox("الولاية *", [f"{i:02d}" for i in range(1, 59)])
        
        phone = st.text_input("رقم الهاتف *")
        description = st.text_area("وصف الهاتف")
        
        if st.form_submit_button("🚀 نشر الإعلان", use_container_width=True):
            if not title or price <= 0 or not phone:
                st.error("❌ يرجى ملء جميع الحقول المطلوبة (*)")
            else:
                try:
                    conn.execute("""
                        INSERT INTO ads (title, price, phone, wilaya, description, category, owner)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (title, price, phone, wilaya, description, category, st.session_state.user))
                    conn.commit()
                    
                    conn.execute("UPDATE users SET ad_count = ad_count + 1 WHERE username=?", 
                               (st.session_state.user,))
                    conn.commit()
                    
                    st.success("✅ تم نشر الإعلان بنجاح!")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {e}")

# ==========================================
# 12. صفحة الدردشة
# ==========================================
def show_chat(conn):
    st.header("💬 المحادثات")
    
    user = st.session_state.user
    
    try:
        conversations = conn.execute("""
            SELECT DISTINCT 
                CASE WHEN sender = ? THEN receiver ELSE sender END as contact,
                MAX(date) as last_msg,
                (SELECT COUNT(*) FROM messages WHERE receiver=? AND sender=contact AND read=0) as unread
            FROM messages 
            WHERE sender = ? OR receiver = ?
            GROUP BY contact
            ORDER BY last_msg DESC
        """, (user, user, user, user)).fetchall()
        
        if not conversations:
            st.info("لا توجد محادثات حالياً")
            return
        
        contacts = [f"{c[0]} 🔴" if c[2] > 0 else c[0] for c in conversations]
        selected = st.selectbox("اختر محادثة", contacts)
        selected = selected.replace(" 🔴", "")
        
        if selected:
            st.subheader(f"الدردشة مع {selected}")
            
            conn.execute("UPDATE messages SET read=1 WHERE sender=? AND receiver=?", 
                        (selected, user))
            conn.commit()
            
            messages = conn.execute("""
                SELECT sender, message, date FROM messages
                WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)
                ORDER BY date ASC
            """, (user, selected, selected, user)).fetchall()
            
            for msg in messages:
                if msg[0] == user:
                    st.markdown(f"<div class='os-chat-sent'><b>أنت:</b> {msg[1]}<br><small>{msg[2][11:16] if msg[2] else ''}</small></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='os-chat-received'><b>{msg[0]}:</b> {msg[1]}<br><small>{msg[2][11:16] if msg[2] else ''}</small></div>", unsafe_allow_html=True)
            
            with st.form("send_message", clear_on_submit=True):
                msg = st.text_input("اكتب رسالتك...")
                if st.form_submit_button("إرسال", use_container_width=True) and msg:
                    conn.execute("""
                        INSERT INTO messages (sender, receiver, message)
                        VALUES (?, ?, ?)
                    """, (user, selected, msg))
                    conn.commit()
                    st.rerun()
    except Exception as e:
        st.error(f"خطأ في تحميل المحادثات: {e}")

# ==========================================
# 13. لوحة الإدارة
# ==========================================
def admin_dashboard(conn):
    st.header("🔐 لوحة الإدارة")
    
    users, ads, visitors, views = get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("المستخدمين", f"{users:,}")
    with col2:
        st.metric("الإعلانات", f"{ads:,}")
    with col3:
        st.metric("الزيارات", f"{visitors:,}")
    with col4:
        st.metric("المشاهدات", f"{views:,}")
    
    tab1, tab2, tab3 = st.tabs(["👥 المستخدمين", "📊 الإحصائيات", "🚨 البلاغات"])
    
    with tab1:
        st.subheader("👥 قائمة المستخدمين")
        try:
            users_df = pd.read_sql_query("""
                SELECT username, role, verified, banned, ad_count, 
                       substr(last_login, 1, 10) as last_login
                FROM users ORDER BY last_login DESC
            """, conn)
            st.dataframe(users_df, use_container_width=True)
        except Exception as e:
            st.error(f"خطأ في تحميل البيانات: {e}")
    
    with tab2:
        st.subheader("📊 إحصائيات متقدمة")
        try:
            category_stats = conn.execute("""
                SELECT category, COUNT(*) as count 
                FROM ads 
                WHERE status='active' 
                GROUP BY category
            """).fetchall()
            
            if category_stats:
                df_cats = pd.DataFrame(category_stats, columns=["الفئة", "العدد"])
                fig = px.pie(df_cats, values='العدد', names='الفئة', 
                            title="توزيع الإعلانات حسب الفئة",
                            color_discrete_sequence=px.colors.sequential.Blues_r)
                st.plotly_chart(fig, use_container_width=True)
        except:
            pass
    
    with tab3:
        st.subheader("🚨 البلاغات المعلقة")
        try:
            reports = conn.execute("""
                SELECT r.id, a.title, r.reporter, r.reason, r.date
                FROM reports r JOIN ads a ON r.ad_id = a.id
                WHERE r.status='pending'
                ORDER BY r.date DESC
            """).fetchall()
            
            if reports:
                for report in reports:
                    with st.container():
                        st.warning(f"📌 إعلان: {report[1]}")
                        st.write(f"المبلغ: {report[2]} | السبب: {report[3]} | التاريخ: {report[4][:10]}")
                        if st.button("✅ معالجة", key=f"resolve_{report[0]}"):
                            conn.execute("UPDATE reports SET status='resolved' WHERE id=?", (report[0],))
                            conn.commit()
                            st.rerun()
                        st.divider()
            else:
                st.info("لا توجد بلاغات معلقة")
        except Exception as e:
            st.error(f"خطأ في تحميل البلاغات: {e}")

# ==========================================
# 14. التشغيل الرئيسي
# ==========================================
def main():
    if "user" not in st.session_state:
        st.session_state.user = None
    if "role" not in st.session_state:
        st.session_state.role = "user"
    if "ip" not in st.session_state:
        st.session_state.ip = secrets.token_hex(8)
    if "page" not in st.session_state:
        st.session_state.page = "main"
    
    log_visitor()
    
    if not st.session_state.user:
        login_page()
    else:
        conn = get_connection()
        
        with st.sidebar:
            st.markdown(f"""
            <div style="background: rgba(20,20,30,0.8); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05); padding: 20px; border-radius: 16px; text-align: center; margin-bottom: 20px;">
                <div style="color: white; font-size: 1.2rem; font-weight: 500;">🎖️ {st.session_state.user}</div>
            </div>
            """, unsafe_allow_html=True)
            
            menu = st.radio(
                "القائمة",
                ["🏠 السوق", "📢 إعلان", "💬 الرسائل", "🤖 المساعد"]
            )
            
            if st.session_state.role == "admin":
                if st.button("🛡️ الإدارة", use_container_width=True):
                    menu = "🛡️ الإدارة"
            
            if st.button("🚪 خروج", use_container_width=True):
                st.session_state.user = None
                st.rerun()
        
        if menu == "🏠 السوق":
            show_market(conn)
        elif menu == "📢 إعلان":
            post_ad(conn)
        elif menu == "💬 الرسائل":
            show_chat(conn)
        elif menu == "🤖 المساعد":
            st.info("🤖 المساعد الذكي قيد التطوير...")
        elif menu == "🛡️ الإدارة" and st.session_state.role == "admin":
            admin_dashboard(conn)

if __name__ == "__main__":
    main()
