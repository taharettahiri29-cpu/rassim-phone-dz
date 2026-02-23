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
    page_title="RASSIM OS ULTIMATE 2026 • 69 ولاية",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. قائمة الولايات الجزائرية (69 ولاية)
# ==========================================
ALGERIAN_WILAYAS = [
    "الكل",
    "01 - أدرار", "02 - الشلف", "03 - الأغواط", "04 - أم البواقي", "05 - باتنة",
    "06 - بجاية", "07 - بسكرة", "08 - بشار", "09 - البليدة", "10 - البويرة",
    "11 - تمنراست", "12 - تبسة", "13 - تلمسان", "14 - تيارت", "15 - تيزي وزو",
    "16 - الجزائر", "17 - الجلفة", "18 - جيجل", "19 - سطيف", "20 - سعيدة",
    "21 - سكيكدة", "22 - سيدي بلعباس", "23 - عنابة", "24 - قالمة", "25 - قسنطينة",
    "26 - المدية", "27 - مستغانم", "28 - المسيلة", "29 - معسكر", "30 - ورقلة",
    "31 - وهران", "32 - البيض", "33 - إليزي", "34 - برج بوعريريج", "35 - بومرداس",
    "36 - الطارف", "37 - تندوف", "38 - تيسمسيلт", "39 - الوادي", "40 - خنشلة",
    "41 - سوق أهراس", "42 - تيبازة", "43 - ميلة", "44 - عين الدفلى", "45 - النعامة",
    "46 - عين تموشنت", "47 - غرداية", "48 - غليزان", "49 - تيميمون", "50 - برج باجي مختار",
    "51 - أولاد جلال", "52 - بني عباس", "53 - عين صالح", "54 - عين قزام", "55 - توقرت",
    "56 - جانت", "57 - المغير", "58 - المنيع", "59 - الطيبات", "60 - أولاد سليمان",
    "61 - سيدي خالد", "62 - بوسعادة", "63 - عين وسارة", "64 - حاسي بحبح", "65 - عين الملح",
    "66 - سيدي عيسى", "67 - عين الباردة", "68 - عين آزال", "69 - عين الحجر"
]

# ==========================================
# 3. المتغيرات السرية في الجلسة
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
if 'robot_active' not in st.session_state:
    st.session_state.robot_active = False
if 'last_alert' not in st.session_state:
    st.session_state.last_alert = None

# ==========================================
# 4. إعدادات قاعدة البيانات
# ==========================================
DB = "rassim_os_ultimate.db"

def init_db():
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
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
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
                views INTEGER DEFAULT 0,
                featured INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                owner TEXT NOT NULL,
                verified INTEGER DEFAULT 0,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                message TEXT NOT NULL,
                read INTEGER DEFAULT 0,
                date TEXT DEFAULT CURRENT_TIMESTAMP
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
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                price INTEGER,
                status TEXT DEFAULT 'new',
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
    return sqlite3.connect(DB, check_same_thread=False)

conn = init_db()

# ==========================================
# 5. دوال التشفير
# ==========================================
def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    ).hex()

# ==========================================
# 6. دوال المساعدة
# ==========================================
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

@st.cache_data(ttl=600)
def load_data_optimized():
    try:
        conn = get_connection()
        data = {
            'users': conn.execute("SELECT COUNT(*) FROM users").fetchone()[0],
            'ads': conn.execute("SELECT COUNT(*) FROM ads WHERE status='active'").fetchone()[0],
            'visitors': conn.execute("SELECT COUNT(*) FROM visitors").fetchone()[0],
            'views': conn.execute("SELECT SUM(views) FROM ads").fetchone()[0] or 0
        }
        return data
    except:
        return None

