import streamlit as st
import sqlite3
import hashlib
import secrets
import time
import os
import base64
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

# ==========================================
# 5. قاعدة البيانات (نسخة متطورة)
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
    
    # جدول الإعلانات المتطور مع جميع التفاصيل
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
    """حفظ الصورة وإرجاع المسار"""
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]
        unique_filename = f"{secrets.token_hex(8)}.{file_extension}"
        file_path = os.path.join(UPLOADS_DIR, unique_filename)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None

def get_image_base64(image_path):
    """تحويل الصورة إلى base64 لعرضها"""
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except:
            return None
    return None

# ==========================================
# 8. إضافة إعلانات تلقائية مع صور من الإنترنت
# ==========================================
def seed_smart_ads():
    """إدخال إعلانات احترافية مع صور وتفاصيل كاملة"""
    
    fake_ads = [
        # iPhone 15 Pro Max
        ("iPhone 15 Pro Max 512GB", 225000, "0555112233", "16 - الجزائر", 
         "آيفون 15 برو ماكس - Titanium • جديد في الكرتون • مع سماعات AirPods Pro هدية", "آيفون",
         "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-finish-select-202309-6-7inch_AV1_GEO_EMEA?wid=5120&hei=2880&fmt=p-jpg&qlt=80&.v=VW44ZXFyUElCYUxPQzRXYWJZb2RuT2xaMlJrWXVNNnZmS0pidU05c0dQUitDdEVZVU9ER3lZc3oyS0pWdHlMazVxUWNOc0lEbTRxRTcwYVZxT1RTWFVvcXNpSFNLTWpGS3l2c1I3TjhYUUhTc1NlSXZ4dXpjZzFWaFRqTDBhckVTU2Y5TjZLV0F3",
         "5.0", "A17 Pro", "8GB", "48MP + 12MP + 12MP", "512GB", "4422mAh", "جديد"),
        
        # Samsung S24 Ultra
        ("Samsung Galaxy S24 Ultra 512GB", 185000, "0666445566", "31 - وهران",
         "S24 Ultra • Titanium • مع قلم S Pen • شاحن 45W مجاني", "سامسونج",
         "https://images.samsung.com/is/image/samsung/p6pim/ar/2401/gallery/ar-galaxy-s24-s928-490891-sm-s928bztumea-539092387?$650_519_PNG$",
         "4.9", "Snapdragon 8 Gen 3", "12GB", "200MP + 50MP + 12MP", "512GB", "5000mAh", "ممتاز"),
        
        # Google Pixel 8 Pro
        ("Google Pixel 8 Pro 256GB", 165000, "0777889900", "42 - تيبازة",
         "Pixel 8 Pro • Bay Blue • مع شاحن 30W وجراب أصلي", "جوجل",
         "https://lh3.googleusercontent.com/lQ3pK1W1gQqQqQqQqQqQqQqQqQqQqQqQqQqQqQqQqQqQqQqQqQqQqQqQqQqQqQ",
         "4.8", "Google Tensor G3", "12GB", "50MP + 48MP + 48MP", "256GB", "5050mAh", "ممتاز"),
        
        # Xiaomi 14 Pro
        ("Xiaomi 14 Pro 512GB", 98000, "0544332211", "25 - قسنطينة",
         "Xiaomi 14 Pro • الأسود • مع شاحن 120W • ضمان محل 6 أشهر", "شاومي",
         "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E875F0267/pms_1695886052.58613323.png",
         "4.7", "Snapdragon 8 Gen 3", "12GB", "50MP + 50MP + 50MP", "512GB", "4880mAh", "جديد"),
        
        # iPhone 14 Pro Max
        ("iPhone 14 Pro Max 256GB", 155000, "0555112277", "06 - بجاية",
         "آيفون 14 برو ماكس • أرجواني • بطارية 92% • مع جراب MagSafe", "آيفون",
         "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-14-pro-finish-select-202209-6-7inch_GEO_EMEA?wid=5120&hei=2880&fmt=p-jpg&qlt=80&.v=VW44ZXFyUElCYUxPQzRXYWJZb2RuT2xaMlJrWXVNNnZmS0pidU05c0dQUitDdEVZVU9ER3lZc3oyS0pWdHlMazVxUWNOc0lEbTRxRTcwYVZxT1RTWFVvcXNpSFNLTWpGS3l2c1I3TjhYUUhTc1NlSXZ4dXpjZzFWaFRqTDBhckVTU2Y5TjZLV0F3",
         "4.8", "A16 Bionic", "6GB", "48MP + 12MP + 12MP", "256GB", "4323mAh", "ممتاز"),
        
        # Nothing Phone 2
        ("Nothing Phone 2 256GB", 85000, "0999001122", "16 - الجزائر",
         "Nothing Phone 2 • أبيض • تصميم Glyph • بطارية ممتازة", "أخرى",
         "https://www.nothing.tech/cdn/shop/files/Phone-2-White-Back_1400x.png?v=1685522910",
         "4.6", "Snapdragon 8+ Gen 1", "12GB", "50MP + 50MP", "256GB", "4700mAh", "ممتاز"),
        
        # OnePlus 12
        ("OnePlus 12 512GB", 130000, "0999001133", "31 - وهران",
         "OnePlus 12 • أخضر • شاحن 100W • مع جراب أصلي", "أخرى",
         "https://oasis.opstatics.com/content/dam/oasis/page/2023/12/oneplus-12/12r/specs/green-pc.png",
         "4.8", "Snapdragon 8 Gen 3", "16GB", "50MP + 48MP + 64MP", "512GB", "5400mAh", "جديد"),
        
        # Huawei P60 Pro
        ("Huawei P60 Pro 512GB", 135000, "0888991122", "42 - تيبازة",
         "Huawei P60 Pro • لون أرجواني • مع خدمات جوجل • شاحن 88W", "هواوي",
         "https://consumer.huawei.com/content/dam/huawei-cbg-site/common/mkt/pdp/phones/p60-pro/images/pc/p60-pro-kv.png",
         "4.7", "Snapdragon 8+ Gen 1", "8GB", "48MP + 48MP + 13MP", "512GB", "4815mAh", "ممتاز"),
        
        # Samsung Z Fold 5
        ("Samsung Z Fold 5 1TB", 210000, "0666445588", "16 - الجزائر",
         "Z Fold 5 • أسود • مع قلم S Pen Fold Edition • شاحن مجاني", "سامسونج",
         "https://images.samsung.com/is/image/samsung/p6pim/ar/2307/gallery/ar-galaxy-z-fold5-f946-490780-sm-f946bzaeeme-537069731?$650_519_PNG$",
         "4.9", "Snapdragon 8 Gen 2", "12GB", "50MP + 12MP + 10MP", "1TB", "4400mAh", "ممتاز")
    ]
    
    try:
        cursor = conn.cursor()
        count = 0
        for ad in fake_ads:
            # التحقق من وجود الإعلان
            existing = cursor.execute(
                "SELECT id FROM ads WHERE title=? AND phone=?", 
                (ad[0], ad[2])
            ).fetchone()
            
            if not existing:
                # إدراج الإعلان مع جميع التفاصيل
                cursor.execute("""
                    INSERT INTO ads (
                        title, price, phone, wilaya, description, category, owner,
                        verified, rating, cpu, ram, camera, capacity, battery, condition
                    ) VALUES (?, ?, ?, ?, ?, ?, 'RASSIM_BOT', 1, ?, ?, ?, ?, ?, ?)
                """, (
                    ad[0], ad[1], ad[2], ad[3], ad[4], ad[5],
                    ad[7], ad[8], ad[9], ad[10], ad[11], ad[12], ad[13]
                ))
                count += 1
        
        conn.commit()
        return count
    except Exception as e:
        st.error(f"⚠️ خطأ في إضافة الإعلانات: {e}")
        return 0

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

