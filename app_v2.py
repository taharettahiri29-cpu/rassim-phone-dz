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
# 3. التصميم المتكامل (CSS)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');

* {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    box-sizing: border-box;
}

/* ===== التصميم العام ===== */
.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(0, 255, 136, 0.05) 0%, rgba(0, 189, 255, 0.05) 90%),
                linear-gradient(135deg, #0a0a1a 0%, #1a1a2f 50%, #0d0d1a 100%);
    color: #ffffff;
    min-height: 100vh;
}

/* تأثير النجوم */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(1px 1px at 10px 10px, rgba(255,255,255,0.3), transparent),
        radial-gradient(1px 1px at 50px 100px, rgba(255,255,255,0.3), transparent);
    background-repeat: repeat;
    background-size: 400px 400px;
    opacity: 0.15;
    animation: starsMove 200s linear infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes starsMove {
    from { transform: translateY(0); }
    to { transform: translateY(-400px); }
}

/* ===== الهيدر الرئيسي ===== */
.main-title {
    font-size: 4rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00ff88, #00bdff, #0066ff, #00ff88);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin: 30px 0 20px;
    animation: gradientFlow 8s ease infinite, float 6s ease-in-out infinite;
}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

/* ===== الكروت الإحصائية ===== */
.stMetric {
    background: rgba(255, 255, 255, 0.03) !important;
    backdrop-filter: blur(12px);
    border-radius: 25px !important;
    padding: 25px 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5) !important;
    transition: all 0.4s ease;
}

.stMetric:hover {
    transform: translateY(-8px) scale(1.02) !important;
    border: 1px solid rgba(0, 255, 136, 0.3) !important;
    box-shadow: 0 30px 60px -15px rgba(0, 255, 136, 0.3) !important;
}

.stMetric [data-testid="stMetricValue"] {
    color: #fff !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
}

