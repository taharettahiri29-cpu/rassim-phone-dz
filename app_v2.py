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
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://t.me/RassimDZ',
        'Report a bug': 'https://t.me/RassimDZ',
        'About': '''
        # 🇩🇿 راسم تيتانيوم ألترا
        **أول سوق إلكتروني جزائري متخصص في الهواتف**
        
        - بيع وشراء في 58 ولاية
        - آمن وسريع ومجاني
        - تواصل مباشر مع البائعين
        '''
    }
)

# ==========================================
# 2. تحسين محركات البحث (SEO) بالكامل
# ==========================================
st.markdown("""
<meta name="description" content="راسم تيتانيوم - أفضل سوق للهواتف في الجزائر. بيع وشراء الهواتف المستعملة والجديدة في 58 ولاية. منصة آمنة وسريعة">
<meta name="keywords" content="واد كنيس, Ouedkniss, هواتف, الجزائر, بيع وشراء, راسم فون, تيتانيوم, سامسونج, ايفون, هواوي, تليفون, téléphone Algerie">
<meta name="author" content="RASSIM DZ">
<meta property="og:title" content="راسم تيتانيوم - سوق الهواتف الجزائري">
<meta property="og:description" content="أول سوق إلكتروني جزائري متخصص في الهواتف">
<meta name="twitter:card" content="summary_large_image">
""", unsafe_allow_html=True)

# ==========================================
# 3. التصميم المتكامل (CSS الكامل)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