.ad-card {
    background: rgba(20, 20, 30, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0, 255, 255, 0.2);
    border-radius: 30px;
    padding: 20px;
    margin-bottom: 20px;
    transition: all 0.4s ease;
}

.ad-card:hover {
    border-color: #00ffff;
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 255, 255, 0.2);
}

.ad-image {
    width: 100%;
    height: 200px;
    object-fit: contain;
    border-radius: 20px;
    margin-bottom: 15px;
    background: rgba(255, 255, 255, 0.05);
    padding: 10px;
}

.spec-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin: 15px 0;
    padding: 15px 0;
    border-top: 1px solid rgba(255,255,255,0.1);
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.spec-item {
    background: rgba(0, 255, 255, 0.1);
    border: 1px solid #00ffff;
    border-radius: 10px;
    padding: 8px;
    text-align: center;
    font-size: 0.85rem;
    color: #00ffff;
}

.spec-item span {
    color: white;
    display: block;
    font-size: 0.8rem;
    margin-top: 3px;
}

.rating {
    display: inline-block;
    background: #ff00ff;
    color: white;
    padding: 3px 10px;
    border-radius: 50px;
    font-size: 0.8rem;
    margin-right: 10px;
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
        <b>{visitors}</b> زائر | <b>{ads}</b> إعلان
    </div>
    """, unsafe_allow_html=True)

def show_wilaya_badges():
    cols = st.columns(5)
    for i, wilaya in enumerate(ALGERIAN_WILAYAS[1:11]):
        with cols[i % 5]:
            display_text = wilaya[:8] + "..." if len(wilaya) > 10 else wilaya
            st.markdown(f"<span class='wilaya-badge'>{display_text}</span>", unsafe_allow_html=True)

def render_ad(ad):
    """عرض الإعلان مع جميع التفاصيل والصور"""
    
    # ad indices: 
    # 0=id, 1=title, 2=price, 3=phone, 4=wilaya, 5=description, 6=category, 7=views,
    # 8=status, 9=owner, 10=verified, 11=date, 12=image_path, 13=rating, 14=cpu,
    # 15=ram, 16=camera, 17=capacity, 18=battery, 19=condition
    
    phone_display = ad[3][:4] + "••••" + ad[3][-4:] if len(ad[3]) > 8 else ad[3]
    verified_badge = "✅ موثق" if ad[10] == 1 else "⚠️ عادي"
    
    # عرض الصورة
    image_html = ""
    if len(ad) > 12 and ad[12]:
        if ad[12].startswith('http'):
            image_html = f'<img src="{ad[12]}" class="ad-image">'
        else:
            img_base64 = get_image_base64(ad[12])
            if img_base64:
                image_html = f'<img src="data:image/jpeg;base64,{img_base64}" class="ad-image">'
    
    st.markdown(f"""
    <div class="ad-card">
        {image_html}
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <div>
                <span style="color: #00ffff;">📍 {ad[4]}</span>
                <span class="rating">⭐ {ad[13] if len(ad) > 13 else '4.5'}</span>
                <span style="color: #888;">👁️ {ad[7]}</span>
            </div>
            <span style="color: {'#00ffff' if ad[10]==1 else '#ff00ff'};">{verified_badge}</span>
        </div>
        
        <h2 style="color: #00ffff; margin: 10px 0;">{ad[1][:40]}</h2>
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 15px 0;">
            <div style="background: #ff00ff20; padding: 8px 20px; border-radius: 50px;">
                <span style="color: #ff00ff; font-size: 2rem; font-weight: bold;">{ad[2]:,}</span>
                <span style="color: white; font-size: 1rem;">دج</span>
            </div>
            <span style="background: rgba(255,0,255,0.1); padding: 8px 20px; border-radius: 50px; color: #ff00ff;">📞 {phone_display}</span>
        </div>
        
        <p style="color: #aaa; margin: 15px 0;">{ad[5][:100]}...</p>
        
        <div class="spec-grid">
            <div class="spec-item">
                ⚡ CPU<br><span>{ad[14] if len(ad) > 14 else 'A17 Pro'}</span>
            </div>
            <div class="spec-item">
                🧠 RAM<br><span>{ad[15] if len(ad) > 15 else '8GB'}</span>
            </div>
            <div class="spec-item">
                📸 Camera<br><span>{ad[16] if len(ad) > 16 else '48MP'}</span>
            </div>
            <div class="spec-item">
                💾 Storage<br><span>{ad[17] if len(ad) > 17 else '256GB'}</span>
            </div>
            <div class="spec-item">
                🔋 Battery<br><span>{ad[18] if len(ad) > 18 else '4500mAh'}</span>
            </div>
            <div class="spec-item">
                📦 Condition<br><span>{ad[19] if len(ad) > 19 else 'ممتاز'}</span>
            </div>
        </div>
        
        <div style="display: flex; gap: 10px; margin-top: 15px;">
            <a href="tel:{ad[3]}" style="flex: 1; text-decoration: none;">
                <button style="width:100%; padding:15px; background:#111; border:2px solid #00ffff; border-radius:15px; color:#00ffff; font-weight:bold; cursor:pointer;">📞 اتصال فوري</button>
            </a>
            <a href="https://wa.me/{ad[3]}" style="flex: 1; text-decoration: none;">
                <button style="width:100%; padding:15px; background:#25D366; border:none; border-radius:15px; color:white; font-weight:bold; cursor:pointer;">📱 واتساب مباشر</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # تحديث المشاهدات
    try:
        conn.execute("UPDATE ads SET views = views + 1 WHERE id=?", (ad[0],))
        conn.commit()
    except:
        pass

def login_page():
    st.markdown('<div class="logo">RASSIM OS ULTIMATE</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#00ffff;">69 ولاية جزائرية • جميع التفاصيل</p>', unsafe_allow_html=True)
    
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

def show_market():
    st.markdown("### 🛍️ السوق الذكي - جميع المواصفات")
    
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        search = st.text_input("", placeholder="🔍 ابحث عن هاتف...")
    with col2:
        category = st.selectbox("", ["الكل", "آيفون", "سامسونج", "جوجل", "شاومي", "هواوي"], label_visibility="collapsed")
    with col3:
        sort = st.selectbox("", ["الأحدث", "السعر", "التقييم"], label_visibility="collapsed")
    
    col_a, col_b = st.columns(2)
    with col_a:
        wilaya = st.selectbox("الولاية", ["الكل"] + [w for w in ALGERIAN_WILAYAS[1:6]])
    with col_b:
        price_range = st.selectbox("السعر", ["الكل", "أقل من 100ألف", "100-150ألف", "150-200ألف", "أكثر من 200ألف"])
    
    # بناء الاستعلام
    query = "SELECT * FROM ads WHERE status='active'"
    params = []
    
    if wilaya and wilaya != "الكل":
        query += " AND wilaya LIKE ?"
        params.append(f"%{wilaya}%")
    if category and category != "الكل":
        query += " AND category = ?"
        params.append(category)
    if search:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.append(f"%{search}%")
        params.append(f"%{search}%")
    
    if sort == "السعر":
        query += " ORDER BY price"
    elif sort == "التقييم":
        query += " ORDER BY rating DESC"
    else:
        query += " ORDER BY date DESC"
    
    query += " LIMIT 20"
    
    ads = conn.execute(query, params).fetchall()
    
    if ads:
        for ad in ads:
            render_ad(ad)
    else:
        st.info("😕 لا توجد إعلانات حالياً")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 إضافة إعلانات تلقائية", use_container_width=True):
                count = seed_smart_ads()
                if count > 0:
                    st.success(f"✅ تمت إضافة {count} إعلان مع الصور والتفاصيل!")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.warning("الإعلانات موجودة مسبقاً")
        with col2:
            if st.button("🔄 تحديث الصفحة", use_container_width=True):
                st.rerun()

def post_ad():
    st.markdown("### 📢 إعلان جديد - مع الصور والتفاصيل")
    
    with st.form("new_ad", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("📱 اسم المنتج *")
            category = st.selectbox("🏷️ الفئة", ["آيفون", "سامسونج", "هواوي", "شاومي", "جوجل", "أخرى"])
        with col2:
            price = st.number_input("💰 السعر (دج) *", min_value=0, step=1000)
            condition = st.selectbox("📦 الحالة", ["جديد", "ممتاز", "جيد جداً", "مستعمل"])
        
        phone = st.text_input("📞 رقم الهاتف *")
        wilaya = st.selectbox("📍 الولاية *", ALGERIAN_WILAYAS[1:])
        
        # المواصفات
        st.markdown("#### 🔧 المواصفات التقنية")
        col_cpu, col_ram, col_cam = st.columns(3)
        with col_cpu:
            cpu = st.text_input("المعالج (CPU)", placeholder="مثال: A17 Pro")
        with col_ram:
            ram = st.text_input("الذاكرة (RAM)", placeholder="مثال: 8GB")
        with col_cam:
            camera = st.text_input("الكاميرا", placeholder="مثال: 48MP")
        
        col_storage, col_battery, col_rating = st.columns(3)
        with col_storage:
            capacity = st.text_input("السعة", placeholder="مثال: 512GB")
        with col_battery:
            battery = st.text_input("البطارية", placeholder="مثال: 4500mAh")
        with col_rating:
            rating = st.selectbox("التقييم", ["5.0", "4.9", "4.8", "4.7", "4.6", "4.5"])
        
        description = st.text_area("📝 الوصف التفصيلي", height=100)
        
        uploaded_file = st.file_uploader("🖼️ ارفع صورة للهاتف", type=["png", "jpg", "jpeg"])
        
        if st.form_submit_button("🚀 نشر الإعلان", use_container_width=True) and title and phone and price > 0:
            image_path = save_uploaded_file(uploaded_file) if uploaded_file else None
            
            try:
                conn.execute("""
                    INSERT INTO ads (
                        title, price, phone, wilaya, description, category, owner,
                        verified, rating, cpu, ram, camera, capacity, battery, condition
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    title, price, phone, wilaya, description, category, st.session_state.user,
                    rating, cpu or "غير محدد", ram or "غير محدد", 
                    camera or "غير محدد", capacity or "غير محدد", 
                    battery or "غير محدد", condition
                ))
                conn.commit()
                st.success("✅ تم نشر إعلانك بنجاح مع جميع التفاصيل!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"❌ خطأ: {e}")

def profile_page():
    st.markdown("### 👤 حسابي الشخصي")
    
    try:
        user_ads = conn.execute("SELECT COUNT(*) FROM ads WHERE owner=?", (st.session_state.user,)).fetchone()[0]
        user_views = conn.execute("SELECT SUM(views) FROM ads WHERE owner=?", (st.session_state.user,)).fetchone()[0] or 0
    except:
        user_ads = 0
        user_views = 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="ad-card">
            <h4 style="color:#00ffff;">📋 معلومات الحساب</h4>
            <p><b>👤 المستخدم:</b> {st.session_state.user}</p>
            <p><b>🔐 الصلاحية:</b> {'مسؤول' if st.session_state.role == 'admin' else 'عضو'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="ad-card">
            <h4 style="color:#ff00ff;">📊 إحصائياتي</h4>
            <p><b>📱 إعلاناتي:</b> {user_ads}</p>
            <p><b>👁️ مشاهدات:</b> {user_views}</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 11. الصفحة الرئيسية
# ==========================================
def main():
    log_visitor()
    show_live_counter()
    
    # فقاعة الدردشة
    st.markdown("""
    <div class="chat-bubble" onclick="window.open('https://wa.me/213555555555')">
        <img src="https://img.icons8.com/ios-filled/30/ffffff/speech-bubble.png" width="30">
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.user:
        with st.sidebar:
            st.markdown(f"### ✨ أهلاً {st.session_state.user}")
            choice = st.radio("القائمة الرئيسية", ["🛍️ السوق", "📢 إعلان جديد", "👤 حسابي", "🚪 خروج"])
            
            if choice == "🚪 خروج":
                st.session_state.user = None
                st.rerun()
        
        if choice == "🛍️ السوق":
            show_market()
        elif choice == "📢 إعلان جديد":
            post_ad()
        elif choice == "👤 حسابي":
            profile_page()
    else:
        login_page()

# ==========================================
# 12. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()
