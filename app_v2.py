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
    "36 - الطارف", "37 - تندوف", "38 - تيسمسيلت", "39 - الوادي", "40 - خنشلة",
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
    st.session_state.verified = 1  # مفعل تلقائياً
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
# 7. نظام "الذكاء العصبي" للواجهة مع جميع التصحيحات
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

    /* ===== تصميم الشعار الاحترافي ===== */
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

    /* ===== تصحيح تداخل التبويبات ===== */
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

    /* إخفاء أي نصوص غريبة */
    [class*="keyboard_ar"], [class*="keyboard"], [class*="translate"] {
        display: none !important;
    }

    body::after {
        content: "";
        display: none !important;
    }

    /* تحسين المسافات في حقول الإدخال */
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

    /* عداد الزوار الحي */
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
# 8. عداد الزوار الحي
# ==========================================
def show_live_counter():
    """عرض عداد الزوار الحي في أسفل الصفحة"""
    _, _, total_visitors, _ = get_stats()
    
    st.markdown(f"""
    <div class="live-counter">
        <span class="live-dot">●</span>
        <span style="color: white; font-family: 'Space Grotesk';">
            LIVE: <b style="color: #00ffff; font-size: 1.1rem;">{total_visitors:,}</b>
        </span>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 9. كاشف المشتري الجدي
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
        
        st.toast("🚨 مشتري جدي دخل!", icon="💰")
        st.balloons()
        return True
    return False

# ==========================================
# 10. روبوت RASSIM الذكي بالدارجة
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
        "سعر": "💰 الأسعار عندنا هي الأفضل في السوق! تفقد الإعلانات وشوف بنفسك",
        "متوفر": "✅ كل الإعلانات المعروضة متوفرة حالياً. دوز وشوف اللي يعجبك",
        "تيبازة": "📍 مقرنا في فوكة (42). التوصيل لـ69 ولاية كاملة 🚚",
        "سلام": "وعليكم السلام! نورت RASSIM OS. تحب تعاون؟ 😊",
        "آيفون": "📱 آيفون 15 برو ماكس بـ225,000 دج موجود. حاب تحجز؟",
        "سامسونج": "📱 S24 Ultra بـ185,000 دج شامل الضمان. متوفر في 16 و31",
        "هواوي": "📱 هواوي P60 Pro موجود. سقسقة عليه في البحث",
        "شاومي": "📱 Xiaomi 14 Pro بـ95,000 دج فقط. فرصة ما تعوضش",
        "واد كنيس": "🎯 نحن البديل العصري لواد كنيس. أسرع، أذكى، وأكثر أماناً",
        "الدزة": "⚡ الدزة الجزائرية واجدة! RASSIM OS هو المستقبل",
        "وين": "📍 المقر الرئيسي: فوكة، تيبازة (42). نغطي 69 ولاية كاملة",
        "69": "✅ 69 ولاية جزائرية مدعومة. حتى الولايات الجديدة مشمولة!",
        "كيفاش": "💡 بسيطة! سجل، دوز على الإعلان، وضغط على واتساب مباشر",
        "توصيل": "📦 التوصيل لكل الولايات. نتعامل مع شركات موثوقة",
        "مساعدة": "🤔 اكتب سؤالك وأنا نجاوبك فوراً"
    }
    
    if user_message == "ترحيب_خاص":
        return welcome_message
    
    for key in responses:
        if key in user_message:
            if key in ["حاب نشري", "كاش", "وين", "دابا"]:
                serious_buyer_detector(user_message)
            return responses[key]
    
    return "رسالتك وصلت! أنا روبوت RASSIM. سأرد عليك قريباً. 🌟"

# ==========================================
# 11. رادار راسم الآلي
# ==========================================
def robotic_alert_ui():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🛰️ رادار RASSIM")
    
    hunter_mode = st.sidebar.toggle("⚡ وضع الصياد", value=True)
    st.session_state.robot_active = hunter_mode
    
    if hunter_mode:
        st.sidebar.success("🟢 الرادار نشط - يراقب الصفقات")
        
        if st.session_state.last_alert:
            with st.sidebar.expander("🚨 آخر عرض ساخن", expanded=True):
                st.markdown(f"""
                **الرسالة:** {st.session_state.last_alert['message']}
                **💰 السعر:** {st.session_state.last_alert['price']} دج
                **⏰ الوقت:** {st.session_state.last_alert['time']}
                """)
                st.markdown("[📞 تواصل فوري](https://wa.me/213555555555)")
    else:
        st.sidebar.warning("🔴 الرادار متوقف")

# ==========================================
# 12. مولد الإعلانات الذكي
# ==========================================
def generate_auto_ads():
    hour = datetime.now().hour
    if 18 <= hour <= 22:
        st.sidebar.markdown("<p style='color:#00ffff; font-weight:bold;'>🔥 وقت الذروة! انشر إعلانك الآن</p>", unsafe_allow_html=True)
    elif 9 <= hour <= 12:
        st.sidebar.markdown("<p style='color:#ff00ff; font-weight:bold;'>☀️ وقت الصباح الذهبي</p>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<p style='color:#888;'>⏳ وقت هادئ - جهز إعلاناتك</p>", unsafe_allow_html=True)

# ==========================================
# 13. عداد وشبكة الولايات
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
    cols = st.columns(6)
    for i, wilaya in enumerate(ALGERIAN_WILAYAS[1:21]):  # عرض أول 20 ولاية كعينة
        with cols[i % 6]:
            st.markdown(f"<span class='wilaya-badge'>{wilaya[:10]}...</span>", unsafe_allow_html=True)
    
    with st.expander("📍 عرض جميع الولايات (69)"):
        cols = st.columns(5)
        for i, wilaya in enumerate(ALGERIAN_WILAYAS[1:]):
            with cols[i % 5]:
                st.markdown(f"<span class='wilaya-badge'>{wilaya}</span>", unsafe_allow_html=True)

# ==========================================
# 14. نظام الدردشة المباشرة
# ==========================================
def show_live_chat():
    st.markdown("""
    <div class="chat-bubble" onclick="document.getElementById('chat_trigger').click();">
        <img src="https://img.icons8.com/ios-filled/30/ffffff/speech-bubble.png" width="30">
    </div>
    <div style="display: none;">
        <button id="chat_trigger">Open</button>
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
            if st.button("🤖 إرسال", use_container_width=True):
                if msg:
                    if msg.lower() == "ترحيب_خاص":
                        reply = rassim_robot_logic("ترحيب_خاص")
                    else:
                        reply = rassim_robot_logic(msg)
                    st.info(f"🤖 {reply}")
                    serious_buyer_detector(msg, 0)

# ==========================================
# 15. نظام التحليل التنبئي
# ==========================================
def show_market_trends(conn):
    st.markdown("### 📈 تحليلات السوق")
    try:
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
                height=250,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("جاري تحميل التحليلات...")

# ==========================================
# 16. محرك البحث الذكي المطور
# ==========================================
def quantum_search_ui():
    col1, col2 = st.columns([3, 1])
    with col1:
        q = st.text_input("", placeholder="🔍 ابحث عن هاتف (آيفون، سامسونج...)")
    with col2:
        st.selectbox("", ["⚡ Flash", "🧠 ذكي"], label_visibility="collapsed")
    
    col_a, col_b = st.columns(2)
    with col_a:
        w = st.selectbox("الولاية", ALGERIAN_WILAYAS)
    with col_b:
        s = st.selectbox("الترتيب", ["الأحدث", "السعر", "المشاهدات"])
    return q, w, s

# ==========================================
# 17. دالة الإعلان المختصرة والأنيقة (نسخة ميني)
# ==========================================
def render_ad_pro(ad):
    """عرض الإعلان بشكل مختصر وأنيق"""
    
    phone_display = ad['phone'][:4] + "••••" + ad['phone'][-4:] if len(ad['phone']) > 8 else ad['phone']
    verified = "✅" if ad.get('verified') else "⚠️"
    verified_color = "#00ffff" if ad.get('verified') else "#ff00ff"
    
    st.markdown(f"""
    <div class="hologram-card">
        <div style="display: flex; justify-content: space-between; color: #888; font-size: 0.85rem; margin-bottom: 8px;">
            <span>📍 {ad['wilaya']}</span>
            <span>👁️ {ad['views']}</span>
            <span style="color: {verified_color};">{verified}</span>
        </div>
        
        <h3 style="color: #00ffff; margin: 8px 0; font-size: 1.3rem;">{ad['title'][:30]}</h3>
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 10px 0;">
            <span style="color: #ff00ff; font-size: 1.6rem; font-weight: bold;">{ad['price']:,} دج</span>
            <span style="background: rgba(255,0,255,0.1); padding: 5px 12px; border-radius: 50px; color: #ff00ff; font-size: 0.9rem;">📞 {phone_display}</span>
        </div>
        
        <p style="color: #aaa; margin: 8px 0; font-size: 0.9rem;">{ad['description'][:60]}...</p>
        
        <div style="display: flex; gap: 8px; margin-top: 12px;">
            <a href="https://wa.me/{ad['phone']}" target="_blank" style="flex: 1;">
                <button style="width:100%; padding:10px; background:#25D366; border:none; border-radius:12px; color:white; font-weight:bold; cursor:pointer; font-size:0.9rem;">📱 واتساب</button>
            </a>
            <a href="tel:{ad['phone']}" style="flex: 1;">
                <button style="width:100%; padding:10px; background:linear-gradient(90deg, #00ffff, #ff00ff); border:none; border-radius:12px; color:black; font-weight:bold; cursor:pointer; font-size:0.9rem;">📞 اتصال</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 18. صفحة تسجيل الدخول مع الشعار الجديد
# ==========================================
def login_page(conn):
    st.markdown("""
    <div class="logo-container">
        <div class="logo-text">RASSIM OS</div>
        <div style="color: #00ffff; letter-spacing: 2px; font-size: 0.9rem; margin-top: -5px;">
            ULTIMATE • 69 WILAYAS
        </div>
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
            if st.form_submit_button("⚡ دخول سريع", use_container_width=True):
                if u and p:
                    user = conn.execute("SELECT password, salt, role, verified FROM users WHERE username=?", (u,)).fetchone()
                    if user:
                        if user[0] == hash_password(p, user[1]):
                            st.session_state.user = u
                            st.session_state.role = user[2]
                            st.session_state.verified = user[3]
                            st.success(f"✅ أهلاً {u}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ كلمة المرور غير صحيحة")
                    else:
                        st.error("❌ المستخدم غير موجود")
                else:
                    st.warning("⚠️ املأ جميع الحقول")
    
    with tab2:
        with st.form("register_form"):
            nu = st.text_input("👤 اسم المستخدم الجديد")
            np = st.text_input("🔐 كلمة المرور", type="password")
            em = st.text_input("📧 البريد الإلكتروني")
            ph = st.text_input("📱 رقم الهاتف")
            if st.form_submit_button("✨ تسجيل وتفعيل فوري", use_container_width=True):
                if nu and np:
                    if len(np) < 6:
                        st.error("❌ كلمة المرور قصيرة (6 أحرف على الأقل)")
                    else:
                        salt = secrets.token_hex(16)
                        hashed = hash_password(np, salt)
                        try:
                            conn.execute("""
                                INSERT INTO users (username, password, salt, email, phone, role, verified)
                                VALUES (?, ?, ?, ?, ?, 'user', 1)
                            """, (nu, hashed, salt, em, ph))
                            conn.commit()
                            st.success("✅ تم التسجيل والتفعيل الفوري! يمكنك الدخول الآن")
                            st.balloons()
                        except sqlite3.IntegrityError:
                            st.error("❌ اسم المستخدم موجود مسبقاً")
                else:
                    st.warning("⚠️ اسم المستخدم وكلمة المرور مطلوبان")

# ==========================================
# 19. صفحة السوق الذكي
# ==========================================
def show_market():
    st.markdown("### 🛍️ السوق الذكي")
    
    q, w, s = quantum_search_ui()
    
    with st.expander("📊 تحليلات السوق الحية", expanded=False):
        show_market_trends(conn)
    
    # إعلانات تجريبية (تأتي من قاعدة البيانات في النسخة الحقيقية)
    ads = [
        {"id": 1, "title": "iPhone 15 Pro Max 512GB", "price": 225000, "phone": "0555123456", 
         "wilaya": "16 - الجزائر", "description": "نظيف جداً، مع كامل أغراضه، بطارية 100%، لون أسود، مع سماعات AirPods Pro هدية", "views": 1024, "verified": True},
        {"id": 2, "title": "Samsung S24 Ultra 512GB", "price": 185000, "phone": "0666123456", 
         "wilaya": "31 - وهران", "description": "حالة ممتازة، بطارية 100%، مع قلم S Pen أصلي، شاحن سريع 45W", "views": 856, "verified": True},
        {"id": 3, "title": "Xiaomi 14 Pro 256GB", "price": 95000, "phone": "0777123456", 
         "wilaya": "25 - قسنطينة", "description": "جديد لم يستعمل، مع كامل أغراضه، ضمان محل 6 أشهر", "views": 623, "verified": True},
        {"id": 4, "title": "Google Pixel 8 Pro", "price": 165000, "phone": "0555987654", 
         "wilaya": "42 - تيبازة", "description": "نظيف، مستعمل شهرين فقط، مع جراب أصلي وشاحن", "views": 421, "verified": True},
        {"id": 5, "title": "iPhone 14 Pro Max", "price": 155000, "phone": "0666987654", 
         "wilaya": "16 - الجزائر", "description": "حالة ممتازة، بطارية 92%، مع جميع الأكسسوارات", "views": 789, "verified": False}
    ]
    
    filtered = ads
    if w and w != "الكل":
        filtered = [a for a in filtered if a['wilaya'] == w]
    if q:
        filtered = [a for a in filtered if q.lower() in a['title'].lower()]
    
    for ad in filtered:
        render_ad_pro(ad)
    
    if not filtered:
        st.info("😕 لا توجد إعلانات تطابق بحثك")

# ==========================================
# 20. إضافة إعلان جديد (نشر فوري)
# ==========================================
def post_ad():
    st.markdown("### 📢 إعلان جديد - نشر فوري لـ 69 ولاية")
    
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
        
        if st.form_submit_button("🚀 نشر فوري", use_container_width=True):
            if title and phone and price > 0:
                try:
                    conn.execute("""
                        INSERT INTO ads (title, price, phone, wilaya, description, category, owner, status, verified)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 'active', 1)
                    """, (title, price, phone, wilaya, desc, cat, st.session_state.user))
                    conn.commit()
                    st.success("✅ تم نشر إعلانك فوراً! سيظهر في كل الولايات")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ خطأ: {e}")
            else:
                st.error("❌ يرجى ملء جميع الحقول المطلوبة")

# ==========================================
# 21. صفحة الحساب الشخصي
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
            <p><b>⭐ التقييم:</b> 4.8/5</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # إحصائيات المستخدم
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
            <p><b>📅 عضو منذ:</b> 2026</p>
            <p><b>🏆 الترتيب:</b> برونزي</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 22. لوحة الإدارة السرية
# ==========================================
def admin_dashboard():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00ffff20, #ff00ff20); border: 2px solid #00ffff; border-radius: 30px; padding: 20px; margin-bottom: 20px;">
        <h1 style="color: white; text-align: center;">🔐 لوحة القيادة المركزية</h1>
        <p style="color: #00ffff; text-align: center;">خاص بالطاهر الطاهري فقط 🛡️</p>
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
        <div style="background: rgba(255,0,0,0.2); border: 2px solid #ff00ff; border-radius: 15px; padding: 15px; margin: 10px 0;">
            <h4 style="color: #ff00ff;">🔥 مشتري جدي!</h4>
            <p><b>الرسالة:</b> {st.session_state.last_alert['message']}</p>
            <p><b>💰 السعر:</b> {st.session_state.last_alert['price']} دج</p>
            <p><b>⏰ الوقت:</b> {st.session_state.last_alert['time']}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("[📞 تواصل عبر واتساب](https://wa.me/213555555555)")
    else:
        st.info("لا توجد تنبيهات جديدة")
    
    # عرض آخر المستخدمين
    st.markdown("### 👥 آخر المستخدمين")
    try:
        recent_users = conn.execute("SELECT username, created_at FROM users ORDER BY created_at DESC LIMIT 5").fetchall()
        for u in recent_users:
            st.markdown(f"- **{u[0]}** ⏱️ {u[1][:16]}")
    except:
        pass

# ==========================================
# 23. المحرك الرئيسي (Main Controller)
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
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #00ffff20, #ff00ff20); border-radius: 20px; padding: 20px; text-align: center; margin-bottom: 20px;">
                <div style="font-size: 3rem;">👑</div>
                <div style="color: white; font-size: 1.2rem;">{st.session_state.user}</div>
                <div style="color: #00ffff; font-size: 0.9rem;">المالك: الطاهر الطاهري</div>
            </div>
            """, unsafe_allow_html=True)
            
            page = st.radio("القائمة الرئيسية", ["🛍️ السوق", "📢 إعلان جديد", "👤 حسابي", "🔐 الإدارة"])
            
            if st.button("🚪 تسجيل الخروج", use_container_width=True):
                st.session_state.user = None
                st.session_state.admin_access = False
                st.rerun()
        
        if page == "🛍️ السوق":
            show_market()
        elif page == "📢 إعلان جديد":
            post_ad()
        elif page == "👤 حسابي":
            profile_page()
        elif page == "🔐 الإدارة":
            if st.session_state.role == "admin":
                admin_dashboard()
            else:
                st.error("🔒 هذه اللوحة خاصة بالطاهر الطاهري فقط")

    show_live_counter()

# ==========================================
# 24. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()


