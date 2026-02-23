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
# 1. إعدادات الصفحة المتقدمة
# ==========================================
st.set_page_config(
    page_title="راسم تيتانيوم - سوق الهواتف الجزائري",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. تحسين محركات البحث (SEO)
# ==========================================
st.markdown("""
<meta name="description" content="راسم تيتانيوم - أفضل سوق للهواتف في الجزائر. بيع وشراء الهواتف المستعملة والجديدة في 58 ولاية.">
<meta name="keywords" content="واد كنيس, Ouedkniss, هواتف, الجزائر, بيع وشراء, راسم فون, تيتانيوم">
<meta name="author" content="RASSIM DZ">
""", unsafe_allow_html=True)

# ==========================================
# 3. التصميم المتكامل - ألوان واضحة وجميلة
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');

* {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    box-sizing: border-box;
}

/* ===== خلفية الصفحة ===== */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #e9ecf5 100%);
    color: #2c3e50;
}

/* ===== الهيدر الرئيسي ===== */
.main-header {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    padding: 30px;
    border-radius: 30px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.main-title {
    font-size: 3.5rem;
    font-weight: 900;
    color: white;
    text-align: center;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 10px rgba(255,255,255,0.5); }
    to { text-shadow: 0 0 20px rgba(255,255,255,0.8); }
}

.main-subtitle {
    color: rgba(255,255,255,0.9);
    text-align: center;
    font-size: 1.2rem;
    margin-top: 10px;
}

/* ===== الكروت الإحصائية ===== */
.stMetric {
    background: white !important;
    border-radius: 20px !important;
    padding: 20px !important;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05) !important;
    border: 1px solid rgba(0,0,0,0.05) !important;
    transition: all 0.3s ease;
}

.stMetric:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(46, 91, 255, 0.1) !important;
    border-color: #2e5bff !important;
}

.stMetric label {
    color: #6c757d !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}

.stMetric [data-testid="stMetricValue"] {
    color: #1e3c72 !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
}

/* ===== الأزرار ===== */
.stButton > button {
    width: 100%;
    border-radius: 50px !important;
    background: linear-gradient(135deg, #2e5bff, #00c3ff) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    border: none !important;
    padding: 15px 30px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 5px 15px rgba(46, 91, 255, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 25px rgba(46, 91, 255, 0.5) !important;
}

/* ===== صناديق الإدخال ===== */
.stTextInput input, 
.stTextArea textarea,
.stSelectbox select {
    background: white !important;
    border: 2px solid #e0e0e0 !important;
    border-radius: 15px !important;
    color: #2c3e50 !important;
    padding: 12px 20px !important;
    font-size: 1rem !important;
    transition: all 0.3s ease;
}

.stTextInput input:focus, 
.stTextArea textarea:focus,
.stSelectbox select:focus {
    border-color: #2e5bff !important;
    box-shadow: 0 0 0 3px rgba(46, 91, 255, 0.1) !important;
    outline: none;
}

.stTextInput label, 
.stTextArea label,
.stSelectbox label {
    color: #1e3c72 !important;
    font-weight: 600 !important;
    margin-bottom: 5px !important;
}

/* ===== التبويبات ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: white;
    padding: 10px;
    border-radius: 50px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    margin-bottom: 30px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 40px !important;
    padding: 10px 30px !important;
    color: #6c757d !important;
    font-weight: 600 !important;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2e5bff, #00c3ff) !important;
    color: white !important;
    box-shadow: 0 5px 15px rgba(46, 91, 255, 0.3) !important;
}

/* ===== الشريط الجانبي ===== */
section[data-testid="stSidebar"] {
    background: white !important;
    border-left: 1px solid rgba(0,0,0,0.05);
    padding: 20px;
}

section[data-testid="stSidebar"] .stMarkdown {
    color: #2c3e50;
}

/* ===== بطاقات الإعلانات ===== */
.ad-card {
    background: white;
    border-radius: 25px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.03);
    border: 1px solid rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}

.ad-card:hover {
    transform: translateX(-5px);
    box-shadow: 0 10px 30px rgba(46, 91, 255, 0.1);
    border-color: #2e5bff;
}

.ad-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1e3c72;
    margin-bottom: 10px;
}

.ad-price {
    background: linear-gradient(135deg, #2e5bff, #00c3ff);
    color: white;
    padding: 8px 20px;
    border-radius: 50px;
    display: inline-block;
    font-weight: 700;
    font-size: 1.3rem;
}

.ad-details {
    display: flex;
    gap: 20px;
    color: #6c757d;
    margin: 15px 0;
    font-size: 0.95rem;
}

.ad-description {
    color: #4a5568;
    line-height: 1.6;
    margin: 15px 0;
}

/* ===== رسائل النجاح والخطأ ===== */
.stAlert {
    border-radius: 15px !important;
    border: none !important;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05) !important;
}

.stAlert.success {
    background: #d4edda !important;
    color: #155724 !important;
}

.stAlert.error {
    background: #f8d7da !important;
    color: #721c24 !important;
}

.stAlert.warning {
    background: #fff3cd !important;
    color: #856404 !important;
}

.stAlert.info {
    background: #d1ecf1 !important;
    color: #0c5460 !important;
}

/* ===== العناوين ===== */
h1, h2, h3 {
    color: #1e3c72 !important;
    font-weight: 700 !important;
}

h1 {
    font-size: 2.5rem !important;
    border-bottom: 3px solid #2e5bff;
    padding-bottom: 15px;
    margin-bottom: 30px !important;
}

h2 {
    font-size: 2rem !important;
    margin: 25px 0 20px !important;
}

/* ===== النصوص العامة ===== */
p, li, .stMarkdown {
    color: #4a5568 !important;
    line-height: 1.6;
}

/* ===== الروابط ===== */
a {
    color: #2e5bff !important;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
}

a:hover {
    color: #00c3ff !important;
    text-decoration: underline;
}

/* ===== الفوتر ===== */
footer {
    background: white !important;
    border-top: 1px solid rgba(0,0,0,0.05) !important;
    padding: 20px !important;
    color: #6c757d !important;
    text-align: center;
    margin-top: 50px;
}

/* ===== شريط التمرير ===== */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #2e5bff, #00c3ff);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #00c3ff, #2e5bff);
}

