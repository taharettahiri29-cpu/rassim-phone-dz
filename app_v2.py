import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import secrets
import time
import plotly.graph_objects as go
import warnings
import os
import base64
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
# 2. إنشاء مجلد uploads إذا لم يكن موجوداً
# ==========================================
UPLOADS_DIR = "uploads"
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

# ==========================================
# 3. قائمة الولايات الجزائرية (69 ولاية)
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
    "36 - الطارف", "37 - تندوف", "38 - تيسمسيلت", "39 - الوادي", "40 - خنشلة",
    "41 - سوق أهراس", "42 - تيبازة", "43 - ميلة", "44 - عين الدفلى", "45 - النعامة",
    "46 - عين تموشنت", "47 - غرداية", "48 - غليزان", "49 - تيميمون", "50 - برج باجي مختار",
    "51 - أولاد جلال", "52 - بني عباس", "53 - عين صالح", "54 - عين قزام", "55 - توقرت",
    "56 - جانت", "57 - المغير", "58 - المنيع", "59 - الطيبات", "60 - أولاد سليман",
    "61 - سيدي خالد", "62 - بوسعادة", "63 - عين وسارة", "64 - حاسي بحبح", "65 - عين الملح",
    "66 - سيدي عيسى", "67 - عين الباردة", "68 - عين آزال", "69 - عين الحجر"
]

# ==========================================
# 4. المتغيرات السرية في الجلسة
# ==========================================
if 'admin_access' not in st.session_state:
    st.session_state.admin_access = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'role' not in st.session_state:
    st.session_state.role = "user"
if 'verified' not in st.session_state:
    st.session_state.verified = 1
if 'ip' not in st.session_state:
    st.session_state.ip = secrets.token_hex(8)
if 'robot_active' not in st.session_state:
    st.session_state.robot_active = False
if 'last_alert' not in st.session_state:
    st.session_state.last_alert = None

# ==========================================
# 5. إعدادات قاعدة البيانات مع إضافة حقل الصورة
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
                verified INTEGER DEFAULT 1,
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
                verified INTEGER DEFAULT 1,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # إضافة حقل الصورة (إذا لم يكن موجوداً)
        try:
            cursor.execute("ALTER TABLE ads ADD COLUMN image_path TEXT")
        except:
            pass  # العمود موجود بالفعل
        
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
# 6. دوال التشفير
# ==========================================
def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    ).hex()

