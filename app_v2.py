import streamlit as st
import sqlite3
import hashlib
import secrets
import time
import os
import base64
import random
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS ULTIMATE • 69 ولاية",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# 2. إنشاء مجلد للصور
# ==========================================
UPLOADS_DIR = "uploads"
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

# ==========================================
# 3. قائمة الولايات
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
# 4. المتغيرات في الجلسة
# ==========================================
if 'user' not in st.session_state:
    st.session_state.user = None
if 'role' not in st.session_state:
    st.session_state.role = "user"
if 'ip' not in st.session_state:
    st.session_state.ip = secrets.token_hex(8)
if 'admin_access' not in st.session_state:
    st.session_state.admin_access = False
if 'last_alert' not in st.session_state:
    st.session_state.last_alert = None

# ==========================================
# 5. قاعدة البيانات
# ==========================================
DB = "rassim_os_ultimate.db"

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)

conn = get_connection()

def init_db():
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
            verified INTEGER DEFAULT 1,
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
            status TEXT DEFAULT 'active',
            owner TEXT NOT NULL,
            verified INTEGER DEFAULT 1,
            date TEXT DEFAULT CURRENT_TIMESTAMP,
            image_path TEXT,
            rating INTEGER DEFAULT 0,
            cpu TEXT,
            ram TEXT,
            camera TEXT,
            capacity TEXT,
            battery TEXT,
            condition TEXT
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

init_db()

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
        conn.execute(
            "INSERT INTO visitors (ip, page) VALUES (?, ?)",
            (st.session_state.ip, 'main')
        )
        conn.commit()
    except:
        pass

def get_stats():
    try:
        users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        ads = conn.execute("SELECT COUNT(*) FROM ads WHERE status='active'").fetchone()[0]
        visitors = conn.execute("SELECT COUNT(*) FROM visitors").fetchone()[0]
        return users, ads, visitors
    except:
        return 0, 0, 0

def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]
        unique_filename = f"{secrets.token_hex(8)}.{file_extension}"
        file_path = os.path.join(UPLOADS_DIR, unique_filename)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None

def get_image_base64(image_path):
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except:
            return None
    return None

def serious_buyer_detector(message, price_offered=0):
    serious_keywords = ["حاب نشري", "نخلصك", "وين نسكنو", "كاش", "آخر سعر", "دابا", "نروحو"]
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

def rassim_robot_logic(user_message):
    user_message = user_message.lower()
    
    responses = {
        "سعر": "💰 الأسعار عندنا هي الأفضل! تفقد الإعلانات وشوف بنفسك",
        "متوفر": "✅ كل الإعلانات المعروضة متوفرة حالياً",
        "تيبازة": "📍 مقرنا في فوكة (42). التوصيل لـ69 ولاية",
        "سلام": "وعليكم السلام! نورت RASSIM OS",
        "آيفون": "📱 آيفون 15 بـ225,000 دج موجود",
        "سامسونج": "📱 S24 Ultra بـ185,000 دج",
        "واد كنيس": "🎯 نحن البديل العصري لواد كنيس",
        "الدزة": "⚡ الدزة الجزائرية واجدة!",
        "وين": "📍 فوكة، تيبازة (42) - نغطي 69 ولاية",
        "69": "✅ 69 ولاية جزائرية مدعومة",
        "كيفاش": "💡 سجل، دوز على الإعلان، وضغط واتساب"
    }
    
    if user_message == "ترحيب_خاص":
        return "🎯 أهلاً بيك في RASSIM OS! راني هنا باش نعاونك"
    
    for key in responses:
        if key in user_message:
            if key in ["حاب نشري", "كاش", "وين"]:
                serious_buyer_detector(user_message)
            return responses[key]
    return "رسالتك وصلت! سأرد قريباً 🌟"

