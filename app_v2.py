import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import re
import datetime
import urllib.parse
import secrets
import os
import time

# ==========================================
# 1. إعدادات النظام العليا (2026)
# ==========================================
st.set_page_config(page_title="RASSIM DZ TITANIUM V2", layout="wide", page_icon="🇩🇿")
DB = "rassim_titanium_v2.db"

# تصميم CSS لرفع مستوى الواجهة (Algerian Excellence)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .titan-header {
        background: linear-gradient(135deg, #006633 0%, #006633 45%, #d21034 50%, #ffffff 55%, #ffffff 100%);
        padding: 40px; border-radius: 20px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border-bottom: 6px solid #d21034; margin-bottom: 25px;
    }
    .price-badge { background: #d21034; color: white; padding: 5px 15px; border-radius: 10px; font-weight: 900; }
    .ad-card { 
        background: white; border-radius: 15px; padding: 20px; 
        border-right: 10px solid #006633; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. محرك البيانات المطور (Database Engine)
# ==========================================
@st.cache_resource
def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, 
            password TEXT, salt TEXT, role TEXT DEFAULT 'user', 
            last_login TEXT, banned INTEGER DEFAULT 0, ad_count INTEGER DEFAULT 0);
        
        CREATE TABLE IF NOT EXISTS ads(
            id INTEGER PRIMARY KEY AUTOINCREMENT, product TEXT, price INTEGER, 
            phone TEXT, wilaya TEXT, description TEXT, date TEXT, 
            owner TEXT, views INTEGER DEFAULT 0, featured INTEGER DEFAULT 0);
            
        CREATE TABLE IF NOT EXISTS ratings(
            id INTEGER PRIMARY KEY AUTOINCREMENT, ad_id INTEGER, rating INTEGER);
            
        CREATE TABLE IF NOT EXISTS login_attempts(
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, attempt_time TEXT);

        CREATE INDEX IF NOT EXISTS idx_ads_price ON ads(price);
        CREATE INDEX IF NOT EXISTS idx_ads_wilaya ON ads(wilaya);
    """)
    conn.commit()

init_db()

# ==========================================
# 3. الأدوات الأمنية (Security)
# ==========================================
def hash_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

def clean_phone(phone):
    return re.sub(r'\D', '', phone)[-9:]

# ==========================================
# 4. بوابة الدخول (Anti-Brute Force Protection)
# ==========================================
if "user" not in st.session_state: st.session_state.user = None

def auth_page():
    st.markdown('<div class="titan-header"><h1 style="color:#d21034; background:white; display:inline-block; padding:10px 30px; border-radius:15px;">🇩🇿 RASSIM DZ TITANIUM</h1></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔐 دخول", "✨ تسجيل جديد"])
    
    conn = get_connection()
    with t1:
        u = st.text_input("اسم المستخدم", key="login_u")
        p = st.text_input("كلمة المرور", type="password", key="login_p")
        if st.button("دخول آمن"):
            # 🛡️ Anti Brute Force
            attempts = conn.execute("""
                SELECT COUNT(*) FROM login_attempts 
                WHERE username=? AND attempt_time > datetime('now','-5 minutes')
            """, (u,)).fetchone()[0]

            if attempts >= 5:
                st.error("🚫 تم حظر الدخول مؤقتاً لمدة 5 دقائق (أكثر من 5 محاولات).")
                return

            data = conn.execute("SELECT password, salt, banned FROM users WHERE username=?", (u,)).fetchone()
            if data and data[0] == hash_password(p, data[1]):
                if data[2]: st.error("🚫 حساب محظور")
                else:
                    st.session_state.user = u
                    conn.execute("UPDATE users SET last_login=datetime('now') WHERE username=?", (u,))
                    conn.commit()
                    st.rerun()
            else:
                conn.execute("INSERT INTO login_attempts(username,attempt_time) VALUES(?,datetime('now'))", (u,))
                conn.commit()
                st.error(f"❌ بيانات خاطئة. محاولة {attempts+1}/5")

    with t2:
        nu = st.text_input("اسم المستخدم")
        np = st.text_input("كلمة السر", type="password")
        if st.button("فتح الحساب"):
            try:
                salt = secrets.token_hex(16)
                conn.execute("INSERT INTO users(username,password,salt) VALUES(?,?,?)", (nu, hash_password(np, salt), salt))
                conn.commit()
                st.success("✅ تم التسجيل!")
            except: st.error("⚠️ الاسم محجوز")

# ==========================================
# 5. لوحة التحكم والتحليلات (Dashboard)
# ==========================================
def dashboard():
    conn = get_connection()
    with st.sidebar:
        st.success(f"👤 {st.session_state.user}")
        if st.button("تسجيل الخروج"):
            st.session_state.user = None
            st.rerun()
        st.divider()
        wilaya_f = st.selectbox("تصفية حسب الولاية", ["الكل"] + [f"{i:02d}" for i in range(1, 59)])

    tab1, tab2, tab3, tab4 = st.tabs(["🔥 السوق", "➕ نشر إعلان", "📊 التحليلات", "👑 الإدارة"])

    # --- 🧠 Smart Score Engine & Market ---
    with tab1:
        search = st.text_input("🔍 ابحث عن هاتفك...")
        
        # استعلام Smart Score Engine
        query = """
            SELECT a.*, IFNULL(AVG(r.rating),0) as avg_r, COUNT(r.rating) as count_r
            FROM ads a LEFT JOIN ratings r ON a.id = r.ad_id 
            GROUP BY a.id 
            ORDER BY 
                a.featured DESC,
                (a.views*0.3 + IFNULL(AVG(r.rating),0)*25) DESC,
                a.id DESC
        """
        ads = conn.execute(query).fetchall()
        df = pd.DataFrame(ads, columns=["id","product","price","phone","wilaya","description","date","owner","views","featured","avg_r","count_r"])
        
        if search: df = df[df["product"].str.contains(search, case=False)]
        if wilaya_f != "الكل": df = df[df["wilaya"] == wilaya_f]

        # --- 📄 Pagination احترافي ---
        items_per_page = 5
        total_pages = max(1, len(df) // items_per_page + (1 if len(df) % items_per_page > 0 else 0))
        page = st.number_input(f"الصفحة (إجمالي {total_pages})", min_value=1, max_value=total_pages, value=1)
        
        start = (page-1) * items_per_page
        end = start + items_per_page
        current_df = df.iloc[start:end]

        for _, ad in current_df.iterrows():
            wa = f"https://wa.me/213{clean_phone(ad['phone'])}"
            st.markdown(f"""
                <div class="ad-card">
                    <div style="display:flex; justify-content:space-between;">
                        <div>
                            <h3 style="margin:0;">{ad['product']} {'⭐' if ad['featured'] else ''}</h3>
                            <p style="color:#666;">📍 {ad['wilaya']} | 📅 {ad['date']} | 👤 {ad['owner']}</p>
                            <p>{ad['description']}</p>
                            <span style="color:#f39c12;">★ {round(ad['avg_r'],1)} ({ad['count_r']})</span> | 
                            <span style="color:#2980b9;">👁️ {ad['views']}</span>
                        </div>
                        <div style="text-align:left;">
                            <div class="price-badge">{ad['price']:,} دج</div>
                            <br><a href="{wa}" target="_blank" style="text-decoration:none; color:#25d366; font-weight:bold;">واتساب 💬</a>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # --- 📢 نشر الإعلان ---
    with tab2:
        with st.form("publish"):
            p1, p2 = st.columns(2)
            name = p1.text_input("اسم الهاتف")
            pr = p2.number_input("السعر", min_value=0)
            ph = p1.text_input("رقم الهاتف")
            wl = p2.selectbox("الولاية", [f"{i:02d}" for i in range(1, 59)])
            ds = st.text_area("الوصف")
            if st.form_submit_button("نشر الآن"):
                if name and ph:
                    conn.execute("INSERT INTO ads(product,price,phone,wilaya,description,date,owner) VALUES(?,?,?,?,?,?,?)",
                                 (name, pr, ph, wl, ds, str(datetime.date.today()), st.session_state.user))
                    conn.commit()
                    st.success("✅ تم النشر")

    # --- 📊 Analytics Pro Upgrade ---
    with tab3:
        st.subheader("📊 إحصائيات المنصة")
        col_a, col_b, col_c = st.columns(3)
        
        top_seller = conn.execute("SELECT owner, COUNT(*) c FROM ads GROUP BY owner ORDER BY c DESC LIMIT 1").fetchone()
        avg_price = conn.execute("SELECT AVG(price) FROM ads").fetchone()[0]
        total_v = conn.execute("SELECT SUM(views) FROM ads").fetchone()[0]

        if top_seller: col_a.metric("أكثر بائع نشاطاً", top_seller[0])
        if avg_price: col_b.metric("متوسط السعر الوطني", f"{int(avg_price):,} دج")
        col_c.metric("إجمالي المشاهدات", f"{total_v if total_v else 0:,}")

    # --- 👑 Admin & 💎 Featured System ---
    with tab4:
        role = conn.execute("SELECT role FROM users WHERE username=?", (st.session_state.user,)).fetchone()[0]
        if role == "admin":
            st.subheader("💎 إدارة تمييز الإعلانات")
            ads_db = pd.read_sql("SELECT id, product, owner, featured FROM ads", conn)
            edited_ads = st.data_editor(ads_db, key="editor")

            if st.button("تحديث الإعلانات المميزة"):
                for _, row in edited_ads.iterrows():
                    conn.execute("UPDATE ads SET featured=? WHERE id=?", (row['featured'], row['id']))
                conn.commit()
                st.success("✅ تم التحديث بنجاح")
        else:
            st.warning("هذه المنطقة للمديرين فقط")

# ==========================================
# الانطلاق
# ==========================================
if st.session_state.user: dashboard()
else: auth_page()
