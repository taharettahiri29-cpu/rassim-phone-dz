import streamlit as st
import sqlite3
import hashlib
import secrets
import time
import os
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS • 69 ولاية",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# 2. قائمة الولايات
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
# 3. المتغيرات في الجلسة
# ==========================================
if 'user' not in st.session_state:
    st.session_state.user = None
if 'role' not in st.session_state:
    st.session_state.role = "user"
if 'ip' not in st.session_state:
    st.session_state.ip = secrets.token_hex(8)

# ==========================================
# 4. قاعدة البيانات (نسخة جديدة)
# ==========================================
DB = "rassim_os.db"

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
    
    # جدول الإعلانات - 9 أعمدة محددة
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

init_db()

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

# ==========================================
# 7. إضافة إعلانات تلقائية (النسخة المصححة)
# ==========================================
def seed_smart_ads():
    """إدخال إعلانات احترافية تلقائياً لملء الموقع"""
    
    fake_ads = [
        ("iPhone 15 Pro Max", 225000, "0555112233", "16 - الجزائر", "نظيف جداً 10/10 مع شاحن أصلي، بطارية 100%", "آيفون"),
        ("iPhone 15 Pro", 195000, "0555112244", "31 - وهران", "مستعمل شهرين فقط، مع كامل الأكسسوارات، لون أزرق", "آيفون"),
        ("Samsung S24 Ultra", 185000, "0666445566", "31 - وهران", "مستعمل شهر واحد فقط، ضمان سنة، مع قلم S Pen", "سامسونج"),
        ("Samsung S23 Ultra", 145000, "0666445577", "16 - الجزائر", "حالة ممتازة، بطارية 98%، مع شاحن سريع", "سامسونج"),
        ("Google Pixel 8 Pro", 165000, "0777889900", "42 - تيبازة", "نسخة أمريكية، مفتوح على كل الشبكات، بطارية 98%", "جوجل"),
        ("Xiaomi 14 Pro", 98000, "0544332211", "25 - قسنطينة", "اللون الأسود، 12GB RAM, 512GB، جديد", "شاومي"),
        ("iPhone 14 Pro Max", 155000, "0555112277", "06 - بجاية", "بطارية 92%، كل شيء أصلي، مع جراب", "آيفون")
    ]
    
    try:
        cursor = conn.cursor()
        count = 0
        for ad in fake_ads:
            # التحقق من وجود الإعلان مسبقاً
            existing = cursor.execute(
                "SELECT id FROM ads WHERE title=? AND phone=?", 
                (ad[0], ad[2])
            ).fetchone()
            
            if not existing:
                # إدراج الإعلان مع 9 أعمدة (title, price, phone, wilaya, description, category, owner, verified)
                cursor.execute("""
                    INSERT INTO ads (title, price, phone, wilaya, description, category, owner, verified)
                    VALUES (?, ?, ?, ?, ?, ?, 'RASSIM_BOT', 1)
                """, ad)
                count += 1
        
        conn.commit()
        return count
    except Exception as e:
        st.error(f"⚠️ خطأ في إضافة الإعلانات: {e}")
        return 0

# ==========================================
# 8. التصميم
# ==========================================
st.markdown("""
<style>
* {
    direction: rtl;
    font-family: 'Segoe UI', Tahoma, sans-serif;
}
.stApp {
    background: #0a0a1a;
    color: white;
}
.logo {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    color: #00ffff;
    padding: 20px;
    text-shadow: 0 0 10px #00ffff;
}
.ad-card {
    background: #1a1a2a;
    border: 1px solid #00ffff;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
}
.ad-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 255, 255, 0.2);
}
.stat-card {
    background: #1a1a2a;
    border: 1px solid #00ffff;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
}
.stat-value {
    font-size: 2rem;
    color: #00ffff;
    font-weight: bold;
}
.wilaya-badge {
    display: inline-block;
    background: #1a1a2a;
    border: 1px solid #00ffff;
    border-radius: 20px;
    padding: 5px 10px;
    margin: 2px;
    color: #00ffff;
    font-size: 0.8rem;
}
.stButton > button {
    background: linear-gradient(90deg, #00ffff, #ff00ff) !important;
    color: black !important;
    font-weight: bold !important;
    border: none !important;
    border-radius: 10px !important;
    width: 100%;
}
.chat-bubble {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #00ffff;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 9999;
}
.live-counter {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background: #1a1a2a;
    border: 1px solid #00ffff;
    padding: 8px 15px;
    border-radius: 50px;
    z-index: 999;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 9. دوال الواجهات
# ==========================================

def show_live_counter():
    users, ads, visitors = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span style="color:#00ffff;">●</span> {visitors} زائر | {ads} إعلان
    </div>
    """, unsafe_allow_html=True)