# ==========================================
# 8. الإعلانات التلقائية الذكية
# ==========================================
def get_auto_ads():
    """توليد إعلانات تلقائية ذكية تحاكي السوق الجزائري"""
    phones = [
        {"name": "iPhone 15 Pro Max 512GB", "price": (210000, 240000), 
         "img": "https://images.unsplash.com/photo-1696446701796-da61225697cc?w=400",
         "specs": {"cpu": "A17 Pro", "ram": "8GB", "cam": "48MP", "battery": "4422mAh"}},
        {"name": "Samsung S24 Ultra 512GB", "price": (180000, 205000), 
         "img": "https://images.unsplash.com/photo-1707248545831-7e8c356f981e?w=400",
         "specs": {"cpu": "Snapdragon 8 Gen 3", "ram": "12GB", "cam": "200MP", "battery": "5000mAh"}},
        {"name": "Google Pixel 8 Pro 256GB", "price": (120000, 145000), 
         "img": "https://images.unsplash.com/photo-1696429117066-e399580556f0?w=400",
         "specs": {"cpu": "Tensor G3", "ram": "12GB", "cam": "50MP", "battery": "5050mAh"}},
        {"name": "Xiaomi 14 Ultra 512GB", "price": (140000, 160000), 
         "img": "https://images.unsplash.com/photo-1610433554474-76348234983c?w=400",
         "specs": {"cpu": "Snapdragon 8 Gen 3", "ram": "16GB", "cam": "50MP", "battery": "5300mAh"}},
        {"name": "iPhone 13 Pro Max 256GB", "price": (105000, 125000), 
         "img": "https://images.unsplash.com/photo-1633333008433-89948d3eb300?w=400",
         "specs": {"cpu": "A15 Bionic", "ram": "6GB", "cam": "12MP", "battery": "4352mAh"}},
        {"name": "Samsung S23 Ultra 512GB", "price": (140000, 165000), 
         "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
         "specs": {"cpu": "Snapdragon 8 Gen 2", "ram": "12GB", "cam": "200MP", "battery": "5000mAh"}},
        {"name": "Nothing Phone 2 256GB", "price": (80000, 95000), 
         "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
         "specs": {"cpu": "Snapdragon 8+ Gen 1", "ram": "12GB", "cam": "50MP", "battery": "4700mAh"}},
        {"name": "OnePlus 12 512GB", "price": (120000, 140000), 
         "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
         "specs": {"cpu": "Snapdragon 8 Gen 3", "ram": "16GB", "cam": "50MP", "battery": "5400mAh"}},
        {"name": "Huawei P60 Pro 512GB", "price": (125000, 145000), 
         "img": "https://images.unsplash.com/photo-1678911821544-7a0e6d9b4b8a?w=400",
         "specs": {"cpu": "Snapdragon 8+ Gen 1", "ram": "8GB", "cam": "48MP", "battery": "4815mAh"}},
    ]
    
    wilayas = ["16 - الجزائر", "31 - وهران", "25 - قسنطينة", "42 - تيبازة", "06 - بجاية", "19 - سطيف"]
    sources = ["واد كنيس", "فيسبوك ماركت", "مجموعة RASSIM", "تاجر معتمد", "عرض خاص"]
    tags = ["🔥 عرض حي", "⚡ جديد", "⭐ مميز", "💰 فرصة", "🚀 كمية محدودة"]
    
    auto_data = []
    for i in range(12):
        phone = random.choice(phones)
        price = random.randint(phone["price"][0], phone["price"][1])
        wilaya = random.choice(wilayas)
        
        auto_data.append({
            "id": i,
            "title": phone["name"],
            "price": price,
            "price_formatted": f"{price:,} دج",
            "wilaya": wilaya,
            "img": phone["img"],
            "source": random.choice(sources),
            "tag": random.choice(tags),
            "specs": phone["specs"]
        })
    return auto_data

def seed_auto_ads_to_db():
    """إضافة الإعلانات التلقائية إلى قاعدة البيانات"""
    auto_ads = get_auto_ads()
    cursor = conn.cursor()
    count = 0
    
    for ad in auto_ads:
        # التحقق من وجود الإعلان
        existing = cursor.execute(
            "SELECT id FROM ads WHERE title=? AND price=? AND phone=?", 
            (ad["title"], ad["price"], f"0555{random.randint(1000,9999)}")
        ).fetchone()
        
        if not existing:
            specs = ad["specs"]
            cursor.execute("""
                INSERT INTO ads (
                    title, price, phone, wilaya, description, category, owner,
                    verified, rating, cpu, ram, camera, capacity, battery, condition
                ) VALUES (?, ?, ?, ?, ?, ?, 'RASSIM_BOT', 1, ?, ?, ?, ?, ?, ?)
            """, (
                ad["title"], ad["price"], f"0555{random.randint(1000,9999)}", 
                ad["wilaya"], f"إعلان من {ad['source']} - {ad['tag']}", "أخرى",
                random.choice(["4.8", "4.9", "5.0"]), specs["cpu"], specs["ram"], 
                specs["cam"], f"{random.choice([256,512])}GB", specs["battery"], "ممتاز"
            ))
            count += 1
    
    conn.commit()
    return count

# ==========================================
# 9. التصميم المتطور
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');

* {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl;
    box-sizing: border-box;
}