/* ===== الأزرار ===== */
.stButton > button {
    width: 100%;
    border-radius: 60px !important;
    background: linear-gradient(135deg, #00ff88, #00bdff, #0066ff) !important;
    background-size: 200% 200% !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    border: none !important;
    height: 3.2em;
    transition: 0.4s ease !important;
    box-shadow: 0 10px 20px -5px rgba(0, 255, 136, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 20px 30px -5px rgba(0, 255, 136, 0.6) !important;
    animation: gradientShift 3s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ===== صناديق الإدخال ===== */
.stTextInput input, 
.stTextArea textarea,
.stSelectbox select {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 50px !important;
    color: white !important;
    padding: 15px 20px !important;
    font-size: 1rem !important;
    transition: all 0.3s ease;
}

.stTextInput input:focus, 
.stTextArea textarea:focus,
.stSelectbox select:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.2) !important;
    outline: none;
}

/* ===== التبويبات ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-radius: 60px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 30px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 50px !important;
    padding: 10px 30px !important;
    color: rgba(255, 255, 255, 0.7) !important;
    font-weight: 600 !important;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #00ff88, #00bdff) !important;
    color: black !important;
    font-weight: 700 !important;
    box-shadow: 0 10px 20px -5px rgba(0, 255, 136, 0.4);
}

/* ===== الشريط الجانبي ===== */
section[data-testid="stSidebar"] {
    background: rgba(10, 10, 26, 0.8) !important;
    backdrop-filter: blur(20px);
    border-left: 1px solid rgba(255, 255, 255, 0.05);
}

/* ===== التجاوب مع الجوال ===== */
@media screen and (max-width: 768px) {
    .main-title { font-size: 2.5rem; }
    .stMetric [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
    .stButton > button { height: 2.8em; font-size: 1rem !important; }
}
</style>

<div class="main-title">🇩🇿 راسم تيتانيوم ألترا</div>
<div style="text-align: center; margin-bottom: 40px;">
    <p style="color: rgba(255,255,255,0.8); font-size: 1.3rem;">✨ أول سوق إلكتروني جزائري للهواتف</p>
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
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
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
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
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
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
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
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
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
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
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
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
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
                visit_date TEXT DEFAULT CURRENT_TIMESTAMP
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
    <div style="background: white; padding: 25px; border-radius: 30px; margin: 25px 0; text-align: center; border: 2px solid #006633;">
        <h3 style="color: #006633;">📢 شارك الموقع مع أصدقائك</h3>
        <p style="color: #666;">ساعد في نشر الموقع واكسب الثواب 🤲</p>
        <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin: 20px 0;">
            <a href="https://www.facebook.com/sharer/sharer.php?u={site_url}" target="_blank">
                <img src="https://img.icons8.com/color/48/facebook-new.png" width="45">
            </a>
            <a href="https://api.whatsapp.com/send?text=شوف هاد الموقع: {site_url}" target="_blank">
                <img src="https://img.icons8.com/color/48/whatsapp--v1.png" width="45">
            </a>
            <a href="https://t.me/share/url?url={site_url}" target="_blank">
                <img src="https://img.icons8.com/color/48/telegram-app--v1.png" width="45">
            </a>
        </div>
        <div style="background: linear-gradient(135deg, #d21034, #ff6b6b); color: white; padding: 8px 25px; border-radius: 50px; display: inline-block;">
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
    <div style="background: linear-gradient(135deg, #25F4EE, #FE2C55); padding: 25px; border-radius: 30px; color: white; text-align: center; margin: 25px 0; border: 3px solid white;">
        <div style="font-size: 2rem; margin-bottom: 10px;">🎵</div>
        <div style="font-size: 1.4rem; font-weight: bold; margin: 15px 0;">
            "تهنينا من التقرعيج، موقع راسم تيتانيوم راهو واجد! 🇩🇿"
        </div>
        <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin: 15px 0;">
            <span style="background: white; color: #FE2C55; padding: 5px 15px; border-radius: 50px;">#واد_كنيس</span>
            <span style="background: white; color: #FE2C55; padding: 5px 15px; border-radius: 50px;">#الجزائر</span>
            <span style="background: white; color: #FE2C55; padding: 5px 15px; border-radius: 50px;">#هواتف</span>
        </div>
        <div style="margin-top: 15px; background: rgba(255,255,255,0.2); padding: 10px; border-radius: 50px;">
            📱 58 ولاية
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
        st.metric("المستخدمين", users)
    with col2:
        st.metric("الإعلانات", ads)
    with col3:
        st.metric("الزيارات", visitors)
    with col4:
        st.metric("المشاهدات", views)

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
                    except:
                        st.error("❌ خطأ في تسجيل الدخول")
    
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
                    st.error("❌ كلمة المرور قصيرة جداً (6 أحرف على الأقل)")
                else:
                    try:
                        salt = secrets.token_hex(16)
                        hashed = hash_password(new_pass, salt)
                        
                        conn.execute("""
                            INSERT INTO users (username, password, salt, email, phone)
                            VALUES (?, ?, ?, ?, ?)
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
        
        query += " ORDER BY featured DESC, created_at DESC LIMIT 10"
        
        ads = conn.execute(query, params).fetchall()
        
        if ads:
            for ad in ads:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {ad[1]}")
                        st.write(f"📍 {ad[4]} | 👁️ {ad[8]} مشاهدة")
                        st.write(ad[5][:100] + "...")
                    with col2:
                        st.markdown(f"## 💰 {ad[2]:,} دج")
                        if st.button("📞 واتساب", key=f"wa_{ad[0]}"):
                            st.info(f"رقم الهاتف: {ad[3]}")
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
            # التحقق من الحقول المطلوبة
            if not title or price <= 0 or not phone:
                st.error("❌ يرجى ملء جميع الحقول المطلوبة (*)")
            else:
                try:
                    conn.execute("""
                        INSERT INTO ads (title, price, phone, wilaya, description, category, owner)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (title, price, phone, wilaya, description, category, st.session_state.user))
                    conn.commit()
                    
                    # تحديث عدد إعلانات المستخدم
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
        # جلب المحادثات
        conversations = conn.execute("""
            SELECT DISTINCT 
                CASE WHEN sender = ? THEN receiver ELSE sender END as contact,
                MAX(created_at) as last_msg,
                (SELECT COUNT(*) FROM messages WHERE receiver=? AND sender=contact AND read=0) as unread
            FROM messages 
            WHERE sender = ? OR receiver = ?
            GROUP BY contact
            ORDER BY last_msg DESC
        """, (user, user, user, user)).fetchall()
        
        if not conversations:
            st.info("لا توجد محادثات حالياً")
            return
        
        # عرض قائمة المحادثات
        contacts = [c[0] for c in conversations]
        selected = st.selectbox("اختر محادثة", contacts)
        
        if selected:
            st.subheader(f"الدردشة مع {selected}")
            
            # تحديث حالة القراءة
            conn.execute("UPDATE messages SET read=1 WHERE sender=? AND receiver=?", 
                        (selected, user))
            conn.commit()
            
            # عرض الرسائل
            messages = conn.execute("""
                SELECT sender, message, created_at FROM messages
                WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)
                ORDER BY created_at ASC
            """, (user, selected, selected, user)).fetchall()
            
            for msg in messages:
                if msg[0] == user:
                    st.markdown(f"<div style='background: #dcf8c6; padding: 10px; border-radius: 10px; margin: 5px 0; text-align: left;'><b>أنت:</b> {msg[1]}<br><small>{msg[2][11:16]}</small></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='background: white; padding: 10px; border-radius: 10px; margin: 5px 0;'><b>{msg[0]}:</b> {msg[1]}<br><small>{msg[2][11:16]}</small></div>", unsafe_allow_html=True)
            
            # إرسال رسالة جديدة
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
    
    # إحصائيات سريعة
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("المستخدمين", users)
    with col2:
        st.metric("الإعلانات", ads)
    with col3:
        st.metric("الزيارات", visitors)
    with col4:
        st.metric("المشاهدات", views)
    
    # عرض المستخدمين
    st.subheader("👥 المستخدمين")
    try:
        users_df = pd.read_sql_query("""
            SELECT username, role, verified, banned, ad_count, last_login 
            FROM users ORDER BY last_login DESC
        """, conn)
        st.dataframe(users_df, use_container_width=True)
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")

# ==========================================
# 14. التشغيل الرئيسي
# ==========================================
def main():
    """الدالة الرئيسية للتشغيل"""
    
    # تهيئة حالة الجلسة
    if "user" not in st.session_state:
        st.session_state.user = None
    if "role" not in st.session_state:
        st.session_state.role = "user"
    if "ip" not in st.session_state:
        st.session_state.ip = secrets.token_hex(8)
    if "page" not in st.session_state:
        st.session_state.page = "main"
    
    # تسجيل الزائر
    log_visitor()
    
    # التحقق من تسجيل الدخول
    if not st.session_state.user:
        login_page()
    else:
        conn = get_connection()
        
        # الشريط الجانبي
        with st.sidebar:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #006633, #d21034); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 20px;">
                <h3>🎖️ {st.session_state.user}</h3>
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
        
        # توجيه الصفحات
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
