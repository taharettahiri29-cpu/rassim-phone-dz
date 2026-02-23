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
    "46 - عين تموشنت", "47 - غرداية", "48 - غليزان", "49 - تيميمон", "50 - برج باجي مختار",
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
                views INTEGER DEFAULT 0,
                featured INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                owner TEXT NOT NULL,
                verified INTEGER DEFAULT 0,
                date TEXT DEFAULT CURRENT_TIMESTAMP
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
        
        # جدول التنبيهات
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
    """الحصول على اتصال بقاعدة البيانات"""
    return sqlite3.connect(DB, check_same_thread=False)

# تهيئة قاعدة البيانات
conn = init_db()

# ==========================================
# 5. دوال التشفير
# ==========================================
def hash_password(password, salt):
    """تشفير كلمة المرور باستخدام salt"""
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    ).hex()

def verify_password(input_password, stored_hash, salt):
    """التحقق من صحة كلمة المرور"""
    input_hash = hash_password(input_password, salt)
    return input_hash == stored_hash

# ==========================================
# 6. دوال المساعدة
# ==========================================
def log_visitor():
    """تسجيل زائر جديد"""
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
# 7. نظام التخزين المؤقت
# ==========================================
@st.cache_data(ttl=600)
def load_data_optimized():
    """تحميل البيانات مع التخزين المؤقت"""
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
        box-shadow: 0 10px 30px rgba(0, 255, 255, 0.5);
        cursor: pointer;
        z-index: 9999;
        transition: all 0.3s ease;
        animation: float 3s ease-in-out infinite;
    }

    .chat-bubble:hover {
        transform: scale(1.15) rotate(10deg);
        box-shadow: 0 20px 40px rgba(255, 0, 255, 0.6);
    }

    .chat-bubble img {
        width: 35px;
        height: 35px;
        filter: brightness(0) invert(1);
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
        animation: pulse 1s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 20px #ff00ff; }
        50% { box-shadow: 0 0 40px #ff0000; }
    }

    .wilaya-badge {
        display: inline-block;
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid #00ffff;
        border-radius: 50px;
        padding: 5px 15px;
        margin: 3px;
        font-size: 0.8rem;
        color: #00ffff;
        transition: all 0.3s ease;
    }

    .wilaya-badge:hover {
        background: #00ffff;
        color: black;
        transform: scale(1.05);
    }

    .wilaya-counter {
        background: linear-gradient(135deg, #00ffff, #ff00ff);
        border-radius: 60px;
        padding: 20px 40px;
        text-align: center;
        margin: 20px 0;
        animation: glow 2s ease-in-out infinite;
    }

    .wilaya-counter h2 {
        color: black;
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
    }

    .wilaya-counter p {
        color: black;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 5px 0 0 0;
    }

    @media screen and (max-width: 768px) {
        .neural-title { font-size: 2rem; }
        .stat-value { font-size: 1.8rem; }
        .chat-bubble { width: 60px; height: 60px; bottom: 20px; right: 20px; }
        .chat-bubble img { width: 30px; height: 30px; }
        .wilaya-counter h2 { font-size: 2rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 9. كاشف المشتري الجدي
# ==========================================
def serious_buyer_detector(message, price_offered=0):
    serious_keywords = [
        "حاب نشري", "نخلصك توت سويت", "وين نسكنو", 
        "كاش", "آخر سعر", "دابا", "الوقتية", "نروحو نخلصو",
        "باش نجي", "العنوان", "وين مكانكم"
    ]
    
    message_lower = message.lower() if message else ""
    is_serious = any(word in message_lower for word in serious_keywords)
    
    if is_serious or price_offered > 0:
        st.session_state.last_alert = {
            'message': message,
            'price': price_offered,
            'time': datetime.now().strftime("%H:%M:%S")
        }
        
        st.toast("🚨 تنبيه: مشتري جدي في الانتظار!", icon="💰")
        
        st.markdown("""
            <audio autoplay>
                <source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg">
            </audio>
        """, unsafe_allow_html=True)
        return True
    return False

# ==========================================
# 10. روبوت RASSIM الذكي
# ==========================================
def rassim_robot_logic(user_message):
    user_message = user_message.lower()
    
    responses = {
        "سعر": "أسعارنا هي الأفضل في السوق الجزائري 🇩🇿، تفقد قائمة الإعلانات الموثقة!",
        "متوفر": "كل ما تراه في الواجهة 'Live' متوفر حالياً. هل تريد حجز هاتف؟",
        "تيبازة": "مقرنا الرئيسي في فوكة، تيبازة (42). التوصيل متوفر لـ 69 ولاية! 🚚",
        "سلام": "وعليكم السلام! أنا روبوت RASSIM OS، كيف يمكنني مساعدتك في العثور على هاتفك القادم؟",
        "آيفون": "لدينا تشكيلة واسعة من هواتف iPhone Titanium. ابحث عنها في خانة البحث الكمومي 🔮",
        "سامسونج": "S24 Ultra متوفر بذاكرة 512GB، السعر 185,000 دج شامل الضمان ✅",
        "هواوي": "هواتف هواوي متوفرة بكثرة في السوق الجزائري، ابحث عن P60 Pro!",
        "شاومي": "Xiaomi 14 Pro بأفضل سعر 95,000 دج فقط!",
        "واد كنيس": "نحن البديل العصري لواد كنيس، أسرع وأذكى وأكثر أماناً ✨",
        "الدزة": "الدزة الجزائرية واجدة! هذا هو مستقبل التجارة الإلكترونية في بلادنا",
        "شحال": "لأي سؤال عن الأسعار، اكتب اسم الهاتف في البحث الكمومي وسيظهر لك كل شيء",
        "وين": f"مقرنا الرئيسي في فوكة، تيبازة (42). نغطي 69 ولاية جزائرية كاملة! 🇩🇿",
        "كيفاش": "بسيطة! سجل دخول، دوّز على الإعلان اللي حابو، وضغط على 'اتصل بالبائع'",
        "69": "نعم! نحن نغطي 69 ولاية جزائرية كاملة. حتى الولايات الجديدة مشمولة في خدماتنا 🚀",
        "ولايات": "69 ولاية جزائرية مدعومة بالكامل. من تندوف إلى الطارف، كل الولايات موجودة!",
        "توصيل": "التوصيل متوفر لجميع الولايات الـ 69. نتعامل مع شركات توصيل موثوقة في كل ولاية 📦"
    }
    
    for key in responses:
        if key in user_message:
            if key in ["حاب نشري", "كاش", "آخر سعر", "وين"]:
                serious_buyer_detector(user_message)
            return responses[key]
    
    return "رسالتك وصلت لراسم! سأقوم بتحليلها والرد عليك في أقرب وقت. هل تريد رقم الهاتف؟"

# ==========================================
# 11. رادار راسم الآلي
# ==========================================
def robotic_alert_ui():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🛰️ رادار راسم الآلي")
    
    hunter_mode = st.sidebar.toggle("تفعيل وضع الصياد (Hunter Mode)")
    st.session_state.robot_active = hunter_mode
    
    if hunter_mode:
        st.sidebar.success("الروبوت يراقب الصفقات الآن... 🟢")
        
        if st.session_state.last_alert:
            with st.sidebar.expander("🚨 آخر عرض جدي", expanded=True):
                st.markdown(f"""
                <div class="radar-alert">
                    <p>🔥 <b>رسالة:</b> {st.session_state.last_alert['message']}</p>
                    <p>💰 <b>السعر:</b> {st.session_state.last_alert['price']} دج</p>
                    <p>⏰ <b>الوقت:</b> {st.session_state.last_alert['time']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("[📞 تواصل عبر واتساب](https://wa.me/213555555555)")
        
        if st.sidebar.button("🔍 اختبار الرادار"):
            test_msg = "حاب نشري التليفون كاش اليوم في فوكة"
            if serious_buyer_detector(test_msg, 220000):
                st.sidebar.error(f"🔥 عرض جدي: {test_msg}")
    else:
        st.sidebar.warning("الرادار مطفأ 🔴")

# ==========================================
# 12. مولد الإعلانات الذكي
# ==========================================
def generate_auto_ads():
    current_hour = datetime.now().hour
    if 18 <= current_hour <= 22:
        status = "🔥 وقت الذروة! انشر الآن لجلب آلاف المشاهدات."
        color = "#00ffff"
    elif 9 <= current_hour <= 12:
        status = "☀️ وقت الصباح الذهبي، انشر إعلانك الآن!"
        color = "#ff00ff"
    else:
        status = "⏳ وقت هادئ، جهز منشوراتك للظهيرة."
        color = "#888888"
    
    st.sidebar.markdown(f"<p style='color: {color}; font-weight: bold;'>🤖 حالة الروبوت: {status}</p>", unsafe_allow_html=True)
    return status

# ==========================================
# 13. عداد الولايات
# ==========================================
def show_wilaya_counter():
    st.markdown("""
    <div class="wilaya-counter">
        <h2>69</h2>
        <p>ولاية جزائرية مدعومة بالكامل 🇩🇿</p>
    </div>
    """, unsafe_allow_html=True)

def show_wilaya_badges():
    st.markdown("### 📍 الولايات الـ 69")
    
    cols = st.columns(5)
    for i, wilaya in enumerate(ALGERIAN_WILAYAS[1:]):
        col_idx = i % 5
        with cols[col_idx]:
            st.markdown(f"<span class='wilaya-badge'>{wilaya}</span>", unsafe_allow_html=True)

# ==========================================
# 14. نظام الدردشة المباشرة
# ==========================================
def show_live_chat():
    st.markdown("""
    <div class="chat-bubble" onclick="document.getElementById('chat-trigger').click();">
        <img src="https://img.icons8.com/ios-filled/30/000000/speech-bubble.png"/>
    </div>
    <div style="display: none;">
        <button id="chat-trigger" onclick="document.querySelector('[data-testid=\\'stSidebar\\']').classList.toggle('open');">Open Chat</button>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 💬 مركز الدعم الذكي")
        generate_auto_ads()
        
        with st.expander("🗣️ تحدث مع روبوت RASSIM", expanded=True):
            st.write("أهلاً بك في RASSIM OS! أنا روبوت راسم الذكي. كيف يمكنني مساعدتك اليوم؟")
            
            col1, col2 = st.columns(2)
            with col1:
                whatsapp_url = "https://wa.me/213555555555" 
                st.markdown(f"[![WhatsApp](https://img.icons8.com/color/48/whatsapp.png)]({whatsapp_url})")
            with col2:
                telegram_url = "https://t.me/RassimDZ"
                st.markdown(f"[![Telegram](https://img.icons8.com/color/48/telegram-app.png)]({telegram_url})")
            
            st.divider()
            contact_msg = st.text_area("📝 اكتب رسالتك هنا:", key="robot_chat")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🤖 إرسال للروبوت", use_container_width=True):
                    if contact_msg:
                        reply = rassim_robot_logic(contact_msg)
                        st.info(f"🤖 الروبوت: {reply}")
                        st.session_state.last_robot_reply = reply
                        serious_buyer_detector(contact_msg, 0)
                    else:
                        st.warning("اكتب شيئاً أولاً!")
            
            with col_b:
                if st.button("👤 التواصل المباشر", use_container_width=True):
                    st.info("سيتم تحويلك إلى فريق الدعم البشري قريباً")
            
            if 'last_robot_reply' in st.session_state:
                st.success(f"آخر رد: {st.session_state.last_robot_reply}")

# ==========================================
# 15. نظام التحليل التنبئي
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
# 16. محرك البحث الذكي
# ==========================================
def quantum_search_ui():
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search_query = st.text_input("", placeholder="🔍 ابحث عن هاتف (مثلاً: iPhone 15 Pro Max)...")
    with col2:
        st.selectbox("", ["🧠 أفضل سعر", "⚡ الأكثر ثقة"], label_visibility="collapsed")
    with col3:
        if st.button("🔮 Flash Scan", use_container_width=True):
            st.balloons()
    
    col_a, col_b = st.columns(2)
    with col_a:
        wilaya = st.selectbox("الولاية", ALGERIAN_WILAYAS)
    with col_b:
        sort = st.selectbox("الترتيب", ["الأحدث", "السعر", "المشاهدات"])
    
    return search_query, wilaya, sort

# ==========================================
# 17. دالة الإعلان الذهبية
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
            serious_buyer_detector(f"شراء سريع لـ {ad['title']}", ad['price'])
            st.success("تم إرسال طلبك إلى البائع")

# ==========================================
# 18. صفحة تسجيل الدخول (مصححة)
# ==========================================
def login_page(conn):
    """صفحة تسجيل الدخول - نمرر conn كمعامل"""
    st.markdown("""
    <div class="neural-header">
        <div class="neural-title">RASSIM OS ULTIMATE</div>
        <p style="color: #00ffff;">69 ولاية جزائرية • الملكية: الطاهر الطاهري 👑</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_wilaya_counter()
    
    cached_data = load_data_optimized()
    if cached_data:
        users, ads, visitors, views = cached_data['users'], cached_data['ads'], cached_data['visitors'], cached_data['views']
    else:
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
    
    with st.expander("📍 الولايات المدعومة (69 ولاية)", expanded=False):
        show_wilaya_badges()
    
    tab1, tab2 = st.tabs(["🔑 دخول", "📝 حساب جديد"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("👤 اسم المستخدم")
            password = st.text_input("🔐 كلمة المرور", type="password")
            
            if st.form_submit_button("⚡ دخول", use_container_width=True):
                if username and password:
                    # ✅ استخدام conn الذي تم تمريره
                    user_data = conn.execute(
                        "SELECT password, salt, role, verified FROM users WHERE username=?", 
                        (username,)
                    ).fetchone()

                    if user_data:
                        stored_hash, user_salt, role, verified = user_data
                        input_hash = hash_password(password, user_salt)
                        
                        if input_hash == stored_hash:
                            st.session_state.user = username
                            st.session_state.role = role
                            st.session_state.verified = verified
                            st.success(f"✅ تم الدخول بنجاح! أهلاً {username}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ كلمة المرور غير صحيحة")
                    else:
                        st.error("❌ اسم المستخدم غير موجود")
                else:
                    st.warning("⚠️ يرجى ملء جميع الحقول")
    
    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("👤 اسم المستخدم")
            new_pass = st.text_input("🔐 كلمة المرور", type="password")
            email = st.text_input("📧 البريد الإلكتروني")
            phone = st.text_input("📱 رقم الهاتف")
            
            if st.form_submit_button("✨ تسجيل", use_container_width=True):
                if new_user and new_pass:
                    salt = secrets.token_hex(16)
                    hashed = hash_password(new_pass, salt)
                    
                    try:
                        conn.execute("""
                            INSERT INTO users (username, password, salt, email, phone, role, verified)
                            VALUES (?, ?, ?, ?, ?, 'user', 0)
                        """, (new_user, hashed, salt, email, phone))
                        conn.commit()
                        st.success("✅ تم التسجيل بنجاح! يمكنك الدخول الآن")
                    except sqlite3.IntegrityError:
                        st.error("❌ اسم المستخدم موجود مسبقاً")
                    except Exception as e:
                        st.error(f"❌ حدث خطأ: {e}")
                else:
                    st.warning("⚠️ اسم المستخدم وكلمة المرور مطلوبان")

# ==========================================
# 19. صفحة السوق الذكي
# ==========================================
def show_market():
    st.markdown("### 🛍️ السوق الذكي")
    
    search_query, wilaya, sort = quantum_search_ui()
    
    with st.expander("📊 تحليلات السوق", expanded=False):
        show_market_trends(conn)
    
    ads = [
        {"id": 1, "title": "iPhone 15 Pro Max Titanium", "price": 225000, "phone": "0555-XX-XX-XX", 
         "wilaya": "16 - الجزائر", "description": "نظيف جداً، مع كامل أكسسواراته", "views": 1024},
        {"id": 2, "title": "Samsung S24 Ultra", "price": 185000, "phone": "0666-XX-XX-XX", 
         "wilaya": "31 - وهران", "description": "حالة ممتازة، بطارية 100%", "views": 856},
        {"id": 3, "title": "Xiaomi 14 Pro", "price": 95000, "phone": "0777-XX-XX-XX", 
         "wilaya": "25 - قسنطينة", "description": "جديد لم يستعمل", "views": 623}
    ]
    
    for ad in ads:
        render_ad_pro(ad)

# ==========================================
# 20. صفحة إضافة إعلان
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
            wilaya = st.selectbox("📍 الولاية *", ALGERIAN_WILAYAS[1:])
        
        phone = st.text_input("📞 رقم الهاتف *")
        description = st.text_area("📝 الوصف")
        
        if st.form_submit_button("🚀 نشر الإعلان", use_container_width=True):
            if title and phone:
                try:
                    conn.execute("""
                        INSERT INTO ads (title, price, phone, wilaya, description, category, owner)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (title, price, phone, wilaya, description, category, st.session_state.user))
                    conn.commit()
                    st.success("✅ تم نشر الإعلان بنجاح!")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ خطأ: {e}")
            else:
                st.error("❌ يرجى ملء الحقول المطلوبة")

# ==========================================
# 21. لوحة الإدارة السرية
# ==========================================
def admin_dashboard():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00ffff20, #ff00ff20); 
    border: 2px solid #00ffff; border-radius: 30px; padding: 30px; margin-bottom: 30px;">
        <h1 style="text-align: center; color: white;">🔐 لوحة القيادة المركزية</h1>
        <p style="text-align: center; color: #00ffff;">خاص بالطاهر الطاهري فقط 🛡️</p>
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
    
    st.markdown("### 🚨 تنبيهات الرادار")
    if st.session_state.last_alert:
        st.markdown(f"""
        <div class="radar-alert">
            <h3 style="color: #ff00ff;">🔥 مشتري جدي!</h3>
            <p><b>الرسالة:</b> {st.session_state.last_alert['message']}</p>
            <p><b>السعر:</b> {st.session_state.last_alert['price']} دج</p>
            <p><b>الوقت:</b> {st.session_state.last_alert['time']}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("[📞 تواصل عبر واتساب](https://wa.me/213555555555)")
    else:
        st.info("لا توجد تنبيهات جديدة")
    
    st.markdown("### 💬 رسائل الدعم")
    try:
        messages = conn.execute("""
            SELECT sender, message, date FROM messages 
            WHERE receiver='rassim' 
            ORDER BY date DESC LIMIT 20
        """).fetchall()
        
        if messages:
            for msg in messages:
                st.markdown(f"**{msg[0]}**: {msg[1]} *(at {msg[2]})*")
        else:
            st.info("لا توجد رسائل دعم حالياً.")
    except Exception as e:
        st.error(f"خطأ في عرض الرسائل: {e}")

# ==========================================
# 22. المحرك الرئيسي
# ==========================================
def main():
    set_ultimate_theme()
    log_visitor()
    show_live_chat()
    robotic_alert_ui()

    if st.session_state.user is None:
        # ✅ تمرير conn إلى دالة login_page
        login_page(conn)
    else:
        with st.sidebar:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #00ffff20, #ff00ff20); 
            border-radius: 20px; padding: 20px; text-align: center; margin-bottom: 20px;">
                <div style="font-size: 3rem;">👑</div>
                <div style="color: white; font-size: 1.2rem;">{st.session_state.user}</div>
                <div style="color: #00ffff; font-size: 0.9rem;">المالك: الطاهر الطاهري</div>
            </div>
            """, unsafe_allow_html=True)
            
            page = st.radio("القائمة الرئيسية", ["🛍️ السوق", "📢 أضف إعلان", "👤 حسابي", "🔐 الإدارة"])
            
            if st.sidebar.button("🚪 تسجيل الخروج", use_container_width=True):
                st.session_state.user = None
                st.session_state.admin_access = False
                st.rerun()
        
        if page == "🛍️ السوق":
            show_market()
        elif page == "📢 أضف إعلان":
            post_ad()
        elif page == "👤 حسابي":
            st.info("🚀 صفحة الحساب الشخصي قيد التطوير")
        elif page == "🔐 الإدارة":
            if st.session_state.role == "admin":
                admin_dashboard()
            else:
                st.error("عذراً، هذه اللوحة خاصة بالطاهر الطاهري فقط!")

# ==========================================
# 23. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()