/* ===== تأثيرات حركية ===== */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeInUp 0.6s ease forwards;
}

/* ===== أزرار المشاركة الاجتماعية ===== */
.social-share {
    background: white;
    padding: 25px;
    border-radius: 30px;
    margin: 25px 0;
    text-align: center;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    border: 1px solid rgba(0,0,0,0.05);
}

.social-share h3 {
    color: #1e3c72 !important;
    margin-bottom: 15px;
}

.social-icons {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
    margin: 20px 0;
}

.social-icon {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: #f8f9fa;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

.social-icon:hover {
    transform: translateY(-5px) scale(1.1);
    box-shadow: 0 10px 25px rgba(46, 91, 255, 0.2);
}

.social-icon img {
    width: 30px;
    height: 30px;
}

/* ===== قسم تيك توك ===== */
.tiktok-section {
    background: linear-gradient(135deg, #25F4EE, #FE2C55);
    padding: 30px;
    border-radius: 30px;
    margin: 25px 0;
    text-align: center;
    box-shadow: 0 10px 30px rgba(254, 44, 85, 0.2);
}

.tiktok-section h2 {
    color: white !important;
    margin-bottom: 15px;
}

.tiktok-section p {
    color: white !important;
    font-size: 1.2rem;
}

.tiktok-tags {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin: 20px 0;
}

.tiktok-tag {
    background: white;
    color: #FE2C55;
    padding: 5px 15px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.9rem;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

/* ===== فقاعات الدردشة ===== */
.chat-sent {
    background: linear-gradient(135deg, #2e5bff, #00c3ff) !important;
    color: white !important;
    padding: 12px 18px;
    border-radius: 20px 20px 5px 20px;
    margin: 10px 0;
    max-width: 80%;
    margin-left: auto;
}

.chat-received {
    background: #f8f9fa !important;
    color: #2c3e50 !important;
    padding: 12px 18px;
    border-radius: 20px 20px 20px 5px;
    margin: 10px 0;
    max-width: 80%;
    margin-right: auto;
    border: 1px solid rgba(0,0,0,0.05);
}

/* ===== التجاوب مع الجوال ===== */
@media screen and (max-width: 768px) {
    .main-title {
        font-size: 2.2rem;
    }
    
    h1 {
        font-size: 2rem !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
    }
    
    .ad-title {
        font-size: 1.3rem;
    }
    
    .ad-price {
        font-size: 1.1rem;
        padding: 6px 15px;
    }
}
</style>

<!-- الهيدر -->
<div class="main-header">
    <div class="main-title">🇩🇿 راسم تيتانيوم ألترا</div>
    <div class="main-subtitle">أول سوق إلكتروني جزائري متخصص في الهواتف</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. إعدادات قاعدة البيانات
# ==========================================
DB = "rassim_titanium.db"

def init_db():
    """تهيئة قاعدة البيانات"""
    try:
        conn = sqlite3.connect(DB, check_same_thread=False)
        cursor = conn.cursor()
        
        # جدول المستخدمين
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
        
        # جدول الإعلانات
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
        
        # جدول الرسائل
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
        
        # جدول المفضلة
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
        
        # جدول الإشعارات
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
        
        # جدول البلاغات
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
        
        # جدول الزوار
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
        st.error(f"خطأ في قاعدة البيانات: {e}")
        return None

@st.cache_resource
def get_connection():
    """الحصول على اتصال قاعدة البيانات"""
    return sqlite3.connect(DB, check_same_thread=False)

# تهيئة قاعدة البيانات
init_db()

# ==========================================
# 5. دوال المساعدة الأساسية
# ==========================================
def hash_password(password, salt):
    """تشفير كلمة المرور"""
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

def create_notification(username, message, notif_type="info"):
    """إنشاء إشعار جديد"""
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
    """تسجيل زائر جديد"""
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
    """الحصول على إحصائيات الموقع"""
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
# 6. أزرار المشاركة الاجتماعية
# ==========================================
def show_social_share():
    """عرض أزرار المشاركة الاجتماعية"""
    site_url = "https://racim-phone.streamlit.app/"
    
    st.markdown(f"""
    <div class="social-share">
        <h3>📢 شارك الموقع مع أصدقائك</h3>
        <p style="color: #6c757d;">ساعد في نشر الموقع واكسب الثواب 🤲</p>
        
        <div class="social-icons">
            <a href="https://www.facebook.com/sharer/sharer.php?u={site_url}" target="_blank">
                <div class="social-icon">
                    <img src="https://img.icons8.com/color/48/facebook-new.png">
                </div>
            </a>
            <a href="https://api.whatsapp.com/send?text=شوف هاد الموقع: {site_url}" target="_blank">
                <div class="social-icon">
                    <img src="https://img.icons8.com/color/48/whatsapp--v1.png">
                </div>
            </a>
            <a href="https://t.me/share/url?url={site_url}" target="_blank">
                <div class="social-icon">
                    <img src="https://img.icons8.com/color/48/telegram-app--v1.png">
                </div>
            </a>
            <a href="#" onclick="navigator.clipboard.writeText('{site_url}'); alert('✅ تم نسخ الرابط!'); return false;">
                <div class="social-icon">
                    <img src="https://img.icons8.com/color/48/link--v1.png">
                </div>
            </a>
        </div>
        
        <div style="background: linear-gradient(135deg, #2e5bff, #00c3ff); color: white; padding: 10px 25px; border-radius: 50px; display: inline-block; font-weight: 600;">
            👥 شارك واكسب الدعاء
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 7. قسم تيك توك
# ==========================================
def show_tiktok_section():
    """عرض قسم تيك توك"""
    st.markdown("""
    <div class="tiktok-section">
        <h2>🎵 تيك توك الجزائر</h2>
        <p style="font-size: 1.3rem; font-weight: bold;">
            "تهنينا من التقرعيج، موقع راسم تيتانيوم راهو واجد! 🇩🇿"
        </p>
        <div style="margin: 15px 0;">
            <span style="background: white; color: #FE2C55; padding: 5px 20px; border-radius: 50px; font-weight: bold;">🔥 تسوق بسهولة</span>
            <span style="background: white; color: #FE2C55; padding: 5px 20px; border-radius: 50px; font-weight: bold; margin: 0 10px;">⚡ بيع بسرعة</span>
            <span style="background: white; color: #FE2C55; padding: 5px 20px; border-radius: 50px; font-weight: bold;">💬 تواصل مباشر</span>
        </div>
        <div class="tiktok-tags">
            <span class="tiktok-tag">#واد_كنيس</span>
            <span class="tiktok-tag">#الجزائر</span>
            <span class="tiktok-tag">#هواتف</span>
            <span class="tiktok-tag">#راسم_تيتانيوم</span>
        </div>
        <div style="margin-top: 20px; background: rgba(255,255,255,0.2); padding: 10px; border-radius: 50px; display: inline-block;">
            📱 58 ولاية - حمل التطبيق
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 8. بطاقات الإحصائيات
# ==========================================
def show_stats_cards():
    """عرض بطاقات الإحصائيات"""
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
    """صفحة تسجيل الدخول والتسجيل"""
    
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
                    st.error("❌ اسم المستخدم قصير جداً (3 أحرف على الأقل)")
                elif len(new_pass) < 6:
                    st.error("❌ كلمة المرور قصيرة جداً (6 أحرف على الأقل)")
                else:
                    try:
                        salt = secrets.token_hex(16)
                        hashed = hash_password(new_pass, salt)
                        
                        conn.execute("""
                            INSERT INTO users (username, password, salt, email, phone, role)
                            VALUES (?, ?, ?, ?, ?, 'user')
                        """, (new_user, hashed, salt, email, phone))
                        conn.commit()
                        
                        st.success("✅ تم التسجيل بنجاح! يمكنك الدخول الآن")
                    except sqlite3.IntegrityError:
                        st.error("❌ اسم المستخدم موجود مسبقاً")
                    except Exception as e:
                        st.error(f"❌ حدث خطأ: {e}")

# ==========================================
# 10. صفحة السوق الذكي
# ==========================================
def show_market(conn):
    """عرض السوق الذكي"""
    st.header("🛍️ السوق الذكي")
    
    show_stats_cards()
    show_social_share()
    show_tiktok_section()
    
    # فلاتر البحث
    with st.expander("🔍 فلترة البحث", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            wilaya = st.selectbox("الولاية", ["الكل"] + [f"{i:02d}" for i in range(1, 59)])
        with col2:
            category = st.selectbox("القسم", ["الكل", "سامسونج", "آيفون", "هواوي", "شاومي", "أخرى"])
        
        search = st.text_input("🔎 بحث عن هاتف", placeholder="اكتب اسم الهاتف...")
        
        if st.button("🔍 بحث", use_container_width=True):
            st.success("جاري البحث...")
    
    # عرض الإعلانات
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
                with st.container():
                    st.markdown(f"""
                    <div class="ad-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div class="ad-title">{ad[1]}</div>
                            <div class="ad-price">{ad[2]:,} دج</div>
                        </div>
                        
                        <div class="ad-details">
                            <span>📍 {ad[4]}</span>
                            <span>👁️ {ad[8]} مشاهدة</span>
                            {f'<span>📅 {ad[12][:10]}</span>' if ad[12] else ''}
                        </div>
                        
                        <div class="ad-description">
                            {ad[5][:150]}...
                        </div>
                        
                        <div style="display: flex; gap: 10px; margin-top: 20px;">
                            <button class="stButton" style="flex: 1;" onclick="window.open('https://wa.me/213{ad[3]}')">📞 واتساب</button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("📞 واتساب", key=f"wa_{ad[0]}"):
                        st.info(f"📱 رقم الهاتف: {ad[3]}")
                    
                    st.divider()
        else:
            st.info("لا توجد إعلانات حالياً")
    except Exception as e:
        st.error(f"خطأ في تحميل الإعلانات: {e}")

# ==========================================
# 11. صفحة إضافة إعلان
# ==========================================
def post_ad(conn):
    """إضافة إعلان جديد"""
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
    """عرض المحادثات"""
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
                    st.markdown(f"<div class='chat-sent'><b>أنت:</b> {msg[1]}<br><small>{msg[2][11:16] if msg[2] else ''}</small></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-received'><b>{msg[0]}:</b> {msg[1]}<br><small>{msg[2][11:16] if msg[2] else ''}</small></div>", unsafe_allow_html=True)
            
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
    """لوحة تحكم الإدارة"""
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
    """الدالة الرئيسية للتشغيل"""
    
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
            <div style="background: linear-gradient(135deg, #1e3c72, #2a5298); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 20px;">
                <h3 style="color: white;">🎖️ {st.session_state.user}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            menu = st.radio(
                "القائمة الرئيسية",
                ["🏠 السوق الذكي", "📢 إضافة إعلان", "💬 الرسائل", "🤖 المساعد الذكي"]
            )
            
            if st.session_state.role == "admin":
                if st.button("🛡️ لوحة الإدارة", use_container_width=True):
                    menu = "🛡️ الإدارة"
            
            if st.button("🚪 تسجيل الخروج", use_container_width=True):
                st.session_state.user = None
                st.rerun()
        
        if menu == "🏠 السوق الذكي":
            show_market(conn)
        elif menu == "📢 إضافة إعلان":
            post_ad(conn)
        elif menu == "💬 الرسائل":
            show_chat(conn)
        elif menu == "🤖 المساعد الذكي":
            st.info("🤖 المساعد الذكي قيد التطوير...")
        elif menu == "🛡️ الإدارة" and st.session_state.role == "admin":
            admin_dashboard(conn)

if __name__ == "__main__":
    main()
