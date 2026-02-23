import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import secrets
import os
import datetime
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

# ==========================================
# 1. إعدادات النخبة وتصحيح الـ CSS (حل مشكلة الحروف المبعثرة)
# ==========================================
st.set_page_config(page_title="RASSIM DZ TITANIUM ULTRA", layout="wide", page_icon="🇩🇿")
DB = "rassim_titanium_max_2026.db"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* ضبط الاتجاه والخط بشكل جذري */
    html, body, [class*="css"], .stApp {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }

    /* الهيدر المتجاوب - حل مشكلة التداخل */
    .main-header {
        background: linear-gradient(135deg, #006633 0%, #d21034 100%);
        padding: 40px 20px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        overflow: hidden;
    }

    /* إصلاح حاوية الإحصائيات لتناسب الهاتف */
    .stats-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        gap: 15px;
    }

    .stat-box {
        text-align: center;
        flex: 1;
        min-width: 120px;
    }

    .stat-val {
        font-size: 2rem;
        font-weight: 900;
        color: #d21034;
        display: block;
    }

    /* بطاقة الإعلان الاحترافية */
    .ad-card { 
        background: white;
        border-radius: 15px;
        padding: 20px; 
        border-right: 10px solid #006633;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        transition: 0.3s ease;
    }
    .ad-card:hover {
        transform: translateY(-5px);
        border-right-color: #d21034;
    }

    .price-tag {
        background: #006633;
        color: white;
        padding: 5px 15px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.2rem;
    }

    /* إخفاء عناصر Streamlit التي تسبب تشويش */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. محرك قاعدة البيانات المطور (حماية البيانات 100%)
# ==========================================
def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    # الجداول الأساسية
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, salt TEXT, role TEXT DEFAULT 'user', banned INTEGER DEFAULT 0)")
    cursor.execute("""CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT, product TEXT, price REAL, phone TEXT, 
        wilaya TEXT, description TEXT, date TEXT, owner TEXT, views INTEGER DEFAULT 0, 
        featured INTEGER DEFAULT 0, category TEXT DEFAULT 'أخرى', images TEXT, status TEXT DEFAULT 'active')""")
    cursor.execute("CREATE TABLE IF NOT EXISTS site_analytics (ip TEXT, visit_date TEXT)")
    
    # ترقية تلقائية (Migration) لضمان عدم حدوث OperationalError
    cursor.execute("PRAGMA table_info(ads)")
    cols = [c[1] for c in cursor.fetchall()]
    if 'status' not in cols:
        cursor.execute("ALTER TABLE ads ADD COLUMN status TEXT DEFAULT 'active'")
    if 'category' not in cols:
        cursor.execute("ALTER TABLE ads ADD COLUMN category TEXT DEFAULT 'أخرى'")
    
    conn.commit()
    return conn

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)

def get_stats():
    conn = get_connection()
    try:
        u = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        v = conn.execute("SELECT COUNT(*) FROM site_analytics").fetchone()[0]
        a = conn.execute("SELECT COUNT(*) FROM ads WHERE status='active'").fetchone()[0]
        return u, v, a
    except:
        return 0, 0, 0

