import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import secrets
import time
import plotly.graph_objects as go
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# ==========================================
# 1. إعدادات الصفحة المتقدمة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS ULTIMATE 2026 • الجزائر",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. المتغيرات السرية في الجلسة
# ==========================================
if 'admin_access' not in st.session_state:
    st.session_state.admin_access = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'role' not in st.session_state:
    st.session_state.role = "user"
if 'verified' not in st.session_state:
    st.session_state.verified = 0
if 'ip' not in st.session_state:
    st.session_state.ip = secrets.token_hex(8)

# ==========================================
# 3. نظام "الذكاء العصبي" للواجهة (Neural UI)
# ==========================================
def set_ultimate_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Space Grotesk', 'Inter', sans-serif;
        direction: rtl;
        box-sizing: border-box;
    }

    .stApp {
        background: radial-gradient(circle at 20% 20%, #1a1a2a, #0a0a0f);
        color: #ffffff;
        min-height: 100vh;
    }

    /* تأثير الجسيمات المتحركة */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(2px 2px at 10px 10px, rgba(0, 255, 255, 0.2), transparent),
            radial-gradient(3px 3px at 50px 100px, rgba(255, 0, 255, 0.2), transparent);
        background-repeat: repeat;
        background-size: 600px 600px;
        opacity: 0.3;
        pointer-events: none;
        z-index: 0;
        animation: quantumFloat 30s linear infinite;
    }

    @keyframes quantumFloat {
        0% { transform: translateY(0) rotate(0deg); }
        100% { transform: translateY(-100px) rotate(5deg); }
    }

    /* الهيدر العصبي */
    .neural-header {
        background: rgba(10, 10, 20, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(0, 255, 255, 0.2);
        padding: 30px;
        margin-bottom: 30px;
        border-radius: 30px;
        text-align: center;
        animation: neuralGlow 3s ease-in-out infinite;
    }

    @keyframes neuralGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.2); }
        50% { box-shadow: 0 0 40px rgba(255, 0, 255, 0.3); }
    }

    .neural-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00ffff, #ff00ff, #00ffff);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientPulse 5s ease infinite;
    }

    @keyframes gradientPulse {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    /* كرت إعلاني بتأثير الهولوغرام */
    .hologram-card {
        background: rgba(20, 20, 30, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 255, 0.1);
        border-radius: 30px;
        padding: 25px;
        margin-bottom: 20px;
        transition: all 0.4s ease;
    }

    .hologram-card:hover {
        border-color: #00ffff;
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 255, 255, 0.2);
    }

    /* زر الـ Cyber-Action */
    .stButton > button {
        background: linear-gradient(90deg, #00ffff, #ff00ff) !important;
        border: none !important;
        color: black !important;
        font-weight: 800 !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 0, 255, 0.4) !important;
    }

    /* بطاقات الإحصائيات */
    .stat-card {
        background: rgba(20, 20, 30, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 255, 0.1);
        border-radius: 25px;
        padding: 20px;
        text-align: center;
        transition: all 0.4s ease;
    }

    .stat-card:hover {
        border-color: #ff00ff;
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(255, 0, 255, 0.2);
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #00ffff;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }

    .stat-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1rem;
        margin-top: 5px;
    }

    /* شريط التمرير */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.02);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00ffff, #ff00ff);
        border-radius: 10px;
    }

    /* التجاوب مع الجوال */
    @media screen and (max-width: 768px) {
        .neural-title { font-size: 2rem; }
        .stat-value { font-size: 1.8rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. نظام التحليل التنبئي
# ==========================================
def show_market_trends(conn):
    st.markdown("### 📈 نبض السوق الجزائري")
    
    try:
        df = pd.read_sql_query("""
            SELECT category, COUNT(*) as count, AVG(price) as avg_price 
            FROM ads 
            WHERE status='active' 
            GROUP BY category 
            ORDER BY count DESC 
            LIMIT 8
        """, conn)
        
        if not df.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df['count'],
                y=df['category'],
                orientation='h',
                marker=dict(color='#00ffff', line=dict(color='#ff00ff', width=2))
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("جاري تحميل التحليلات...")

# ==========================================
# 5. محرك البحث الذكي
# ==========================================
def quantum_search_ui():
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search_query = st.text_input("", placeholder="🔍 ابحث عن هاتف (مثلاً: iPhone 15 Pro Max)...")
    with col2:
        st.selectbox("", ["🧠 أفضل سعر", "⚡ الأكثر ثقة"], label_visibility="collapsed")
    with col3:
        st.button("🔮 Flash Scan", use_container_width=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        wilaya = st.selectbox("الولاية", ["الكل"] + [f"{i:02d}" for i in range(1, 59)])
    with col_b:
        sort = st.selectbox("الترتيب", ["الأحدث", "السعر", "المشاهدات"])
    
    return search_query, wilaya, sort

# ==========================================
# 6. دالة الإعلان الذهبية
# ==========================================
def render_ad_pro(ad):
    st.markdown(f"""
    <div class="hologram-card">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span>📍 {ad['wilaya']}</span>
            <span>👁️ {ad['views']}</span>
        </div>
        <h2 style="color: #00ffff; margin: 10px 0;">{ad['title']}</h2>
        <h1 style="color: #ff00ff;">{ad['price']:,} دج</h1>
        <p style="color: #aaa;">{ad['description'][:100]}...</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📞 اتصل بالبائع", key=f"call_{ad['id']}", use_container_width=True):
            st.info(f"رقم الهاتف: {ad['phone']}")
    with col2:
        if st.button("⚡ شراء سريع", key=f"buy_{ad['id']}", use_container_width=True):
            st.success("تم إرسال طلبك إلى البائع")

# ==========================================
# 7. إعدادات قاعدة البيانات
# ==========================================
DB = "rassim_os_ultimate.db"

def init_db():
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
                views INTEGER DEFAULT 0,
                featured INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                owner TEXT NOT NULL,
                verified INTEGER DEFAULT 0,
                date TEXT DEFAULT CURRENT_TIMESTAMP
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

# ==========================================
# 8. دوال المساعدة
# ==========================================
def hash_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

def log_visitor():
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO visitors (ip, page) VALUES (?, ?)",
            (st.session_state.ip, st.session_state.get('page', 'main'))
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

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)

# تهيئة قاعدة البيانات
conn = init_db()

# ==========================================
# 9. صفحة تسجيل الدخول
# ==========================================
def login_page():
    st.markdown("""
    <div class="neural-header">
        <div class="neural-title">RASSIM OS ULTIMATE</div>
        <p style="color: white;">أول سوق إلكتروني جزائري بتقنية Quantum AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    users, ads, visitors, views = get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{users}</div><div class="stat-label">مستخدم</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{ads}</div><div class="stat-label">إعلان</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{visitors}</div><div class="stat-label">زيارة</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{views}</div><div class="stat-label">مشاهدة</div></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 دخول", "📝 حساب جديد"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("👤 اسم المستخدم")
            password = st.text_input("🔐 كلمة المرور", type="password")
            
            if st.form_submit_button("⚡ دخول", use_container_width=True):
                if username == "admin" and password == "admin":
                    st.session_state.user = "admin"
                    st.session_state.role = "admin"
                    st.rerun()
                else:
                    st.error("❌ بيانات غير صحيحة")
    
    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("👤 اسم المستخدم")
            new_pass = st.text_input("🔐 كلمة المرور", type="password")
            
            if st.form_submit_button("✨ تسجيل", use_container_width=True):
                if new_user and new_pass:
                    st.success("✅ تم التسجيل بنجاح!")

# ==========================================
# 10. صفحة السوق الذكي
# ==========================================
def show_market():
    st.markdown("### 🛍️ السوق الذكي")
    
    search_query, wilaya, sort = quantum_search_ui()
    
    with st.expander("📊 تحليلات السوق", expanded=False):
        show_market_trends(conn)
    
    # إعلانات تجريبية
    ads = [
        {"id": 1, "title": "iPhone 15 Pro Max Titanium", "price": 225000, "phone": "0555-XX-XX-XX", 
         "wilaya": "الجزائر (16)", "description": "نظيف جداً، مع كامل أكسسواراته", "views": 1024},
        {"id": 2, "title": "Samsung S24 Ultra", "price": 185000, "phone": "0666-XX-XX-XX", 
         "wilaya": "وهران (31)", "description": "حالة ممتازة، بطارية 100%", "views": 856},
        {"id": 3, "title": "Xiaomi 14 Pro", "price": 95000, "phone": "0777-XX-XX-XX", 
         "wilaya": "قسنطينة (25)", "description": "جديد لم يستعمل", "views": 623}
    ]
    
    for ad in ads:
        render_ad_pro(ad)

# ==========================================
# 11. صفحة إضافة إعلان
# ==========================================
def post_ad():
    st.markdown("### 📢 إضافة إعلان جديد")
    
    with st.form("new_ad_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("📱 اسم المنتج *")
            category = st.selectbox("🏷️ الفئة", ["سامسونج", "آيفون", "هواوي", "شاومي", "أخرى"])
        with col2:
            price = st.number_input("💰 السعر (دج) *", min_value=0, step=1000)
            wilaya = st.selectbox("📍 الولاية *", [f"{i:02d}" for i in range(1, 59)])
        
        phone = st.text_input("📞 رقم الهاتف *")
        description = st.text_area("📝 الوصف")
        
        if st.form_submit_button("🚀 نشر الإعلان", use_container_width=True):
            if title and phone:
                st.success("✅ تم نشر الإعلان بنجاح!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ يرجى ملء الحقول المطلوبة")

# ==========================================
# 12. لوحة الإدارة السرية
# ==========================================
def admin_dashboard():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00ffff20, #ff00ff20); 
    border: 2px solid #00ffff; border-radius: 30px; padding: 30px; margin-bottom: 30px;">
        <h1 style="text-align: center; color: white;">🔐 لوحة التحكم السرية</h1>
        <p style="text-align: center; color: #00ffff;">مستوى الدخول: القائد 🛰️</p>
    </div>
    """, unsafe_allow_html=True)
    
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
# 13. التشغيل الرئيسي النهائي
# ==========================================
def main():
    # تطبيق الثيم
    set_ultimate_theme()
    
    # تسجيل الزائر
    log_visitor()
    
    # عرض الصفحة المناسبة
    if not st.session_state.user:
        login_page()
    else:
        # القائمة الجانبية
        with st.sidebar:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #00ffff20, #ff00ff20); 
            border-radius: 20px; padding: 20px; text-align: center; margin-bottom: 20px;">
                <div style="font-size: 3rem;">⚡</div>
                <div style="color: white; font-size: 1.2rem;">{st.session_state.user}</div>
            </div>
            """, unsafe_allow_html=True)
            
            menu = st.radio("", ["🛍️ السوق", "📢 إضافة إعلان", "🤖 المساعد"])
            
            if st.session_state.role == "admin":
                with st.expander("🔧 النظام"):
                    code = st.text_input("كود الدخول", type="password")
                    if code == "RASSIM-42-2026":
                        st.session_state.admin_access = True
            
            if st.button("🚪 خروج", use_container_width=True):
                st.session_state.user = None
                st.session_state.admin_access = False
                st.rerun()
        
        # توجيه الصفحات
        if st.session_state.admin_access:
            admin_dashboard()
        elif menu == "🛍️ السوق":
            show_market()
        elif menu == "📢 إضافة إعلان":
            post_ad()
        else:
            st.info("🤖 المساعد الذكي قيد التطوير")

# ==========================================
# 14. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()