def show_wilaya_badges():
    cols = st.columns(5)
    for i, wilaya in enumerate(ALGERIAN_WILAYAS[1:11]):
        with cols[i % 5]:
            display_text = wilaya[:8] + "..." if len(wilaya) > 10 else wilaya
            st.markdown(f"<span class='wilaya-badge'>{display_text}</span>", unsafe_allow_html=True)

def render_ad(ad):
    # ad[2] = phone, ad[3] = wilaya, ad[4] = price, ad[5] = description, ad[6] = views
    phone_display = ad[2][:4] + "••••" + ad[2][-4:] if len(ad[2]) > 8 else ad[2]
    
    st.markdown(f"""
    <div class="ad-card">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #00ffff;">📍 {ad[3]}</span>
            <span style="color: #888;">👁️ {ad[6]}</span>
        </div>
        <h3 style="color: #00ffff;">{ad[1][:30]}</h3>
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 15px 0;">
            <span style="color: #ff00ff; font-size: 1.8rem; font-weight: bold;">{ad[4]:,} دج</span>
            <span style="background: rgba(255,0,255,0.1); padding: 5px 15px; border-radius: 50px; color: #ff00ff;">📞 {phone_display}</span>
        </div>
        <p style="color: #aaa;">{ad[5][:80]}...</p>
        <div style="display: flex; gap: 10px; margin-top: 15px;">
            <a href="tel:{ad[2]}" style="flex:1; text-decoration: none;">
                <button style="width:100%; padding:12px; background:#111; border:1px solid #00ffff; border-radius:10px; color:#00ffff; font-weight:bold; cursor:pointer;">📞 اتصال</button>
            </a>
            <a href="https://wa.me/{ad[2]}" style="flex:1; text-decoration: none;">
                <button style="width:100%; padding:12px; background:#25D366; border:none; border-radius:10px; color:white; font-weight:bold; cursor:pointer;">📱 واتساب</button>
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
    st.markdown('<div class="logo">RASSIM OS</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;">69 ولاية جزائرية</p>', unsafe_allow_html=True)
    
    users, ads, visitors = get_stats()
    cols = st.columns(3)
    for i, (val, label) in enumerate(zip([users, ads, visitors], ["مستخدم", "إعلان", "زيارة"])):
        with cols[i]:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{val}</div><div>{label}</div></div>', unsafe_allow_html=True)
    
    with st.expander("📍 الولايات المدعومة"):
        show_wilaya_badges()
    
    tab1, tab2 = st.tabs(["🔑 دخول", "📝 تسجيل"])
    
    with tab1:
        with st.form("login"):
            u = st.text_input("اسم المستخدم")
            p = st.text_input("كلمة المرور", type="password")
            if st.form_submit_button("دخول", use_container_width=True) and u and p:
                if u == "admin" and p == "admin":
                    st.session_state.user = u
                    st.session_state.role = "admin"
                    st.success("تم الدخول بنجاح!")
                    time.sleep(1)
                    st.rerun()
                else:
                    user = conn.execute("SELECT password, salt, role FROM users WHERE username=?", (u,)).fetchone()
                    if user and user[0] == hash_password(p, user[1]):
                        st.session_state.user = u
                        st.session_state.role = user[2]
                        st.success("تم الدخول بنجاح!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
    
    with tab2:
        with st.form("register"):
            nu = st.text_input("اسم مستخدم جديد")
            np = st.text_input("كلمة المرور", type="password")
            if st.form_submit_button("تسجيل", use_container_width=True) and nu and np:
                if len(np) >= 6:
                    salt = secrets.token_hex(16)
                    hashed = hash_password(np, salt)
                    try:
                        conn.execute("INSERT INTO users (username, password, salt, role) VALUES (?,?,?,'user')", (nu, hashed, salt))
                        conn.commit()
                        st.success("تم التسجيل بنجاح!")
                    except:
                        st.error("اسم المستخدم موجود مسبقاً")
                else:
                    st.error("كلمة المرور قصيرة (6 أحرف على الأقل)")

def show_market():
    st.markdown("### 🛍️ السوق الذكي")
    
    col1, col2 = st.columns([3,1])
    with col1:
        search = st.text_input("", placeholder="🔍 ابحث عن هاتف...")
    with col2:
        wilaya = st.selectbox("", ["الكل"] + [w for w in ALGERIAN_WILAYAS[1:6]], label_visibility="collapsed")
    
    # بناء الاستعلام
    query = "SELECT * FROM ads WHERE status='active'"
    params = []
    
    if wilaya and wilaya != "الكل":
        query += " AND wilaya LIKE ?"
        params.append(f"%{wilaya}%")
    if search:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.append(f"%{search}%")
        params.append(f"%{search}%")
    
    query += " ORDER BY date DESC LIMIT 20"
    
    ads = conn.execute(query, params).fetchall()
    
    if ads:
        for ad in ads:
            render_ad(ad)
    else:
        st.info("لا توجد إعلانات حالياً")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 إضافة إعلانات تلقائية"):
                count = seed_smart_ads()
                if count > 0:
                    st.success(f"✅ تمت إضافة {count} إعلان!")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.warning("تمت إضافة الإعلانات مسبقاً")
        with col2:
            if st.button("🔄 إعادة تشغيل التطبيق"):
                st.rerun()

def post_ad():
    st.markdown("### 📢 إعلان جديد")
    
    with st.form("new_ad"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("اسم المنتج *")
            cat = st.selectbox("الفئة", ["آيفون", "سامسونج", "هواوي", "شاومي", "أخرى"])
        with col2:
            price = st.number_input("السعر *", min_value=0, step=1000)
            wilaya = st.selectbox("الولاية *", ALGERIAN_WILAYAS[1:])
        
        phone = st.text_input("رقم الهاتف *")
        desc = st.text_area("الوصف")
        
        if st.form_submit_button("نشر", use_container_width=True) and title and phone and price > 0:
            try:
                conn.execute("""
                    INSERT INTO ads (title, price, phone, wilaya, description, category, owner, verified)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 1)
                """, (title, price, phone, wilaya, desc, cat, st.session_state.user))
                conn.commit()
                st.success("✅ تم نشر إعلانك بنجاح!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"خطأ: {e}")

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
        <div class="ad-card">
            <h4 style="color:#00ffff;">معلومات الحساب</h4>
            <p><b>المستخدم:</b> {st.session_state.user}</p>
            <p><b>الصلاحية:</b> {'مسؤول' if st.session_state.role == 'admin' else 'عضو'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="ad-card">
            <h4 style="color:#ff00ff;">إحصائياتي</h4>
            <p><b>إعلاناتي:</b> {user_ads}</p>
            <p><b>مشاهدات:</b> {user_views}</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 10. الصفحة الرئيسية
# ==========================================
def main():
    log_visitor()
    show_live_counter()
    
    # فقاعة الدردشة
    st.markdown("""
    <div class="chat-bubble" onclick="window.open('https://wa.me/213555555555')">
        <img src="https://img.icons8.com/ios-filled/30/ffffff/speech-bubble.png" width="25">
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.user:
        with st.sidebar:
            st.markdown(f"### أهلاً {st.session_state.user}")
            choice = st.radio("القائمة", ["السوق", "إعلان جديد", "حسابي", "خروج"])
            
            if choice == "خروج":
                st.session_state.user = None
                st.rerun()
        
        if choice == "السوق":
            show_market()
        elif choice == "إعلان جديد":
            post_ad()
        elif choice == "حسابي":
            profile_page()
    else:
        login_page()

# ==========================================
# 11. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()