# ==========================================
# 3. الوظائف الرئيسية (سوق، نشر، إدارة)
# ==========================================
def show_market(conn):
    st.header("🛍️ السوق الذكي")
    
    # نظام الفلاتر المبسط
    col1, col2 = st.columns(2)
    with col1:
        search_q = st.text_input("🔍 ابحث عن هاتف أو منتج...")
    with col2:
        wilaya_f = st.selectbox("📍 فلترة حسب الولاية", ["الكل"] + [f"{i:02d}" for i in range(1, 59)])

    query = "SELECT * FROM ads WHERE status='active'"
    params = []
    
    if search_q:
        query += " AND (product LIKE ? OR description LIKE ?)"
        params.extend([f'%{search_q}%', f'%{search_q}%'])
    if wilaya_f != "الكل":
        query += " AND wilaya = ?"
        params.append(wilaya_f)
        
    ads = conn.execute(query + " ORDER BY featured DESC, id DESC", params).fetchall()

    if not ads:
        st.info("لا توجد نتائج تطابق بحثك حالياً.")
    else:
        for ad in ads:
            with st.container():
                st.markdown(f"""
                <div class="ad-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                        <div>
                            <h3 style="margin:0; color:#d21034;">{ad[1]} {"⭐" if ad[9] else ""}</h3>
                            <p style="margin:5px 0; color:#555;">📍 ولاية: {ad[4]} | 📅 {ad[6][:10]}</p>
                            <span class="price-tag">{ad[2]:,} دج</span>
                        </div>
                        <div style="text-align:left; margin-top:10px;">
                            <small>👤 البائع: {ad[7]}</small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📞 أظهر رقم الهاتف", key=f"btn_{ad[0]}"):
                    st.success(f"رقم التواصل: {ad[3]}")
                    conn.execute("UPDATE ads SET views = views + 1 WHERE id = ?", (ad[0],))
                    conn.commit()

def post_ad(conn):
    st.header("📢 أنشئ إعلانك")
    with st.form("post_form"):
        p_name = st.text_input("اسم المنتج (مثلاً: iPhone 15 Pro)")
        p_price = st.number_input("السعر (دج)", min_value=0)
        p_wilaya = st.selectbox("الولاية", [f"{i:02d}" for i in range(1, 59)])
        p_cat = st.selectbox("الفئة", ["هواتف", "إكسسوارات", "كمبيوتر", "أخرى"])
        p_desc = st.text_area("وصف المنتج")
        p_phone = st.text_input("رقم الهاتف")
        submit = st.form_submit_button("🚀 نشر الإعلان الآن")
        
        if submit:
            if p_name and p_phone and p_price > 0:
                conn.execute("INSERT INTO ads (product, price, phone, wilaya, description, date, owner, category) VALUES (?,?,?,?,?,datetime('now'),?,?)",
                             (p_name, p_price, p_phone, p_wilaya, p_desc, st.session_state.user, p_cat))
                conn.commit()
                st.balloons()
                st.success("تم النشر بنجاح! إعلانك الآن متاح للجميع.")
            else:
                st.error("يرجى ملء جميع البيانات الأساسية.")

# ==========================================
# 4. محرك التشغيل الرئيسي
# ==========================================
def main():
    init_db()
    conn = get_connection()
    
    if "user" not in st.session_state:
        st.session_state.user = None

    if not st.session_state.user:
        # واجهة الترحيب
        st.markdown('<div class="main-header"><h1>🇩🇿 RASSIM DZ TITANIUM ULTRA</h1><p>سوق الهواتف والأجهزة الأول في الجزائر</p></div>', unsafe_allow_html=True)
        
        u_count, v_count, a_count = get_stats()
        st.markdown(f"""
            <div class="stats-container">
                <div class="stat-box"><span class="stat-val">{u_count}</span><span class="stat-label">مشارك</span></div>
                <div class="stat-box"><span class="stat-val">{a_count}</span><span class="stat-label">إعلان نشط</span></div>
                <div class="stat-box"><span class="stat-val">{v_count}</span><span class="stat-label">زيارة</span></div>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 حساب جديد"])
        with tab1:
            u = st.text_input("اسم المستخدم", key="login_u")
            p = st.text_input("كلمة السر", type="password", key="login_p")
            if st.button("دخول"):
                res = conn.execute("SELECT password, salt FROM users WHERE username=?", (u,)).fetchone()
                if res and res[0] == hashlib.pbkdf2_hmac('sha256', p.encode(), res[1].encode(), 100000).hex():
                    st.session_state.user = u
                    conn.execute("INSERT INTO site_analytics VALUES (?, datetime('now'))", (u,))
                    conn.commit()
                    st.rerun()
                else: st.error("عذراً، تأكد من البيانات")
        with tab2:
            nu = st.text_input("اختر اسم مستخدم", key="reg_u")
            np = st.text_input("اختر كلمة سر", type="password", key="reg_p")
            if st.button("إنشاء حساب"):
                if len(nu) > 2 and len(np) > 5:
                    salt = secrets.token_hex(16)
                    h = hashlib.pbkdf2_hmac('sha256', np.encode(), salt.encode(), 100000).hex()
                    try:
                        conn.execute("INSERT INTO users (username, password, salt) VALUES (?,?,?)", (nu, h, salt))
                        conn.commit()
                        st.success("تم إنشاء الحساب! سجل دخولك الآن.")
                    except: st.error("الاسم مأخوذ من قبل")
                else: st.warning("الاسم قصير جداً أو كلمة السر ضعيفة")

    else:
        # واجهة المستخدم المسجل
        with st.sidebar:
            st.markdown(f"### ✨ مرحباً {st.session_state.user}")
            menu = st.radio("القائمة:", ["🛒 تصفح السوق", "➕ انشر إعلان", "📊 إحصائياتي", "🚪 خروج"])
            
            # قسم الإدارة السري
            st.divider()
            with st.expander("🛠 الإدارة"):
                ad_pass = st.text_input("كلمة سر المسؤول", type="password")
                if ad_pass == "racim2026":
                    if st.button("فتح لوحة التحكم"): st.session_state.admin = True

        if menu == "🛒 تصفح السوق": show_market(conn)
        elif menu == "➕ انشر إعلان": post_ad(conn)
        elif menu == "🚪 خروج":
            st.session_state.user = None
            st.rerun()

if __name__ == "__main__":
    main()