.stApp {
    background: radial-gradient(circle at 20% 20%, #1a1a2a, #0a0a0f);
    color: #ffffff;
    min-height: 100vh;
}

.logo {
    font-size: 3.5rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00ffff, #ff00ff, #00ffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 20px;
    animation: shine 3s linear infinite;
}

@keyframes shine {
    to { background-position: 200% center; }
}

.hologram-card {
    background: rgba(20, 20, 30, 0.4);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0, 255, 255, 0.2);
    border-radius: 30px;
    padding: 20px;
    margin-bottom: 20px;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}

.hologram-card:hover {
    border-color: #00ffff;
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 255, 255, 0.2);
}

.ad-tag {
    position: absolute;
    top: 10px;
    right: 10px;
    background: linear-gradient(135deg, #ff00ff, #ff0000);
    color: white;
    padding: 4px 12px;
    border-radius: 50px;
    font-size: 0.7rem;
    font-weight: bold;
    z-index: 10;
}

.ad-image {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 20px;
    margin-bottom: 15px;
    border: 1px solid rgba(0, 255, 255, 0.3);
}

.stat-card {
    background: rgba(20, 20, 30, 0.5);
    border: 1px solid #00ffff;
    border-radius: 25px;
    padding: 20px;
    text-align: center;
}

.stat-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #00ffff;
}

.wilaya-badge {
    display: inline-block;
    background: rgba(0, 255, 255, 0.1);
    border: 1px solid #00ffff;
    border-radius: 50px;
    padding: 5px 10px;
    margin: 3px;
    color: #00ffff;
    font-size: 0.8rem;
    white-space: nowrap;
}

.stButton > button {
    background: linear-gradient(90deg, #00ffff, #ff00ff) !important;
    border: none !important;
    color: black !important;
    font-weight: 800 !important;
    border-radius: 15px !important;
    padding: 12px 25px !important;
    transition: all 0.3s ease !important;
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(255, 0, 255, 0.3) !important;
}

.chat-bubble {
    position: fixed;
    bottom: 20px;
    right: 20px;
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
    background: rgba(0, 0, 0, 0.7);
    border: 1px solid #00ffff;
    padding: 10px 20px;
    border-radius: 50px;
    z-index: 999;
    color: white;
    backdrop-filter: blur(5px);
}

.spec-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 5px;
    margin: 10px 0;
    font-size: 0.8rem;
}

.spec-item {
    background: rgba(255, 255, 255, 0.05);
    padding: 5px;
    border-radius: 5px;
    text-align: center;
}

.disclaimer {
    text-align: center;
    font-size: 0.7rem;
    color: #666;
    margin-top: 30px;
    padding: 10px;
    border-top: 1px solid #333;
}

.robot-message {
    background: rgba(255, 0, 255, 0.1);
    border: 1px solid #ff00ff;
    border-radius: 15px;
    padding: 10px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 10. دوال الواجهات
# ==========================================

def show_live_counter():
    users, ads, visitors = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span style="color: #00ffff;">●</span> 
        <b>{visitors}</b> زائر • <b>{ads}</b> إعلان
    </div>
    """, unsafe_allow_html=True)

def show_wilaya_badges():
    cols = st.columns(5)
    for i, wilaya in enumerate(ALGERIAN_WILAYAS[1:11]):
        with cols[i % 5]:
            display_text = wilaya[:8] + "..." if len(wilaya) > 10 else wilaya
            st.markdown(f"<span class='wilaya-badge'>{display_text}</span>", unsafe_allow_html=True)

def show_auto_market():
    """عرض الإعلانات التلقائية في شبكة احترافية"""
    st.markdown("### 🤖 إعلانات محدثة تلقائياً (الآن)")
    
    ads = get_auto_ads()
    
    cols = st.columns(3)
    for i, ad in enumerate(ads):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="hologram-card" style="padding: 15px;">
                <div class="ad-tag">{ad['tag']}</div>
                <img src="{ad['img']}" class="ad-image">
                <h4 style="margin: 10px 0; font-size: 1rem;">{ad['title']}</h4>
                <p style="color: #00ffff; font-weight: bold; font-size: 1.2rem;">{ad['price_formatted']}</p>
                
                <div class="spec-grid">
                    <div class="spec-item">⚡ {ad['specs']['cpu']}</div>
                    <div class="spec-item">🧠 {ad['specs']['ram']}</div>
                    <div class="spec-item">📸 {ad['specs']['cam']}</div>
                    <div class="spec-item">🔋 {ad['specs']['battery']}</div>
                </div>
                
                <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: #888; margin: 10px 0;">
                    <span>📍 {ad['wilaya']}</span>
                    <span>🌐 {ad['source']}</span>
                </div>
                
                <button style="width: 100%; background: transparent; border: 2px solid #ff00ff; color: #ff00ff; border-radius: 10px; padding: 8px; cursor: pointer; font-weight: bold;"
                        onclick="window.open('https://wa.me/213555555555')">
                    📦 تواصل مع البائع
                </button>
            </div>
            """, unsafe_allow_html=True)

