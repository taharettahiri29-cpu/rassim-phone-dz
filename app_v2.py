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
# 1. إعدادات النخبة TITANIUM MAX
# ==========================================
st.set_page_config(page_title="RASSIM DZ TITANIUM MAX", layout="wide", page_icon="🇩🇿")
DB = "rassim_titanium_max_2026.db"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #f0f2f6; }
    .main-header {
        background: linear-gradient(135deg, #006633 0%, #006633 48%, #d21034 50%, #ffffff 52%, #ffffff 100%);
        padding: 50px; border-radius: 30px; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        border-bottom: 10px solid #d21034; margin-bottom: 35px;
    }
    .ad-card { 
        background: white; border-radius: 20px; padding: 30px; 
        border-right: 15px solid #006633; margin-bottom: 25px; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.08); transition: 0.4s ease;
    }
    .ad-card:hover { transform: translateY(-5px); border-right-color: #d21034; }
    .price-tag { background: #d21034; color: white; padding: 10px 25px; border-radius: 15px; font-weight: 900; font-size: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. محرك البيانات الشامل (MAX ENGINE)
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

        CREATE TABLE IF NOT EXISTS visitors(
            id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, visit_date TEXT, last_seen TEXT);

        CREATE TABLE IF NOT EXISTS ad_views(
            id INTEGER PRIMARY KEY AUTOINCREMENT, ad_id INTEGER, view_time TEXT);

        CREATE TABLE IF NOT EXISTS sessions(
            id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, start_time TEXT, 
            last_activity TEXT, duration INTEGER DEFAULT 0);

        CREATE TABLE IF NOT EXISTS clicks(
            id INTEGER PRIMARY KEY AUTOINCREMENT, ad_id INTEGER, click_time TEXT);

        CREATE TABLE IF NOT EXISTS page_views(
            id INTEGER PRIMARY KEY AUTOINCREMENT, page TEXT, view_time TEXT);

        CREATE INDEX IF NOT EXISTS idx_ads_price ON ads(price);
        CREATE INDEX IF NOT EXISTS idx_ads_owner ON ads(owner);
    """)
    conn.commit()

init_db()

# ==========================================
# 3. التحليلات والتتبع (MAX ANALYTICS ENGINE)
# ==========================================
def track_visitor():
    conn = get_connection()
    ip = st.session_state.get("ip")
    if not ip:
        ip = secrets.token_hex(8)
        st.session_state.ip = ip
    today = str(datetime.date.today())
    existing = conn.execute("SELECT id FROM visitors WHERE ip=? AND visit_date=?", (ip, today)).fetchone()
    if not existing:
        conn.execute("INSERT INTO visitors(ip,visit_date,last_seen) VALUES(?,?,datetime('now'))", (ip, today))
    else:
        conn.execute("UPDATE visitors SET last_seen=datetime('now') WHERE ip=?", (ip,))
    conn.commit()

def track_session():
    conn = get_connection()
    ip = st.session_state.ip
    now = datetime.datetime.now()
    s = conn.execute("SELECT id,start_time FROM sessions WHERE ip=? ORDER BY id DESC LIMIT 1", (ip,)).fetchone()
    if not s:
        conn.execute("INSERT INTO sessions(ip,start_time,last_activity) VALUES(?,?,?)", (ip, now, now))
    else:
        start = datetime.datetime.fromisoformat(s[1])
        duration = int((now - start).total_seconds())
        conn.execute("UPDATE sessions SET last_activity=?, duration=? WHERE id=?", (now, duration, s[0]))
    conn.commit()

def hash_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

# ==========================================
# 4. بوابة الدخول المحصنة
# ==========================================
if "user" not in st.session_state: st.session_state.user = None

def auth_page():
    st.markdown('<div class="main-header"><h1 style="color:#d21034; background:white; display:inline-block; padding:15px 50px; border-radius:20px; font-weight:900;">🇩🇿 RASSIM DZ TITANIUM MAX</h1></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔒 دخول النخبة", "✨ انضمام للمنصة"])
    conn = get_connection()
    
    with t1:
        u = st.text_input("المستخدم")
        p = st.text_input("كلمة السر", type="password")
        if st.button("دخول آمن"):
            attempts = conn.execute("SELECT COUNT(*) FROM login_attempts WHERE username=? AND attempt_time > datetime('now','-5 minutes')", (u,)).fetchone()[0]
            if attempts >= 5:
                st.error("🚫 تم حظر الدخول مؤقتاً لمدة 5 دقائق.")
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
                st.error("❌ بيانات خاطئة")

    with t2:
        nu = st.text_input("اسم مستخدم جديد")
        np = st.text_input("كلمة مرور قوية", type="password")
        if st.button("إنشاء حساب"):
            try:
                salt = secrets.token_hex(16)
                conn.execute("INSERT INTO users(username,password,salt) VALUES(?,?,?)", (nu, hash_password(np, salt), salt))
                conn.commit()
                st.success("✅ تم التسجيل!")
            except: st.error("⚠️ الاسم محجوز")

# ==========================================
# 5. المنظومة الذكية (The Dashboard)
# ==========================================
def dashboard():
    track_visitor()
    track_session()
    conn = get_connection()
    
    with st.sidebar:
        st.markdown(f"### 🎖️ {st.session_state.user}")
        online = conn.execute("SELECT COUNT(DISTINCT ip) FROM visitors WHERE last_seen > datetime('now','-5 minutes')").fetchone()[0]
        st.info(f"🟢 الزوار النشطون: {online}")
        if st.button("🚪 تسجيل خروج"):
            st.session_state.user = None
            st.rerun()
        st.divider()
        wilaya_f = st.selectbox("📍 تصفية الولاية", ["الكل"] + [f"{i:02d}" for i in range(1, 59)])

    tab1, tab2, tab3, tab4 = st.tabs(["🔍 السوق الذكي", "📢 نشر إعلان", "📊 Analytics MAX", "🛡️ الإدارة"])

    # --- السوق والترند الذكي ---
    with tab1:
        conn.execute("INSERT INTO page_views(page,view_time) VALUES('market',datetime('now'))")
        conn.commit()
        search = st.text_input("🔎 ابحث عن هاتف، بائع، أو وصف...")
        
        # 🧠 Smart Score Engine (ORDER BY المطور)
        query = """
            SELECT a.*, IFNULL(AVG(r.rating),0) as avg_r, COUNT(r.rating) as count_r
            FROM ads a LEFT JOIN ratings r ON a.id = r.ad_id 
            GROUP BY a.id 
            ORDER BY
                a.featured DESC,
                (a.views*0.4 + IFNULL(AVG(r.rating),0)*30 + (SELECT COUNT(*) FROM clicks c WHERE c.ad_id=a.id)*5) DESC,
                a.id DESC
        """
        ads = conn.execute(query).fetchall()
        df = pd.DataFrame(ads, columns=["id","product","price","phone","wilaya","description","date","owner","views","featured","avg_r","count_r"])
        
        if search: df = df[df["product"].str.contains(search, case=False)]
        if wilaya_f != "الكل": df = df[df["wilaya"] == wilaya_f]

        # 📄 Pagination
        items_per_page = 5
        page = st.number_input("الصفحة", min_value=1, value=1)
        current_df = df.iloc[(page-1)*items_per_page : page*items_per_page]

        for _, ad in current_df.iterrows():
            conn.execute("UPDATE ads SET views = views + 1 WHERE id=?", (ad['id'],))
            conn.execute("INSERT INTO ad_views(ad_id,view_time) VALUES(?,datetime('now'))", (ad['id'],))
            conn.commit()

            wa = f"https://wa.me/213{re.sub(r'\D', '', ad['phone'])[-9:]}"
            
            st.markdown(f"""
                <div class="ad-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <h2 style="margin:0; color:#006633;">{ad['product']} {f'<span style="background:#ffd700; color:black; font-size:0.8rem; padding:2px 10px; border-radius:5px;">مميز</span>' if ad['featured'] else ''}</h2>
                            <p style="color:#666;">📍 {ad['wilaya']} | 👤 {ad['owner']} | 📅 {ad['date']}</p>
                            <p style="font-size:1.2rem;">{ad['description']}</p>
                            <span style="color:#f39c12;">★ {round(ad['avg_r'],1)} ({ad['count_r']})</span> | 👁️ {ad['views']+1}
                        </div>
                        <div style="text-align:left;">
                            <div class="price-tag">{ad['price']:,} دج</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # 💬 Conversion Tracking (WhatsApp Button)
            click_id = f"click_{ad['id']}_{time.time()}"
            if st.button("اتصال واتساب 💬", key=click_id):
                conn.execute("INSERT INTO clicks(ad_id,click_time) VALUES(?,datetime('now'))", (ad['id'],))
                conn.commit()
                st.link_button("فتح المحادثة الآن", wa)

    # --- Analytics MAX (مؤشرات الذكاء السوقي) ---
    with tab3:
        conn.execute("INSERT INTO page_views(page,view_time) VALUES('analytics',datetime('now'))")
        conn.commit()
        st.subheader("📊 إحصائيات TITANIUM MAX المتقدمة")
        
        today = str(datetime.date.today())
        total_views_ads = conn.execute("SELECT SUM(views) FROM ads").fetchone()[0] or 0
        total_clicks = conn.execute("SELECT COUNT(*) FROM clicks").fetchone()[0]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🌍 زوار فريدون", conn.execute("SELECT COUNT(DISTINCT ip) FROM visitors").fetchone()[0])
        c2.metric("📢 إجمالي الإعلانات", conn.execute("SELECT COUNT(*) FROM ads").fetchone()[0])
        c3.metric("👤 مستخدمون", conn.execute("SELECT COUNT(*) FROM users").fetchone()[0])
        c4.metric("👁️ مشاهدات السوق", total_views_ads)

        # 🧠 مؤشرات الذكاء السوقي
        st.divider()
        st.subheader("🧠 مؤشرات الذكاء السوقي")
        
        avg_session = conn.execute("SELECT AVG(duration) FROM sessions").fetchone()[0]
        conversion = (total_clicks / total_views_ads * 100) if total_views_ads > 0 else 0
        hour_peak = conn.execute("SELECT strftime('%H',view_time) h, COUNT(*) c FROM ad_views GROUP BY h ORDER BY c DESC LIMIT 1").fetchone()
        top_engaged = conn.execute("SELECT product, views + (SELECT COUNT(*) FROM clicks WHERE ad_id=ads.id) score FROM ads ORDER BY score DESC LIMIT 1").fetchone()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("⏱️ متوسط مدة الجلسة", f"{int(avg_session) if avg_session else 0} ث")
        m2.metric("🎯 معدل التحويل", f"{conversion:.2f}%")
        if hour_peak: m3.metric("⏰ ذروة النشاط", f"{hour_peak[0]}:00")
        if top_engaged: m4.metric("🔥 الأعلى تفاعل", top_engaged[0])

        st.subheader("📈 نمو المنصة")
        growth = pd.read_sql("SELECT visit_date d, COUNT(*) v FROM visitors GROUP BY d ORDER BY d DESC LIMIT 30", conn)
        if not growth.empty: st.line_chart(growth.set_index("d"))

    # --- نشر الإعلانات ---
    with tab2:
        conn.execute("INSERT INTO page_views(page,view_time) VALUES('publish',datetime('now'))")
        conn.commit()
        with st.form("max_post"):
            st.subheader("📢 تفاصيل الإعلان")
            col1, col2 = st.columns(2)
            name = col1.text_input("موديل الجهاز")
            pr = col2.number_input("السعر بالدينار", min_value=0)
            ph = col1.text_input("رقم الهاتف")
            wi = col2.selectbox("الولاية", [f"{i:02d}" for i in range(1, 59)])
            ds = st.text_area("وصف شامل")
            if st.form_submit_button("نشر الإعلان 🚀"):
                if name and ph:
                    conn.execute("INSERT INTO ads(product,price,phone,wilaya,description,date,owner) VALUES(?,?,?,?,?,?,?)", (name, pr, ph, wi, ds, today, st.session_state.user))
                    conn.execute("UPDATE users SET ad_count = ad_count + 1 WHERE username=?", (st.session_state.user,))
                    conn.commit()
                    st.success("تم النشر!")

    # --- الإدارة والذكاء الإداري ---
    with tab4:
        role = conn.execute("SELECT role FROM users WHERE username=?", (st.session_state.user,)).fetchone()[0]
        if role == "admin":
            # إدارة الإعلانات المميزة
            st.subheader("💎 إدارة تمييز الإعلانات")
            ads_df = pd.read_sql("SELECT id, product, featured FROM ads", conn)
            edited = st.data_editor(ads_df)
            if st.button("تحديث التمييز"):
                for _, row in edited.iterrows():
                    conn.execute("UPDATE ads SET featured=? WHERE id=?", (row['featured'], row['id']))
                conn.commit()
                st.success("تم التحديث")

            # 📊 نشاط المستخدمين
            st.subheader("📊 نشاط المستخدمين التفصيلي")
            user_stats = pd.read_sql("SELECT u.username, u.ad_count, COUNT(DISTINCT a.id) ads, IFNULL(SUM(a.views),0) views FROM users u LEFT JOIN ads a ON u.username=a.owner GROUP BY u.username", conn)
            st.dataframe(user_stats)

            # 🚨 كشف الحسابات المشبوهة
            st.subheader("🚨 كشف الحسابات المشبوهة")
            suspicious = conn.execute("SELECT username, COUNT(*) attempts FROM login_attempts GROUP BY username HAVING attempts > 10").fetchall()
            if suspicious:
                st.warning("حسابات بمحاولات دخول كثيرة (احتمال هجوم):")
                st.write(suspicious)
            else: st.success("لا يوجد نشاط مشبوه حالياً.")
        else: st.warning("🔒 خاص بالمدراء")

# ==========================================
# Run
# ==========================================
if st.session_state.user: dashboard()
else: auth_page()