# ==========================================
# 7. دوال المساعدة
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
# 8. نظام "الذكاء العصبي" للواجهة
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

    .logo-container {
        text-align: center;
        padding: 20px;
        margin-bottom: 20px;
    }

    .logo-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 5px;
        background: linear-gradient(90deg, #00ffff, #ff00ff, #00ffff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        display: inline-block;
        filter: drop-shadow(0 0 10px rgba(0,255,255,0.3));
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 40px !important;
        justify-content: center;
        direction: rtl !important;
        padding: 10px !important;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: nowrap !important;
    }

    .stTabs [data-baseweb="tab"] p {
        font-size: 1.2rem !important;
        font-weight: bold !important;
        color: white !important;
    }

    [class*="keyboard_ar"], [class*="keyboard"], [class*="translate"] {
        display: none !important;
    }

    body::after {
        content: "";
        display: none !important;
    }

    .stTextInput, .stTextArea {
        margin-bottom: 15px !important;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        color: white !important;
        padding: 12px 20px !important;
        direction: rtl !important;
        text-align: right !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00ffff !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3) !important;
    }

    .stTextInput label, .stTextArea label {
        color: #00ffff !important;
        font-size: 1rem !important;
        margin-bottom: 5px !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #00ffff, #ff00ff) !important;
        border: none !important;
        color: black !important;
        font-weight: 800 !important;
        border-radius: 15px !important;
        padding: 12px 25px !important;
        transition: all 0.3s ease !important;
        font-size: 1.1rem !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(255, 0, 255, 0.3) !important;
    }

    .hologram-card {
        background: rgba(20, 20, 30, 0.4);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 255, 0.1);
        border-radius: 30px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.4s ease;
        direction: rtl;
        text-align: right;
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
        padding: 5px 10px;
        margin: 3px;
        font-size: 0.8rem;
        color: #00ffff;
        white-space: nowrap;
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
        font-size: 2.2rem;
        font-weight: 800;
        color: #00ffff;
        direction: ltr !important;
        font-family: 'Space Grotesk', monospace !important;
    }

    .stat-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1rem;
        margin-top: 5px;
    }

    .chat-bubble {
        position: fixed;
        bottom: 80px;
        right: 30px;
        background: linear-gradient(135deg, #00ffff, #ff00ff);
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 9999;
        animation: float 3s ease-in-out infinite;
        box-shadow: 0 10px 20px rgba(0, 255, 255, 0.3);
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .live-counter {
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: rgba(0, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid #00ffff;
        padding: 10px 20px;
        border-radius: 50px;
        z-index: 999;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: pulseGlow 2s infinite;
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 5px rgba(0, 255, 255, 0.2); }
        50% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.5); }
        100% { box-shadow: 0 0 5px rgba(0, 255, 255, 0.2); }
    }

    .live-dot {
        color: #00ffff;
        font-weight: bold;
        font-size: 1.2rem;
        animation: blink 1s infinite;
    }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    .terms-box {
        background: rgba(20, 20, 30, 0.6);
        border: 1px solid #ff00ff;
        border-radius: 30px;
        padding: 20px;
        margin-top: 20px;
        color: white;
        font-size: 0.9rem;
        line-height: 1.8;
    }

    .terms-box h2 {
        color: #ff00ff;
        text-align: center;
        margin-bottom: 15px;
    }

    .terms-box hr {
        border-color: rgba(255, 0, 255, 0.2);
        margin: 15px 0;
    }

    .footer-note {
        text-align: center;
        font-size: 0.8rem;
        color: #888;
    }

    @media screen and (max-width: 768px) {
        .logo-text { font-size: 2.2rem; }
        .stat-value { font-size: 1.8rem; }
        .chat-bubble { width: 50px; height: 50px; bottom: 70px; right: 15px; }
        .live-counter { left: 15px; padding: 8px 15px; font-size: 0.8rem; }
        .stTabs [data-baseweb="tab-list"] { gap: 20px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 9. عداد الزوار الحي
# ==========================================
def show_live_counter():
    _, _, total_visitors, _ = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span class="live-dot">●</span>
        <span style="color: white; font-family: 'Space Grotesk';">LIVE: <b style="color: #00ffff;">{total_visitors:,}</b></span>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 10. كاشف المشتري الجدي
# ==========================================
def serious_buyer_detector(message, price_offered=0):
    serious_keywords = [
        "حاب نشري", "نخلصك توت سويت", "وين نسكنو", 
        "كاش", "آخر سعر", "دابا", "نروحو نخلصو", "العنوان",
        "واش راك", "الوقتية", "نجي نشوفو"
    ]
    
    message_lower = message.lower() if message else ""
    is_serious = any(word in message_lower for word in serious_keywords)
    
    if is_serious or price_offered > 0:
        st.session_state.last_alert = {
            'message': message,
            'price': price_offered,
            'time': datetime.now().strftime("%H:%M:%S")
        }
        st.toast("🚨 مشتري جدي!", icon="💰")
        return True
    return False

# ==========================================
# 11. روبوت RASSIM الذكي
# ==========================================
def rassim_robot_logic(user_message):
    user_message = user_message.lower()
    
    welcome_message = """
    🎯 يا أهلاً بيك في RASSIM OS ULTIMATE! 🇩🇿 
    
    راني هنا باش نعاونك تبيع ولا تشري تليفونك في 69 ولاية بكل سهولة.
    
    🔥 ميزتي الكبيرة؟ نعرف شكون المشتري "الصح" وشكون اللي جاي "يقصر".
    
    ⚡ أدخل، سجل، وحط إعلانك.. الرادار راهو خدام!
    
    💬 شحال تحب؟ (آيفون، سامسونج، ولا غرسة؟)
    """
    
    responses = {
        "سعر": "💰 الأسعار عندنا هي الأفضل! تفقد الإعلانات وشوف بنفسك",
        "متوفر": "✅ كل الإعلانات المعروضة متوفرة حالياً",
        "تيبازة": "📍 مقرنا في فوكة (42). التوصيل لـ69 ولاية",
        "سلام": "وعليكم السلام! نورت RASSIM OS",
        "آيفون": "📱 آيفون 15 بـ225,000 دج موجود",
        "سامسونج": "📱 S24 Ultra بـ185,000 دج",
        "هواوي": "📱 هواوي P60 Pro موجود",
        "شاومي": "📱 Xiaomi 14 Pro بـ95,000 دج",
        "واد كنيس": "🎯 نحن البديل العصري لواد كنيس",
        "الدزة": "⚡ الدزة الجزائرية واجدة!",
        "وين": "📍 فوكة، تيبازة (42) - نغطي 69 ولاية",
        "69": "✅ 69 ولاية جزائرية مدعومة",
        "كيفاش": "💡 سجل، دوز على الإعلان، وضغط واتساب",
        "توصيل": "📦 التوصيل لكل الولايات"
    }
    
    if user_message == "ترحيب_خاص":
        return welcome_message
    
    for key in responses:
        if key in user_message:
            if key in ["حاب نشري", "كاش", "وين"]:
                serious_buyer_detector(user_message)
            return responses[key]
    return "رسالتك وصلت! سأرد قريباً 🌟"

# ==========================================
# 12. رادار راسم الآلي
# ==========================================
def robotic_alert_ui():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🛰️ رادار RASSIM")
    hunter_mode = st.sidebar.toggle("⚡ وضع الصياد", value=True)
    st.session_state.robot_active = hunter_mode
    
    if hunter_mode:
        st.sidebar.success("🟢 الرادار نشط")
        if st.session_state.last_alert:
            with st.sidebar.expander("🚨 آخر عرض"):
                st.markdown(f"**{st.session_state.last_alert['message']}**\n💰 {st.session_state.last_alert['price']} دج")
                st.markdown("[📞 تواصل](https://wa.me/213555555555)")
    else:
        st.sidebar.warning("🔴 الرادار متوقف")

# ==========================================
# 13. مولد الإعلانات الذكي
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
# 14. عداد وشبكة الولايات
# ==========================================
def show_wilaya_counter():
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <div style="background: linear-gradient(135deg, #00ffff, #ff00ff); border-radius: 60px; padding: 15px 30px; display: inline-block;">
            <span style="color: black; font-size: 2.5rem; font-weight: 900;">69</span>
            <span style="color: black; font-size: 1.2rem; margin-right: 10px;">ولاية جزائرية</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_wilaya_badges():
    sample_wilayas = ALGERIAN_WILAYAS[1:21]
    cols = st.columns(6)
    for i, wilaya in enumerate(sample_wilayas):
        with cols[i % 6]:
            display_text = wilaya if len(wilaya) <= 10 else wilaya[:10] + "..."
            st.markdown(f"<span class='wilaya-badge'>{display_text}</span>", unsafe_allow_html=True)
    
    with st.expander("📍 عرض جميع الولايات (69)"):
        cols = st.columns(5)
        for i, wilaya in enumerate(ALGERIAN_WILAYAS[1:]):
            with cols[i % 5]:
                st.markdown(f"<span class='wilaya-badge'>{wilaya}</span>", unsafe_allow_html=True)

# ==========================================
# 15. نظام الدردشة المباشرة
# ==========================================
def show_live_chat():
    st.markdown("""
    <div class="chat-bubble" onclick="document.getElementById('chat_trigger').click();">
        <img src="https://img.icons8.com/ios-filled/30/ffffff/speech-bubble.png" width="30">
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 💬 الدعم الذكي")
        generate_auto_ads()
        
        with st.expander("🗣️ تحدث مع روبوت RASSIM", expanded=False):
            st.write("أهلاً! أنا روبوت راسم الذكي بالدارجة الجزائرية")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("[![WhatsApp](https://img.icons8.com/color/40/whatsapp.png)](https://wa.me/213555555555)")
            with col2:
                st.markdown("[![Telegram](https://img.icons8.com/color/40/telegram-app.png)](https://t.me/RassimDZ)")
            
            msg = st.text_area("📝 اكتب رسالتك:", key="robot_input", height=80)
            if st.button("🤖 إرسال", use_container_width=True) and msg:
                reply = rassim_robot_logic(msg)
                st.info(f"🤖 {reply}")
                serious_buyer_detector(msg, 0)

# ==========================================
# 16. نظام التحليل التنبئي
# ==========================================
def show_market_trends(conn):
    st.markdown("### 📈 تحليلات السوق")
    try:
        if conn:
            df = pd.read_sql_query("SELECT category, COUNT(*) as count FROM ads WHERE status='active' GROUP BY category", conn)
            if not df.empty:
                fig = go.Figure(go.Bar(
                    x=df['count'],
                    y=df['category'],
                    orientation='h',
                    marker_color='#00ffff',
                    text=df['count'],
                    textposition='auto'
                ))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=250
                )
                st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("جاري تحميل التحليلات...")

# ==========================================
# 17. محرك البحث الذكي
# ==========================================
def quantum_search_ui():
    col1, col2 = st.columns([3, 1])
    with col1:
        q = st.text_input("", placeholder="🔍 ابحث عن هاتف...")
    with col2:
        st.selectbox("", ["⚡ Flash", "🧠 ذكي"], label_visibility="collapsed")
    
    col_a, col_b = st.columns(2)
    with col_a:
        w = st.selectbox("الولاية", ALGERIAN_WILAYAS)
    with col_b:
        s = st.selectbox("الترتيب", ["الأحدث", "السعر", "المشاهدات"])
    return q, w, s

# ==========================================
# 18. دالة الإعلان مع عرض الصور
# ==========================================
def render_ad_pro(ad):
    verified = "✅ موثق" if ad.get('verified') else "⚠️ عادي"
    image_html = ""
    
    # إذا كان هناك مسار للصورة، اعرضها
    if ad.get('image_path') and os.path.exists(ad['image_path']):
        try:
            with open(ad['image_path'], 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
                image_html = f"""
                <div style="width: 100%; height: 200px; overflow: hidden; border-radius: 15px; margin-bottom: 15px; background-color: #0d0d1a; border: 1px solid #00ffff;">
                    <img src="data:image/jpeg;base64,{img_data}" 
                         alt="{ad.get('title', 'صورة الهاتف')}" 
                         style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.95);">
                </div>
                """
        except:
            image_html = ""
    
    st.markdown(f"""
    <div class="hologram-card" style="margin-bottom: 20px;">
        {image_html}
        <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 8px;">
            <span style="color: #00ffff;">📍 {ad.get('wilaya', '')}</span>
            <span style="color: #888;">👁️ {ad.get('views', 0)}</span>
            <span style="color: {'#00ffff' if ad.get('verified') else '#ff00ff'};">{verified}</span>
        </div>
        <h3 style="color: #00ffff; margin: 8px 0;">{ad.get('title', '')[:40]}</h3>
        <div style="font-size: 1.8rem; font-weight: bold; color: #ff00ff; margin: 10px 0;">
            {ad.get('price', 0):,} <span style="font-size: 0.9rem;">دج</span>
        </div>
        <p style="color: #aaa; margin: 10px 0;">{ad.get('description', '')[:80]}...</p>
        <div style="display: flex; gap: 10px;">
            <a href="tel:{ad.get('phone', '')}" style="flex: 1; text-decoration: none;">
                <button style="width:100%; padding:12px; background:#111; border:1px solid #00ffff; border-radius:10px; color:#00ffff; font-weight:bold; cursor:pointer;">📞 اتصال</button>
            </a>
            <a href="https://wa.me/{ad.get('phone', '')}" style="flex: 1; text-decoration: none;">
                <button style="width:100%; padding:12px; background:#25D366; border:none; border-radius:10px; color:white; font-weight:bold; cursor:pointer;">📱 واتساب</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 19. اتفاقية الاستخدام (Terms of Service)
# ==========================================
def show_terms():
    st.markdown("""
    <div class="terms-box hologram-card" style="border-color: #ff00ff;">
        <h2 style="color: #ff00ff; text-align: center;">📜 قانون المنصة (RASSIM OS)</h2>
        <p style="text-align: right;">
        يا أهلاً بيك في RASSIM OS. باش نحافظو على نظافة السوق وثقة المستخدمين، لازم تلتزم بهاد الشروط:
        <br><br>
        ✅ <b>المصداقية:</b> الإعلان لازم يكون حقيقي وصور الهاتف تكون واضحة. الكذب في السلعة "ممنوع" والروبوت تاعنا يفيق بيك.
        <br><br>
        ✅ <b>الاحترام:</b> أي كلام غير لائق في الدردشة أو الوصف يؤدي لحظر الحساب (Ban) نهائياً بلا ما نرجعو لك.
        <br><br>
        ✅ <b>69 ولاية:</b> حنا نغطيو كامل الجزائر، لذا تأكد من اختيار ولايتك الصحيحة باش يوصلك المشتري الجدي اللي قريب ليك.
        <br><br>
        ⚠️ <b>إخلاء مسؤولية:</b> الموقع هو وسيط ذكي يجمع البائع والمشتري. التأكد من سلامة الهاتف والخلص يكون بيناتكم (برّاء للذمة).
        <br><br>
        🚀 <b>التفعيل الفوري:</b> عطيناكم الثقة وفعلنا الحسابات تلقائياً، حافظوا عليها باش تبقاو Verified.
        </p>
        <hr>
        <p class="footer-note">
        برمجة وتطوير: راسم (2026) • فوكة، تيبازة
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 20. صفحة تسجيل الدخول
# ==========================================
def login_page(conn):
    st.markdown("""
    <div class="logo-container">
        <div class="logo-text">RASSIM OS</div>
        <div style="color: #00ffff; letter-spacing: 2px;">ULTIMATE • 69 WILAYAS</div>
    </div>
    """, unsafe_allow_html=True)
    
    show_wilaya_counter()
    
    users, ads, visitors, views = get_stats()
    cols = st.columns(4)
    for i, (val, label) in enumerate(zip([users, ads, visitors, views], ["مستخدم", "إعلان", "زيارة", "مشاهدة"])):
        with cols[i]:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{val:,}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)
    
    with st.expander("📍 الولايات المدعومة (69)"):
        show_wilaya_badges()
    
    tab1, tab2 = st.tabs(["🔑 دخول", "📝 تسجيل فوري"])
    
    with tab1:
        with st.form("login_form"):
            u = st.text_input("👤 اسم المستخدم")
            p = st.text_input("🔐 كلمة المرور", type="password")
            if st.form_submit_button("⚡ دخول", use_container_width=True) and u and p:
                user = conn.execute("SELECT password, salt, role, verified FROM users WHERE username=?", (u,)).fetchone()
                if user and user[0] == hash_password(p, user[1]):
                    st.session_state.user = u
                    st.session_state.role = user[2]
                    st.session_state.verified = user[3]
                    st.success(f"✅ أهلاً {u}")
                    st.rerun()
                else:
                    st.error("❌ بيانات غير صحيحة")
    
    with tab2:
        with st.form("register_form"):
            nu = st.text_input("👤 اسم المستخدم الجديد")
            np = st.text_input("🔐 كلمة المرور", type="password")
            em = st.text_input("📧 البريد الإلكتروني")
            ph = st.text_input("📱 رقم الهاتف")
            if st.form_submit_button("✨ تسجيل", use_container_width=True) and nu and np:
                if len(np) >= 6:
                    salt = secrets.token_hex(16)
                    hashed = hash_password(np, salt)
                    try:
                        conn.execute("INSERT INTO users (username, password, salt, email, phone, role, verified) VALUES (?,?,?,?,?,'user',1)", 
                                   (nu, hashed, salt, em, ph))
                        conn.commit()
                        st.success("✅ تم التسجيل!")
                    except:
                        st.error("❌ اسم المستخدم موجود")
                else:
                    st.error("❌ كلمة المرور قصيرة")

# ==========================================
# 21. صفحة السوق الذكي مع عرض الإعلانات من قاعدة البيانات
# ==========================================
def show_market():
    st.markdown("### 🛍️ السوق الذكي")
    q, w, s = quantum_search_ui()
    
    with st.expander("📊 تحليلات السوق", expanded=False):
        show_market_trends(conn)
    
    # جلب الإعلانات من قاعدة البيانات
    try:
        query = "SELECT * FROM ads WHERE status='active'"
        params = []
        
        if w and w != "الكل":
            query += " AND wilaya=?"
            params.append(w)
        if q:
            query += " AND (title LIKE ? OR description LIKE ?)"
            params.append(f"%{q}%")
            params.append(f"%{q}%")
        
        query += " ORDER BY date DESC LIMIT 20"
        
        ads = conn.execute(query, params).fetchall()
        
        if ads:
            for ad in ads:
                # تحويل الصف إلى قاموس للوصول السهل
                ad_dict = {
                    'id': ad[0],
                    'title': ad[1],
                    'price': ad[2],
                    'phone': ad[3],
                    'wilaya': ad[4],
                    'description': ad[5],
                    'category': ad[6],
                    'views': ad[7],
                    'featured': ad[8],
                    'status': ad[9],
                    'owner': ad[10],
                    'verified': ad[11],
                    'date': ad[12],
                    'image_path': ad[13] if len(ad) > 13 else None
                }
                render_ad_pro(ad_dict)
        else:
            st.info("😕 لا توجد إعلانات")
    except Exception as e:
        st.error(f"خطأ في تحميل الإعلانات: {e}")

# ==========================================
# 22. إضافة إعلان جديد مع رفع الصور
# ==========================================
def post_ad():
    st.markdown("### 📢 إعلان جديد - نشر فوري بالصور")
    
    with st.form("new_ad_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("📱 اسم المنتج *")
            cat = st.selectbox("🏷️ الفئة", ["سامسونج", "آيفون", "هواوي", "شاومي", "جوجل", "أخرى"])
        with col2:
            price = st.number_input("💰 السعر (دج) *", min_value=0, step=1000)
            wilaya = st.selectbox("📍 الولاية *", ALGERIAN_WILAYAS[1:])
        
        phone = st.text_input("📞 رقم الهاتف *", placeholder="مثال: 0555123456")
        desc = st.text_area("📝 الوصف", height=100, placeholder="اكتب وصفاً مفصلاً للمنتج...")
        
        # إضافة حقل رفع الصورة
        uploaded_file = st.file_uploader("🖼️ ارفع صورة للهاتف", type=["png", "jpg", "jpeg", "webp"])
        image_path = None
        
        if uploaded_file is not None:
            # توليد اسم فريد للصورة
            file_extension = uploaded_file.name.split('.')[-1]
            unique_filename = f"{secrets.token_hex(8)}.{file_extension}"
            image_path = os.path.join(UPLOADS_DIR, unique_filename)
            
            # حفظ الصورة
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ تم حفظ الصورة بنجاح")

        if st.form_submit_button("🚀 نشر فوري بالصور", use_container_width=True):
            if title and phone and price > 0:
                try:
                    conn.execute("""
                        INSERT INTO ads (title, price, phone, wilaya, description, category, owner, status, verified, image_path)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 'active', 1, ?)
                    """, (title, price, phone, wilaya, desc, cat, st.session_state.user, image_path))
                    conn.commit()
                    st.success("✅ تم نشر إعلانك فوراً بالصور! سيظهر في كل الولايات")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ خطأ: {e}")
            else:
                st.error("❌ يرجى ملء جميع الحقول المطلوبة")

# ==========================================
# 23. صفحة الحساب الشخصي
# ==========================================
def profile_page():
    st.markdown("### 👤 حسابي الشخصي")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="hologram-card">
            <h4 style="color:#00ffff;">معلومات الحساب</h4>
            <p><b>👤 المستخدم:</b> {st.session_state.user}</p>
            <p><b>🔐 الصلاحية:</b> {'مسؤول' if st.session_state.role == 'admin' else 'عضو'}</p>
            <p><b>✅ الحالة:</b> {'مفعل' if st.session_state.verified else 'غير مفعل'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        try:
            user_ads = conn.execute("SELECT COUNT(*) FROM ads WHERE owner=?", (st.session_state.user,)).fetchone()[0]
            user_views = conn.execute("SELECT SUM(views) FROM ads WHERE owner=?", (st.session_state.user,)).fetchone()[0] or 0
        except:
            user_ads = 0
            user_views = 0
        
        st.markdown(f"""
        <div class="hologram-card">
            <h4 style="color:#ff00ff;">إحصائياتي</h4>
            <p><b>📊 إعلاناتي:</b> {user_ads}</p>
            <p><b>👁️ مشاهدات:</b> {user_views}</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 24. لوحة الإدارة
# ==========================================
def admin_dashboard():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00ffff20, #ff00ff20); border: 2px solid #00ffff; border-radius: 30px; padding: 20px; margin-bottom: 20px;">
        <h1 style="color: white; text-align: center;">🔐 لوحة القيادة</h1>
        <p style="color: #00ffff; text-align: center;">خاص بالطاهر الطاهري</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    st.markdown("### 🚨 تنبيهات الرادار")
    if st.session_state.last_alert:
        st.markdown(f"""
        <div style="background: rgba(255,0,0,0.2); border: 2px solid #ff00ff; border-radius: 15px; padding: 15px;">
            <h4 style="color: #ff00ff;">🔥 مشتري جدي!</h4>
            <p><b>{st.session_state.last_alert['message']}</b></p>
            <p>💰 {st.session_state.last_alert['price']} دج</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 25. الدالة الرئيسية - المحرك النهائي
# ==========================================
def main():
    set_ultimate_theme()
    log_visitor()
    
    show_live_chat()
    show_live_counter()
    
    if st.session_state.user:
        with st.sidebar:
            st.markdown(f"### ✨ أهلاً {st.session_state.user}")
            choice = st.radio("القائمة الرئيسية", ["🛍️ السوق", "📢 نشر", "👤 حسابي", "🚪 خروج"])
            
            robotic_alert_ui()
            
            with st.expander("📜 شروط الاستخدام"):
                show_terms()
            
            if choice == "🚪 خروج":
                st.session_state.user = None
                st.rerun()
        
        if choice == "🛍️ السوق":
            show_market()
        elif choice == "📢 نشر":
            post_ad()
        elif choice == "👤 حسابي":
            profile_page()
        
        if st.session_state.role == "admin" and st.sidebar.button("🔐 الإدارة"):
            admin_dashboard()
    else:
        login_page(conn)

# ==========================================
# 26. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()