def login_page():
    st.markdown('<div class="logo">RASSIM OS ULTIMATE</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#00ffff;">69 ولاية جزائرية • إعلانات تلقائية حية</p>', unsafe_allow_html=True)
    
    users, ads, visitors = get_stats()
    cols = st.columns(3)
    for i, (val, label) in enumerate(zip([users, ads, visitors], ["مستخدم", "إعلان", "زيارة"])):
        with cols[i]:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{val}</div><div>{label}</div></div>', unsafe_allow_html=True)
    
    with st.expander("📍 الولايات المدعومة"):
        show_wilaya_badges()
    
    tab1, tab2 = st.tabs(["🔑 دخول", "📝 تسجيل جديد"])
    
    with tab1:
        with st.form("login"):
            u = st.text_input("👤 اسم المستخدم")
            p = st.text_input("🔐 كلمة المرور", type="password")
            if st.form_submit_button("⚡ دخول", use_container_width=True) and u and p:
                if u == "admin" and p == "admin":
                    st.session_state.user = u
                    st.session_state.role = "admin"
                    st.success("✅ تم الدخول بنجاح!")
                    time.sleep(1)
                    st.rerun()
                else:
                    user = conn.execute("SELECT password, salt, role FROM users WHERE username=?", (u,)).fetchone()
                    if user and user[0] == hash_password(p, user[1]):
                        st.session_state.user = u
                        st.session_state.role = user[2]
                        st.success("✅ تم الدخول بنجاح!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ بيانات غير صحيحة")
    
    with tab2:
        with st.form("register"):
            nu = st.text_input("👤 اسم مستخدم جديد")
            np = st.text_input("🔐 كلمة المرور", type="password")
            if st.form_submit_button("✨ تسجيل", use_container_width=True) and nu and np:
                if len(np) >= 6:
                    salt = secrets.token_hex(16)
                    hashed = hash_password(np, salt)
                    try:
                        conn.execute("INSERT INTO users (username, password, salt, role) VALUES (?,?,?,'user')", (nu, hashed, salt))
                        conn.commit()
                        st.success("✅ تم التسجيل بنجاح!")
                    except:
                        st.error("❌ اسم المستخدم موجود مسبقاً")
                else:
                    st.error("❌ كلمة المرور قصيرة (6 أحرف على الأقل)")