# ==========================================
# 7. نظام "الذكاء العصبي" للواجهة
# ==========================================
def set_ultimate_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');

    * {
        font-family: 'Cairo', 'Space Grotesk', 'Inter', sans-serif !important;
        box-sizing: border-box;
    }

    .stApp {
        background: radial-gradient(circle at 20% 20%, #1a1a2a, #0a0a0f);
        color: #ffffff;
        min-height: 100vh;
    }

    h1, h2, h3, h4, h5, h6, p, span, div, button, label, .stMarkdown {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Cairo', sans-serif !important;
        line-height: 1.6 !important;
    }

    .stat-value {
        font-family: 'Space Grotesk', monospace !important;
        direction: ltr !important;
        text-align: center !important;
    }

    .stTextInput input, .stTextArea textarea {
        direction: rtl !important;
        text-align: right !important;
    }

    .neural-header {
        background: rgba(10, 10, 20, 0.7);
        backdrop-filter: blur(20px);
        padding: 30px;
        margin-bottom: 30px;
        border-radius: 30px;
        text-align: center;
        border-bottom: 1px solid rgba(0, 255, 255, 0.2);
    }

    .neural-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00ffff, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #00ffff, #ff00ff) !important;
        border: none !important;
        color: black !important;
        font-weight: 800 !important;
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
    }

    .hologram-card {
        background: rgba(20, 20, 30, 0.4);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 255, 0.1);
        border-radius: 30px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.4s ease;
    }

    .hologram-card:hover {
        border-color: #00ffff;
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 255, 255, 0.2);
    }

    .wilaya-badge {
        display: inline-block;
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid #00ffff;
        border-radius: 50px;
        padding: 8px 15px;
        margin: 5px;
        color: #00ffff;
        white-space: nowrap;
    }

    .wilaya-counter {
        background: linear-gradient(135deg, #00ffff, #ff00ff);
        border-radius: 60px;
        padding: 20px 40px;
        text-align: center;
        margin: 20px 0;
    }

    .wilaya-counter h2 {
        color: black;
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        direction: ltr !important;
    }

    .chat-bubble {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: linear-gradient(135deg, #00ffff, #ff00ff);
        width: 70px;
        height: 70px;
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
        50% { transform: translateY(-15px); }
    }

    .radar-alert {
        background: rgba(255, 0, 0, 0.2);
        border: 2px solid #ff00ff;
        border-radius: 20px;
        padding: 15px;
        margin: 10px 0;
    }

    .stat-card {
        background: rgba(20, 20, 30, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 255, 0.1);
        border-radius: 25px;
        padding: 20px;
        text-align: center;
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #00ffff;
    }

    .stat-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1rem;
        margin-top: 5px;
    }

    @media screen and (max-width: 768px) {
        .neural-title { font-size: 2rem; }
        .stat-value { font-size: 1.8rem; }
        .chat-bubble { width: 60px; height: 60px; }
        .wilaya-counter h2 { font-size: 2rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 8. كاشف المشتري الجدي
# ==========================================
def serious_buyer_detector(message, price_offered=0):
    serious_keywords = [
        "حاب نشري", "نخلصك توت سويت", "وين نسكنو", 
        "كاش", "آخر سعر", "دابا", "نروحو نخلصو", "العنوان"
    ]
    
    message_lower = message.lower() if message else ""
    is_serious = any(word in message_lower for word in serious_keywords)
    
    if is_serious or price_offered > 0:
        st.session_state.last_alert = {
            'message': message,
            'price': price_offered,
            'time': datetime.now().strftime("%H:%M:%S")
        }
        
        st.toast("🚨 تنبيه: مشتري جدي!", icon="💰")
        st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>', unsafe_allow_html=True)
        return True
    return False

# ==========================================
# 9. روبوت RASSIM الذكي
# ==========================================
def rassim_robot_logic(user_message):
    user_message = user_message.lower()
    
    responses = {
        "سعر": "أسعارنا الأفضل في الجزائر 🇩🇿، تفقد الإعلانات!",
        "متوفر": "كل الإعلانات المعروضة متوفرة حالياً",
        "تيبازة": "مقرنا في فوكة (42). التوصيل لـ69 ولاية 🚚",
        "سلام": "وعليكم السلام! أنا روبوت RASSIM، كيف أساعدك؟",
        "آيفون": "آيفون متوفر بكثرة، ابحث في السوق 🔍",
        "سامسونج": "S24 Ultra بـ185,000 دج شامل الضمان ✅",
        "هواوي": "هواوي متوفرة، ابحث عن P60 Pro!",
        "شاومي": "Xiaomi 14 Pro بـ95,000 دج فقط!",
        "واد كنيس": "بديل واد كنيس العصري، أسرع وأذكى ✨",
        "الدزة": "الدزة الجزائرية واجدة! 🚀",
        "وين": "مقرنا فوكة (42) - نغطي 69 ولاية!",
        "69": "69 ولاية جزائرية كاملة! 🇩🇿",
        "ولايات": "من تندوف للطارف - 69 ولاية",
        "توصيل": "التوصيل لكل الولايات 📦"
    }
    
    for key in responses:
        if key in user_message:
            if key in ["حاب نشري", "كاش", "وين"]:
                serious_buyer_detector(user_message)
            return responses[key]
    
    return "رسالتك وصلت! سأرد قريباً. هل تريد رقم الهاتف؟"

# ==========================================
# 10. رادار راسم الآلي
# ==========================================
def robotic_alert_ui():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🛰️ رادار راسم")
    
    if st.sidebar.toggle("وضع الصياد"):
        st.session_state.robot_active = True
        st.sidebar.success("🟢 يراقب الصفقات...")
        
        if st.session_state.last_alert:
            with st.sidebar.expander("🚨 آخر عرض"):
                st.markdown(f"**{st.session_state.last_alert['message']}**\n💰 {st.session_state.last_alert['price']} دج\n⏰ {st.session_state.last_alert['time']}")
                st.markdown("[📞 واتساب](https://wa.me/213555555555)")
    else:
        st.session_state.robot_active = False
        st.sidebar.warning("🔴 الرادار مطفأ")

# ==========================================
# 11. مولد الإعلانات الذكي
# ==========================================
def generate_auto_ads():
    hour = datetime.now().hour
    if 18 <= hour <= 22:
        st.sidebar.markdown("<p style='color:#00ffff;'>🔥 وقت الذروة! انشر الآن</p>", unsafe_allow_html=True)
    elif 9 <= hour <= 12:
        st.sidebar.markdown("<p style='color:#ff00ff;'>☀️ وقت الصباح الذهبي</p>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<p style='color:#888;'>⏳ وقت هادئ</p>", unsafe_allow_html=True)

# ==========================================
# 12. عداد الولايات
# ==========================================
def show_wilaya_counter():
    st.markdown('<div class="wilaya-counter"><h2>69</h2><p>ولاية جزائرية مدعومة 🇩🇿</p></div>', unsafe_allow_html=True)

def show_wilaya_badges():
    cols = st.columns(5)
    for i, w in enumerate(ALGERIAN_WILAYAS[1:]):
        with cols[i % 5]:
            st.markdown(f"<span class='wilaya-badge'>{w}</span>", unsafe_allow_html=True)

# ==========================================
# 13. نظام الدردشة المباشرة
# ==========================================
def show_live_chat():
    st.markdown("""
    <div class="chat-bubble" onclick="document.getElementById('chat-trigger').click();">
        <img src="https://img.icons8.com/ios-filled/30/000000/speech-bubble.png" width="35">
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 💬 الدعم الذكي")
        generate_auto_ads()
        
        with st.expander("🗣️ روبوت RASSIM"):
            st.write("أهلاً! أنا روبوت راسم الذكي.")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("[![WhatsApp](https://img.icons8.com/color/48/whatsapp.png)](https://wa.me/213555555555)")
            with col2:
                st.markdown("[![Telegram](https://img.icons8.com/color/48/telegram-app.png)](https://t.me/RassimDZ)")
            
            msg = st.text_area("رسالتك:", key="robot_msg")
            if st.button("🤖 إرسال"):
                if msg:
                    reply = rassim_robot_logic(msg)
                    st.info(f"🤖 {reply}")

# ==========================================
# 14. نظام التحليل التنبئي
# ==========================================
def show_market_trends(conn):
    st.markdown("### 📈 نبض السوق")
    try:
        df = pd.read_sql_query("SELECT category, COUNT(*) as c FROM ads WHERE status='active' GROUP BY category", conn)
        if not df.empty:
            fig = go.Figure(go.Bar(x=df['c'], y=df['category'], orientation='h', marker_color='#00ffff'))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', height=300)
            st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("جاري التحميل...")

# ==========================================
# 15. محرك البحث الذكي (مختصر)
# ==========================================
def quantum_search_ui():
    col1, col2 = st.columns([3, 1])
    with col1:
        q = st.text_input("", placeholder="🔍 ابحث عن هاتف...")
    with col2:
        st.selectbox("", ["أفضل سعر", "الأحدث"], label_visibility="collapsed")
    
    col_a, col_b = st.columns(2)
    with col_a:
        w = st.selectbox("الولاية", ALGERIAN_WILAYAS)
    with col_b:
        s = st.selectbox("الترتيب", ["الأحدث", "السعر"])
    return q, w, s

# ==========================================
# 16. دالة الإعلان المختصرة والأنيقة (المطلوبة)
# ==========================================
def render_ad_pro(ad):
    """عرض الإعلان بشكل مختصر وأنيق"""
    
    phone_display = ad['phone'][:4] + "••••" + ad['phone'][-4:] if len(ad['phone']) > 8 else ad['phone']
    verified = "✅" if ad.get('verified') else "⚠️"
    verified_color = "#00ffff" if ad.get('verified') else "#ff00ff"
    
    st.markdown(f"""
    <div class="hologram-card" style="padding: 20px;">
        <div style="display: flex; justify-content: space-between; color: #888; font-size: 0.9rem; margin-bottom: 10px;">
            <span>📍 {ad['wilaya']}</span>
            <span>👁️ {ad['views']}</span>
            <span style="color: {verified_color};">{verified}</span>
        </div>
        
        <h3 style="color: #00ffff; margin: 10px 0; font-size: 1.4rem;">{ad['title']}</h3>
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 15px 0;">
            <h2 style="color: #ff00ff; margin: 0; font-size: 1.8rem;">{ad['price']:,} دج</h2>
            <div style="background: rgba(255,0,255,0.1); padding: 6px 15px; border-radius: 50px;">
                <span style="color: #ff00ff; font-weight: bold;">📞 {phone_display}</span>
            </div>
        </div>
        
        <p style="color: #aaa; margin: 10px 0; font-size: 0.95rem;">{ad['description'][:80]}...</p>
        
        <div style="display: flex; gap: 10px; margin-top: 15px;">
            <a href="https://wa.me/{ad['phone']}" target="_blank" style="flex: 1; text-decoration: none;">
                <button style="width:100%; padding:12px; background:#25D366; border:none; border-radius:12px; color:white; font-weight:bold; cursor:pointer; font-size:0.95rem;">📱 واتساب</button>
            </a>
            <a href="tel:{ad['phone']}" style="flex: 1; text-decoration: none;">
                <button style="width:100%; padding:12px; background:linear-gradient(90deg, #00ffff, #ff00ff); border:none; border-radius:12px; color:black; font-weight:bold; cursor:pointer; font-size:0.95rem;">📞 اتصال</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 17. صفحة تسجيل الدخول
# ==========================================
def login_page(conn):
    st.markdown("""
    <div class="neural-header">
        <div class="neural-title">RASSIM OS</div>
        <p style="color:#00ffff;">69 ولاية • الملكية: الطاهر الطاهري 👑</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_wilaya_counter()
    
    users, ads, visitors, views = get_stats()
    cols = st.columns(4)
    for i, (val, label) in enumerate(zip([users, ads, visitors, views], ["مستخدم", "إعلان", "زيارة", "مشاهدة"])):
        with cols[i]:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{val}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)
    
    with st.expander("📍 الولايات (69)"):
        show_wilaya_badges()
    
    tab1, tab2 = st.tabs(["🔑 دخول", "📝 حساب جديد"])
    
    with tab1:
        with st.form("login"):
            u = st.text_input("المستخدم")
            p = st.text_input("كلمة المرور", type="password")
            if st.form_submit_button("دخول", use_container_width=True):
                if u and p:
                    user = conn.execute("SELECT password, salt, role, verified FROM users WHERE username=?", (u,)).fetchone()
                    if user and user[0] == hash_password(p, user[1]):
                        st.session_state.user = u
                        st.session_state.role = user[2]
                        st.session_state.verified = user[3]
                        st.success(f"أهلاً {u}")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("خطأ في البيانات")
    
    with tab2:
        with st.form("register"):
            u = st.text_input("المستخدم الجديد")
            p = st.text_input("كلمة المرور", type="password")
            e = st.text_input("البريد")
            ph = st.text_input("الهاتف")
            if st.form_submit_button("تسجيل", use_container_width=True):
                if u and p:
                    salt = secrets.token_hex(16)
                    hashed = hash_password(p, salt)
                    try:
                        conn.execute("INSERT INTO users VALUES (?,?,?,?,?,'user',0,0,0,NULL,CURRENT_TIMESTAMP)", 
                                   (u, hashed, salt, e, ph))
                        conn.commit()
                        st.success("تم التسجيل!")
                    except:
                        st.error("المستخدم موجود")

# ==========================================
# 18. صفحة السوق الذكي
# ==========================================
def show_market():
    st.markdown("### 🛍️ السوق الذكي")
    
    q, w, s = quantum_search_ui()
    
    with st.expander("📊 تحليلات"):
        show_market_trends(conn)
    
    ads = [
        {"id": 1, "title": "iPhone 15 Pro Max 512GB", "price": 225000, "phone": "0555123456", 
         "wilaya": "16 - الجزائر", "description": "نظيف جداً، مع كامل أغراضه، بطارية 100%", "views": 1024, "verified": True},
        {"id": 2, "title": "Samsung S24 Ultra 512GB", "price": 185000, "phone": "0666123456", 
         "wilaya": "31 - وهران", "description": "ممتاز، بطارية 100%، مع قلم S Pen", "views": 856, "verified": True},
        {"id": 3, "title": "Xiaomi 14 Pro 256GB", "price": 95000, "phone": "0777123456", 
         "wilaya": "25 - قسنطينة", "description": "جديد لم يستعمل، ضمان 6 أشهر", "views": 623, "verified": False},
        {"id": 4, "title": "Google Pixel 8 Pro", "price": 165000, "phone": "0555987654", 
         "wilaya": "42 - تيبازة", "description": "مستعمل شهرين، مع جراب أصلي", "views": 421, "verified": True},
        {"id": 5, "title": "iPhone 14 Pro Max", "price": 155000, "phone": "0666987654", 
         "wilaya": "16 - الجزائر", "description": "ممتاز، بطارية 92%، مع الأكسسوارات", "views": 789, "verified": False}
    ]
    
    filtered = ads
    if w and w != "الكل":
        filtered = [a for a in filtered if a['wilaya'] == w]
    if q:
        filtered = [a for a in filtered if q.lower() in a['title'].lower()]
    
    for ad in filtered:
        render_ad_pro(ad)
    
    if not filtered:
        st.info("لا توجد إعلانات")

# ==========================================
# 19. إضافة إعلان
# ==========================================
def post_ad():
    st.markdown("### 📢 إعلان جديد")
    
    with st.form("new_ad"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("المنتج *")
            cat = st.selectbox("الفئة", ["سامسونج", "آيفون", "هواوي", "شاومي", "أخرى"])
        with col2:
            price = st.number_input("السعر *", min_value=0, step=1000)
            wilaya = st.selectbox("الولاية *", ALGERIAN_WILAYAS[1:])
        
        phone = st.text_input("رقم الهاتف *")
        desc = st.text_area("الوصف")
        
        if st.form_submit_button("نشر", use_container_width=True):
            if title and phone and price > 0:
                try:
                    conn.execute("INSERT INTO ads (title,price,phone,wilaya,description,category,owner) VALUES (?,?,?,?,?,?,?)",
                               (title, price, phone, wilaya, desc, cat, st.session_state.user))
                    conn.commit()
                    st.success("تم النشر!")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"خطأ: {e}")

# ==========================================
# 20. الحساب الشخصي
# ==========================================
def profile_page():
    st.markdown("### 👤 حسابي")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="hologram-card">
            <h4 style="color:#00ffff;">المعلومات</h4>
            <p><b>المستخدم:</b> {st.session_state.user}</p>
            <p><b>الصلاحية:</b> {'مسؤول' if st.session_state.role=='admin' else 'عضو'}</p>
            <p><b>التوثيق:</b> {'✅' if st.session_state.verified else '⏳'}</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 21. لوحة الإدارة
# ==========================================
def admin_dashboard():
    st.markdown('<div style="background: #00ffff20; padding:20px; border-radius:30px;"><h1 style="color:white;">🔐 لوحة القيادة</h1><p style="color:#00ffff;">خاص بالطاهر الطاهري</p></div>', unsafe_allow_html=True)
    
    users, ads, visitors, views = get_stats()
    cols = st.columns(4)
    for i, (val, label) in enumerate(zip([users, ads, visitors, views], ["مستخدم", "إعلان", "زيارة", "مشاهدة"])):
        with cols[i]:
            st.metric(label, val)
    
    st.markdown("### 🚨 التنبيهات")
    if st.session_state.last_alert:
        st.warning(f"🔥 {st.session_state.last_alert['message']} - {st.session_state.last_alert['price']} دج")
        st.markdown("[📞 واتساب](https://wa.me/213555555555)")
    else:
        st.info("لا توجد تنبيهات")

# ==========================================
# 22. المحرك الرئيسي
# ==========================================
def main():
    set_ultimate_theme()
    log_visitor()
    show_live_chat()
    robotic_alert_ui()

    if st.session_state.user is None:
        login_page(conn)
    else:
        with st.sidebar:
            st.markdown(f'<div style="background:#00ffff20; padding:20px; border-radius:20px; text-align:center;"><h3>{st.session_state.user}</h3><p style="color:#00ffff;">المالك: الطاهر الطاهري</p></div>', unsafe_allow_html=True)
            page = st.radio("", ["🛍️ السوق", "📢 إعلان", "👤 حسابي", "🔐 الإدارة"])
            
            if st.button("🚪 خروج", use_container_width=True):
                st.session_state.user = None
                st.session_state.admin_access = False
                st.rerun()
        
        if page == "🛍️ السوق":
            show_market()
        elif page == "📢 إعلان":
            post_ad()
        elif page == "👤 حسابي":
            profile_page()
        elif page == "🔐 الإدارة" and st.session_state.role == "admin":
            admin_dashboard()
        else:
            st.error("🔒 غير مصرح")

# ==========================================
# 23. التشغيل
# ==========================================
if __name__ == "__main__":
    main()