* {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

/* ===== الهيدر الرئيسي ===== */
.main-header {
    background: linear-gradient(135deg, #006633 0%, #006633 48%, #d21034 50%, #ffffff 52%, #ffffff 100%);
    padding: 40px 20px;
    border-radius: 30px;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    margin-bottom: 30px;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { box-shadow: 0 20px 40px rgba(0,102,51,0.3); }
    to { box-shadow: 0 20px 60px rgba(210,16,52,0.5); }
}

.main-header h1 {
    color: white;
    font-size: 2.5rem;
    font-weight: 900;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    margin-bottom: 10px;
}

.main-header p {
    color: white;
    font-size: 1.2rem;
    opacity: 0.95;
}

/* ===== أزرار المشاركة الاجتماعية ===== */
.social-share {
    background: white;
    padding: 25px 20px;
    border-radius: 30px;
    margin: 25px 0;
    text-align: center;
    box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    border: 2px solid #006633;
}

.social-share h3 {
    color: #006633;
    font-size: 1.5rem;
    margin-bottom: 10px;
}

.social-grid {
    display: flex;
    justify-content: center;
    gap: 15px;
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
    transition: all 0.3s;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

.social-icon:hover {
    transform: scale(1.1) translateY(-5px);
    box-shadow: 0 10px 20px rgba(210,16,52,0.2);
}

.social-icon img {
    width: 30px;
    height: 30px;
}

.share-badge {
    background: linear-gradient(135deg, #d21034, #ff6b6b);
    color: white;
    padding: 8px 25px;
    border-radius: 50px;
    display: inline-block;
    font-weight: bold;
}

/* ===== قسم تيك توك ===== */
.tiktok-section {
    background: linear-gradient(135deg, #25F4EE, #FE2C55);
    padding: 25px;
    border-radius: 30px;
    color: white;
    text-align: center;
    margin: 25px 0;
    border: 3px solid white;
    animation: shake 0.8s ease;
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    20%, 60% { transform: translateX(-5px); }
    40%, 80% { transform: translateX(5px); }
}

.tiktok-quote {
    font-size: 1.4rem;
    font-weight: bold;
    margin: 15px 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.tiktok-features {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin: 15px 0;
}

.feature-tag {
    background: rgba(255,255,255,0.2);
    padding: 5px 15px;
    border-radius: 50px;
    font-size: 0.9rem;
    backdrop-filter: blur(5px);
}

.tiktok-hashtags {
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
    margin: 15px 0;
}

.hashtag {
    background: white;
    color: #FE2C55;
    padding: 5px 15px;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: bold;
}

/* ===== بطاقات الإحصائيات ===== */
.stats-container {
    display: flex;
    justify-content: space-between;
    gap: 15px;
    flex-wrap: wrap;
    margin: 25px 0;
}

.stat-card {
    flex: 1;
    min-width: 120px;
    background: white;
    padding: 20px 15px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    border-bottom: 4px solid #d21034;
}

.stat-value {
    font-size: 2.2rem;
    font-weight: 900;
    color: #d21034;
    line-height: 1.2;
}

.stat-label {
    font-size: 1rem;
    color: #006633;
    font-weight: 600;
    margin-top: 5px;
}

/* ===== بطاقات الإعلانات ===== */
.ad-card {
    background: white;
    border-radius: 25px;
    padding: 25px;
    margin-bottom: 20px;
    border-right: 8px solid #006633;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    transition: all 0.3s;
    animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.ad-card:hover {
    transform: translateX(-5px);
    border-right-color: #d21034;
    box-shadow: 0 15px 30px rgba(210,16,52,0.15);
}

.ad-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #d21034;
    margin-bottom: 10px;
}

.ad-price {
    background: linear-gradient(135deg, #006633, #00a86b);
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
    color: #666;
    margin: 15px 0;
    font-size: 0.95rem;
}

.ad-actions {
    display: flex;
    gap: 10px;
    margin-top: 15px;
}

.ad-btn {
    flex: 1;
    background: #f8f9fa;
    border: none;
    border-radius: 50px;
    padding: 10px;
    font-size: 0.95rem;
    color: #006633;
    cursor: pointer;
    transition: all 0.3s;
    font-weight: 600;
}

.ad-btn:hover {
    background: #006633;
    color: white;
}

/* ===== فقاعات الدردشة ===== */
.chat-container {
    background: #f8f9fa;
    border-radius: 20px;
    padding: 20px;
    max-height: 400px;
    overflow-y: auto;
}

.chat-bubble {
    padding: 12px 18px;
    border-radius: 18px;
    margin: 8px 0;
    max-width: 80%;
    animation: popIn 0.3s ease;
}

@keyframes popIn {
    from { transform: scale(0.9); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

.chat-sent {
    background: #dcf8c6;
    margin-left: auto;
    border-bottom-left-radius: 5px;
}

.chat-received {
    background: white;
    margin-right: auto;
    border-bottom-right-radius: 5px;
    border: 1px solid #eee;
}

/* ===== شارة المميز ===== */
.featured-badge {
    background: linear-gradient(135deg, #ffd700, #ffa500);
    color: white;
    padding: 4px 15px;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: bold;
    display: inline-block;
    margin-right: 10px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

/* ===== المساعد الذكي ===== */
.ai-section {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 25px;
    border-radius: 25px;
    color: white;
    margin: 25px 0;
}

/* ===== لوحة الإدارة ===== */
.admin-section {
    background: linear-gradient(135deg, #2c3e50, #3498db);
    padding: 25px;
    border-radius: 25px;
    color: white;
    margin: 25px 0;
}

/* ===== التجاوب مع الجوال ===== */
@media (max-width: 768px) {
    .main-header h1 { font-size: 1.8rem; }
    .stat-value { font-size: 1.8rem; }
    .ad-title { font-size: 1.3rem; }
    .ad-price { font-size: 1.1rem; padding: 6px 15px; }
    .social-icon { width: 40px; height: 40px; }
    .social-icon img { width: 24px; height: 24px; }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. إعدادات قاعدة البيانات
# ==========================================
DB = "rassim_titanium.db"

def init_db():
    """تهيئة قاعدة البيانات مع جميع الجداول"""
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
            visited_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    return conn

@st.cache_resource
def get_connection():
    """الحصول على اتصال قاعدة البيانات"""
    return sqlite3.connect(DB, check_same_thread=False)

# تهيئة قاعدة البيانات
init_db()

# ==========================================
# 5. دوال المساعدة
# ==========================================
def hash_password(password, salt):
    """تشفير كلمة المرور"""
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

def create_notification(username, message, notif_type="info"):
    """إنشاء إشعار جديد"""
    conn = get_connection()
    conn.execute(
        "INSERT INTO notifications (username, message, type) VALUES (?, ?, ?)",
        (username, message, notif_type)
    )
    conn.commit()

def log_visitor():
    """تسجيل زائر جديد"""
    conn = get_connection()
    conn.execute(
        "INSERT INTO visitors (ip, page) VALUES (?, ?)",
        (st.session_state.get('ip', 'unknown'), st.session_state.get('page', 'main'))
    )
    conn.commit()

def get_stats():
    """الحصول على إحصائيات الموقع"""
    conn = get_connection()
    users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    ads = conn.execute("SELECT COUNT(*) FROM ads WHERE status='active'").fetchone()[0]
    visitors = conn.execute("SELECT COUNT(*) FROM visitors").fetchone()[0]
    views = conn.execute("SELECT SUM(views) FROM ads").fetchone()[0] or 0
    return users, ads, visitors, views

# ==========================================
# 6. أزرار المشاركة الاجتماعية (المطلوبة)
# ==========================================
def show_social_share():
    """عرض أزرار المشاركة الاجتماعية"""
    site_url = "https://racim-phone.streamlit.app/"
    
    st.markdown(f"""
    <div class="social-share">
        <h3>📢 شارك الموقع مع أصدقائك</h3>
        <p style="color: #666;">ساعد في نشر الموقع واكسب الثواب 🤲</p>
        
        <div class="social-grid">
            <a href="https://www.facebook.com/sharer/sharer.php?u={site_url}" target="_blank" class="social-icon">
                <img src="https://img.icons8.com/color/48/facebook-new.png">
            </a>
            <a href="https://api.whatsapp.com/send?text=شوف هاد الموقع لبيع الهواتف: {site_url}" target="_blank" class="social-icon">
                <img src="https://img.icons8.com/color/48/whatsapp--v1.png">
            </a>
            <a href="https://t.me/share/url?url={site_url}" target="_blank" class="social-icon">
                <img src="https://img.icons8.com/color/48/telegram-app--v1.png">
            </a>
            <a href="#" onclick="navigator.clipboard.writeText('{site_url}'); alert('✅ تم نسخ الرابط!'); return false;" class="social-icon">
                <img src="https://img.icons8.com/color/48/link--v1.png">
            </a>
        </div>
        
        <div class="share-badge">
            👥 شارك مع 10 أصدقاء واكسب الدعاء
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 7. قسم تيك توك (المطلوب)
# ==========================================
def show_tiktok_section():
    """عرض قسم تيك توك"""
    st.markdown("""
    <div class="tiktok-section">
        <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 15px;">
            <span style="font-size: 2.5rem;">🎵</span>
            <span style="font-size: 1.5rem; font-weight: bold;">تيك توك الجزائر</span>
        </div>
        
        <div class="tiktok-quote">
            "تهنينا من التقرعيج في فيسبوك، موقع راسم تيتانيوم للدزة راهو واجد! 🇩🇿"
        </div>
        
        <div class="tiktok-features">
            <span class="feature-tag">🔥 تسوق بسهولة</span>
            <span class="feature-tag">⚡ بيع بسرعة</span>
            <span class="feature-tag">💬 تواصل مباشر</span>
        </div>
        
        <div class="tiktok-hashtags">
            <span class="hashtag">#واد_كنيس</span>
            <span class="hashtag">#الجزائر</span>
            <span class="hashtag">#هواتف</span>
            <span class="hashtag">#راسم_تيتانيوم</span>
        </div>
        
        <div style="margin-top: 20px;">
            <span style="background: white; color: #FE2C55; padding: 8px 25px; border-radius: 50px; font-weight: bold;">
                📱 58 ولاية - حمل التطبيق
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 8. بطاقات الإحصائيات
# ==========================================
def show_stats_cards():
    """عرض بطاقات الإحصائيات"""
    users, ads, visitors, views = get_stats()
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-value">{users}</div>
            <div class="stat-label">مستخدم</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{ads}</div>
            <div class="stat-label">إعلان</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{visitors}</div>
            <div class="stat-label">زيارة</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{views}</div>
            <div class="stat-label">مشاهدة</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 9. صفحة السوق الذكي
# ==========================================
def show_market(conn):
    """عرض السوق الذكي مع الفلاتر"""
    st.markdown('<div class="main-header"><h1>🛍️ السوق الذكي</h1><p>تصفح آلاف الهواتف في 58 ولاية</p></div>', unsafe_allow_html=True)
    
    # إحصائيات سريعة
    show_stats_cards()
    
    # أزرار المشاركة
    show_social_share()
    
    # قسم تيك توك
    show_tiktok_section()
    
    # فلاتر البحث
    with st.expander("🔍 فلترة البحث", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            wilaya = st.selectbox("الولاية", ["الكل"] + [f"{i:02d}" for i in range(1, 59)])
        with col2:
            category = st.selectbox("القسم", ["الكل", "سامسونج", "آيفون", "هواوي", "شاومي", "أخرى"])
        with col3:
            sort = st.selectbox("الترتيب", ["الأحدث", "الأكثر مشاهدة", "الأعلى سعراً", "الأقل سعراً"])
        
        search = st.text_input("🔎 بحث عن هاتف", placeholder="اكتب اسم الهاتف...")
        
        if st.button("🔍 بحث", use_container_width=True):
            st.success("جاري البحث...")
    
    # عرض الإعلانات
    ads = conn.execute("""
        SELECT * FROM ads 
        WHERE status='active' 
        ORDER BY featured DESC, created_at DESC 
        LIMIT 10
    """).fetchall()
    
    if ads:
        for ad in ads:
            featured_badge = '<span class="featured-badge">⭐ مميز</span>' if ad[9] else ''
            
            st.markdown(f"""
            <div class="ad-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span class="ad-title">{ad[1]}</span>
                        {featured_badge}
                    </div>
                    <span class="ad-price">{ad[2]:,} دج</span>
                </div>
                
                <div class="ad-details">
                    <span>📍 {ad[4]}</span>
                    <span>👁️ {ad[8]} مشاهدة</span>
                    <span>📅 {ad[12][:10]}</span>
                </div>
                
                <p style="color: #666; margin: 10px 0;">{ad[5][:100]}...</p>
                
                <div class="ad-actions">
                    <button class="ad-btn" onclick="window.open('https://wa.me/213{ad[3]}')">📞 واتساب</button>
                    <button class="ad-btn">❤️ حفظ</button>
                    <button class="ad-btn">💬 مراسلة</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("لا توجد إعلانات حالياً")

# ==========================================
# 10. صفحة إضافة إعلان
# ==========================================
def post_ad(conn):
    st.markdown('<div class="main-header"><h1>📢 إضافة إعلان جديد</h1></div>', unsafe_allow_html=True)
    
    with st.form("new_ad_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("اسم الهاتف")
            category = st.selectbox("الفئة", ["سامسونج", "آيفون", "هواوي", "شاومي", "أخرى"])
        with col2:
            price = st.number_input("السعر (دج)", min_value=0, step=1000)
            wilaya = st.selectbox("الولاية", [f"{i:02d}" for i in range(1, 59)])
        
        phone = st.text_input("رقم الهاتف")
        description = st.text_area("وصف الهاتف")
        
        if st.form_submit_button("🚀 نشر الإعلان", use_container_width=True):
            if title and price > 0 and phone:
                conn.execute("""
                    INSERT INTO ads (title, price, phone, wilaya, description, category, owner)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (title, price, phone, wilaya, description, category, st.session_state.user))
                conn.commit()
                st.success("✅ تم نشر الإعلان بنجاح!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ يرجى ملء جميع الحقول المطلوبة")

# ==========================================
# 11. نظام الدردشة
# ==========================================
def show_chat(conn):
    st.markdown('<div class="main-header"><h1>💬 المحادثات</h1></div>', unsafe_allow_html=True)
    
    user = st.session_state.user
    
    # جلب المحادثات
    conversations = conn.execute("""
        SELECT DISTINCT 
            CASE WHEN sender = ? THEN receiver ELSE sender END as contact,
            MAX(created_at) as last_msg
        FROM messages 
        WHERE sender = ? OR receiver = ?
        GROUP BY contact
        ORDER BY last_msg DESC
    """, (user, user, user)).fetchall()
    
    if not conversations:
        st.info("لا توجد محادثات حالياً")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("المحادثات")
        contacts = [c[0] for c in conversations]
        selected = st.radio("", contacts)
    
    with col2:
        if selected:
            st.subheader(f"الدردشة مع {selected}")
            
            # عرض الرسائل
            messages = conn.execute("""
                SELECT sender, message, created_at FROM messages
                WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)
                ORDER BY created_at ASC
            """, (user, selected, selected, user)).fetchall()
            
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in messages:
                if msg[0] == user:
                    st.markdown(f'<div class="chat-bubble chat-sent"><b>أنت:</b> {msg[1]}<br><small>{msg[2][11:16]}</small></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-bubble chat-received"><b>{msg[0]}:</b> {msg[1]}<br><small>{msg[2][11:16]}</small></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # إرسال رسالة
            with st.form("send_message", clear_on_submit=True):
                msg = st.text_input("اكتب رسالتك...")
                if st.form_submit_button("إرسال", use_container_width=True) and msg:
                    conn.execute("""
                        INSERT INTO messages (sender, receiver, message)
                        VALUES (?, ?, ?)
                    """, (user, selected, msg))
                    conn.commit()
                    st.rerun()

# ==========================================
# 12. لوحة الإدارة
# ==========================================
def admin_dashboard(conn):
    st.markdown('<div class="admin-section"><h1 style="color:white; text-align:center;">🔐 لوحة الإدارة</h1></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 الإحصائيات", "👥 المستخدمين", "🚨 البلاغات"])
    
    with tab1:
        users, ads, visitors, views = get_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("المستخدمين", users)
        col2.metric("الإعلانات", ads)
        col3.metric("الزيارات", visitors)
        col4.metric("المشاهدات", views)
        
        # رسم بياني
        daily_visits = conn.execute("""
            SELECT date(visited_at) as date, COUNT(*) as count
            FROM visitors
            GROUP BY date
            ORDER BY date DESC
            LIMIT 7
        """).fetchall()
        
        if daily_visits:
            df = pd.DataFrame(daily_visits, columns=["التاريخ", "الزيارات"])
            fig = px.line(df, x="التاريخ", y="الزيارات", title="آخر 7 أيام")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        users_df = pd.read_sql_query("SELECT username, role, verified, banned, ad_count FROM users", conn)
        st.dataframe(users_df, use_container_width=True)
    
    with tab3:
        reports = conn.execute("""
            SELECT r.id, a.title, r.reporter, r.reason, r.status
            FROM reports r JOIN ads a ON r.ad_id = a.id
            WHERE r.status = 'pending'
        """).fetchall()
        
        if reports:
            for report in reports:
                st.warning(f"إعلان: {report[1]} - سبب: {report[3]}")
                if st.button(f"معالجة {report[0]}"):
                    conn.execute("UPDATE reports SET status='resolved' WHERE id=?", (report[0],))
                    conn.commit()
                    st.rerun()
        else:
            st.info("لا توجد بلاغات معلقة")

# ==========================================
# 13. صفحة تسجيل الدخول
# ==========================================
def login_page():
    st.markdown("""
    <div class="main-header">
        <h1>🇩🇿 راسم تيتانيوم ألترا</h1>
        <p>أول سوق إلكتروني جزائري للهواتف</p>
    </div>
    """, unsafe_allow_html=True)
    
    # إحصائيات
    show_stats_cards()
    
    # أزرار المشاركة
    show_social_share()
    
    # قسم تيك توك
    show_tiktok_section()
    
    tab1, tab2 = st.tabs(["🔑 تسجيل الدخول", "📝 حساب جديد"])
    conn = get_connection()
    
    with tab1:
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        
        if st.button("دخول", use_container_width=True):
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
    
    with tab2:
        new_user = st.text_input("اسم المستخدم الجديد")
        new_pass = st.text_input("كلمة المرور الجديدة", type="password")
        email = st.text_input("البريد الإلكتروني")
        phone = st.text_input("رقم الهاتف")
        
        if st.button("تسجيل", use_container_width=True):
            if new_user and new_pass:
                try:
                    salt = secrets.token_hex(16)
                    hashed = hash_password(new_pass, salt)
                    
                    conn.execute("""
                        INSERT INTO users (username, password, salt, email, phone)
                        VALUES (?, ?, ?, ?, ?)
                    """, (new_user, hashed, salt, email, phone))
                    conn.commit()
                    
                    st.success("✅ تم التسجيل بنجاح! يمكنك الدخول الآن")
                except:
                    st.error("❌ اسم المستخدم موجود مسبقاً")

# ==========================================
# 14. التشغيل الرئيسي
# ==========================================
def main():
    # تهيئة حالة الجلسة
    if "user" not in st.session_state:
        st.session_state.user = None
    if "role" not in st.session_state:
        st.session_state.role = "user"
    if "ip" not in st.session_state:
        st.session_state.ip = secrets.token_hex(8)
    
    # تسجيل الزائر
    log_visitor()
    
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
            st.markdown('<div class="ai-section"><h1 style="color:white;">🤖 المساعد الذكي</h1><p style="color:white;">قريباً...</p></div>', unsafe_allow_html=True)
        elif menu == "🛡️ الإدارة" and st.session_state.role == "admin":
            admin_dashboard(conn)

if __name__ == "__main__":
    main()