def show_live_chat():
    """فقاعة الدردشة والروبوت"""
    st.markdown("""
    <div class="chat-bubble" onclick="document.getElementById('chat_trigger').click();">
        <img src="https://img.icons8.com/ios-filled/30/ffffff/speech-bubble.png" width="30">
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 💬 روبوت RASSIM")
        
        with st.expander("🗣️ تحدث مع الروبوت", expanded=False):
            st.markdown('<div class="robot-message">أهلاً! أنا روبوت راسم الذكي بالدارجة الجزائرية</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("[![WhatsApp](https://img.icons8.com/color/40/whatsapp.png)](https://wa.me/213555555555)")
            with col2:
                st.markdown("[![Telegram](https://img.icons8.com/color/40/telegram-app.png)](https://t.me/RassimDZ)")
            
            msg = st.text_area("📝 اكتب رسالتك:", key="robot_input", height=80)
            if st.button("🤖 إرسال", use_container_width=True) and msg:
                reply = rassim_robot_logic(msg)
                st.info(f"🤖 {reply}")

def show_market():
    st.markdown("### 🛍️ السوق الذكي")
    
    # الإعلانات التلقائية أولاً
    show_auto_market()
    
    st.markdown("### 📢 إعلانات المستخدمين")
    
    # إعلانات من قاعدة البيانات
    ads = conn.execute("SELECT * FROM ads WHERE status='active' ORDER BY date DESC LIMIT 10").fetchall()
    
    if ads:
        for ad in ads:
            # عرض الإعلانات من قاعدة البيانات
            pass
    else:
        st.info("لا توجد إعلانات من المستخدمين بعد")
        if st.button("🚀 إضافة إعلانات تجريبية", use_container_width=True):
            count = seed_auto_ads_to_db()
            st.success(f"✅ تمت إضافة {count} إعلان")
            st.rerun()

def post_ad():
    st.markdown("### 📢 إعلان جديد")
    
    with st.form("new_ad"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("📱 اسم المنتج *")
            category = st.selectbox("🏷️ الفئة", ["آيفون", "سامسونج", "هواوي", "شاومي", "أخرى"])
        with col2:
            price = st.number_input("💰 السعر (دج) *", min_value=0, step=1000)
            wilaya = st.selectbox("📍 الولاية *", ALGERIAN_WILAYAS[1:])
        
        phone = st.text_input("📞 رقم الهاتف *")
        description = st.text_area("📝 الوصف", height=100)
        
        uploaded_file = st.file_uploader("🖼️ ارفع صورة", type=["png", "jpg", "jpeg"])
        
        if st.form_submit_button("🚀 نشر", use_container_width=True) and title and phone and price > 0:
            image_path = save_uploaded_file(uploaded_file) if uploaded_file else None
            
            try:
                conn.execute("""
                    INSERT INTO ads (title, price, phone, wilaya, description, category, owner, verified, image_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
                """, (title, price, phone, wilaya, description, category, st.session_state.user, image_path))
                conn.commit()
                st.success("✅ تم النشر!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"❌ خطأ: {e}")

def profile_page():
    st.markdown("### 👤 حسابي")
    
    try:
        user_ads = conn.execute("SELECT COUNT(*) FROM ads WHERE owner=?", (st.session_state.user,)).fetchone()[0]
        user_views = conn.execute("SELECT SUM(views) FROM ads WHERE owner=?", (st.session_state.user,)).fetchone()[0] or 0
    except:
        user_ads = 0
        user_views = 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="hologram-card">
            <h4 style="color:#00ffff;">📋 معلومات الحساب</h4>
            <p><b>👤 المستخدم:</b> {st.session_state.user}</p>
            <p><b>🔐 الصلاحية:</b> {'مسؤول' if st.session_state.role == 'admin' else 'عضو'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="hologram-card">
            <h4 style="color:#ff00ff;">📊 إحصائياتي</h4>
            <p><b>📱 إعلاناتي:</b> {user_ads}</p>
            <p><b>👁️ مشاهدات:</b> {user_views}</p>
        </div>
        """, unsafe_allow_html=True)

def admin_dashboard():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00ffff20, #ff00ff20); border: 2px solid #00ffff; border-radius: 30px; padding: 20px; margin-bottom: 20px;">
        <h1 style="color: white; text-align: center;">🔐 لوحة القيادة</h1>
        <p style="color: #00ffff; text-align: center;">خاص بالطاهر الطاهري</p>
    </div>
    """, unsafe_allow_html=True)
    
    users, ads, visitors = get_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("المستخدمين", users)
    with col2:
        st.metric("الإعلانات", ads)
    with col3:
        st.metric("الزيارات", visitors)
    
    if st.button("🚀 إضافة إعلانات تلقائية", use_container_width=True):
        count = seed_auto_ads_to_db()
        st.success(f"✅ تمت إضافة {count} إعلان!")

# ==========================================
# 11. الصفحة الرئيسية النهائية
# ==========================================
def main():
    log_visitor()
    show_live_counter()
    show_live_chat()
    
    st.markdown('<div class="logo">RASSIM OS ULTIMATE</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#00ffff;">69 ولاية • إعلانات تلقائية حية • ذكاء اصطناعي</p>', unsafe_allow_html=True)
    
    if st.session_state.user:
        with st.sidebar:
            st.markdown(f"### ✨ أهلاً {st.session_state.user}")
            choice = st.radio("القائمة", ["🛍️ السوق", "📢 إعلان جديد", "👤 حسابي", "🚪 خروج"])
            
            if st.session_state.role == "admin" and st.button("🔐 الإدارة", use_container_width=True):
                choice = "admin"
            
            if choice == "🚪 خروج":
                st.session_state.user = None
                st.rerun()
        
        if choice == "🛍️ السوق":
            show_market()
        elif choice == "📢 إعلان جديد":
            post_ad()
        elif choice == "👤 حسابي":
            profile_page()
        elif choice == "admin":
            admin_dashboard()
    else:
        login_page()
    
    # إخلاء المسؤولية
    st.markdown("""
    <div class="disclaimer">
        * المحتوى التلقائي يتم تجميعه لأغراض إحصائية وتسهيل البحث، 
        RASSIM OS لا يتحمل مسؤولية دقة الأسعار الخارجية.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 12. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()
