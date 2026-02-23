import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import secrets
import os
import time
import base64
import plotly.express as px
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import warnings

warnings.filterwarnings('ignore')

# ==========================================
# 1. الإعدادات وتصميم الواجهة
# ==========================================
st.set_page_config(page_title="RASSIM DZ TITANIUM ULTRA", layout="wide", page_icon="🇩🇿")
DB = "rassim_titanium_max_2026.db"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background: #f4f7f9; }
    .main-header {
        background: linear-gradient(135deg, #006633 0%, #d21034 100%);
        padding: 40px; border-radius: 20px; text-align: center; color: white; margin-bottom: 30px;
    }
    .stats-container {
        display: flex; justify-content: space-around; background: white; padding: 20px;
        border-radius: 15px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stat-box { text-align: center; flex: 1; }
    .stat-val { font-size: 2.2rem; font-weight: 900; color: #d21034; }
    .ad-card { 
        background: white; border-radius: 15px; padding: 20px; 
        border-right: 8px solid #006633; margin-bottom: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .price-tag { background: #006633; color: white; padding: 5px 12px; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. محرك قاعدة البيانات (مع نظام الحفاظ على البيانات)
# ==========================================
def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    # إنشاء الجداول الأساسية
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, salt TEXT, role TEXT DEFAULT 'user')")
    cursor.execute("""CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT, product TEXT, price REAL, phone TEXT, 
        wilaya TEXT, description TEXT, date TEXT, owner TEXT, views INTEGER DEFAULT 0, 
        featured INTEGER DEFAULT 0, category TEXT, images TEXT, status TEXT DEFAULT 'active')""")
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, from_user TEXT, to_user TEXT, message TEXT, date TEXT, read INTEGER DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS site_analytics (ip TEXT, visit_date TEXT)")
    
    # --- نظام الترقية الذكي (حماية البيانات) ---
    # فحص الأعمدة الموجودة في جدول ads
    cursor.execute("PRAGMA table_info(ads)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    
    # إضافة الأعمدة الناقصة إذا لم تكن موجودة (دون حذف البيانات)
    columns_to_check = {
        'status': "TEXT DEFAULT 'active'",
        'category': "TEXT DEFAULT 'أخرى'",
        'views': "INTEGER DEFAULT 0",
        'featured': "INTEGER DEFAULT 0"
    }
    
    for col_name, col_type in columns_to_check.items():
        if col_name not in existing_columns:
            try:
                cursor.execute(f"ALTER TABLE ads ADD COLUMN {col_name} {col_type}")
            except Exception as e:
                pass # العمود قد يكون أضيف في جلسة أخرى

    conn.commit()
    return conn

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)

def log_visitor():
    conn = get_connection()
    conn.execute("INSERT INTO site_analytics (ip, visit_date) VALUES (?, datetime('now'))", ("guest",))
    conn.commit()

def get_stats():
    conn = get_connection()
    # استخدام try/except كطبقة حماية ثانية لضمان عمل الواجهة حتى لو تعطلت قاعدة البيانات
    try:
        u = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        v = conn.execute("SELECT COUNT(*) FROM site_analytics").fetchone()[0]
        a = conn.execute("SELECT COUNT(*) FROM ads").fetchone()[0]
        return u, v, a
    except:
        return 0, 0, 0

# ==========================================
# 3. الوظائف الرئيسية (سوق، نشر، إلخ)
# ==========================================
def show_market(conn):
    st.subheader("🛍️ المنتجات المتاحة")
    
    # نظام البحث
    search_q = st.text_input("🔍 ابحث عن هاتف أو منتج...")
    
    query = "SELECT * FROM ads WHERE 1=1"
    params = []
    if search_q:
        query += " AND (product LIKE ? OR description LIKE ?)"
        params.extend([f'%{search_q}%', f'%{search_q}%'])
    
    ads = conn.execute(query + " ORDER BY id DESC", params).fetchall()

    if not ads:
        st.info("لا توجد إعلانات حالياً.")
    else:
        for ad in ads:
            with st.container():
                # استخدام الفهارس الرقمية لضمان الدقة (ad[1] هو المنتج، ad[2] السعر، إلخ)
                st.markdown(f"""
                <div class="ad-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <h3 style="margin:0; color:#d21034;">{ad[1]}</h3>
                            <p style="margin:5px 0; color:#555;">📍 {ad[4]} | 📅 {ad[6]}</p>
                            <span class="price-tag">{ad[2]:,} دج</span>
                        </div>
                        <div style="text-align:left;">
                            <small>👤 البائع: {ad[7]}</small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📞 التواصل مع البائع", key=f"btn_{ad[0]}"):
                    st.success(f"رقم الهاتف للتواصل: {ad[3]}")

def post_ad(conn):
    st.subheader("📢 انشر إعلانك الآن")
    with st.form("ad_form"):
        p_name = st.text_input("اسم المنتج")
        p_price = st.number_input("السعر", min_value=0)
        p_wilaya = st.selectbox("الولاية", [f"{i:02d}" for i in range(1, 59)])
        p_desc = st.text_area("تفاصيل إضافية")
        p_phone = st.text_input("رقم الهاتف")
        if st.form_submit_button("🚀 نشر الإعلان"):
            if p_name and p_phone:
                conn.execute("INSERT INTO ads (product, price, phone, wilaya, description, date, owner) VALUES (?,?,?,?,?,datetime('now'),?)",
                             (p_name, p_price, p_phone, p_wilaya, p_desc, st.session_state.user))
                conn.commit()
                st.success("تم النشر بنجاح! سيظهر إعلانك في السوق فوراً.")
            else:
                st.warning("يرجى ملء البيانات الأساسية.")

# ==========================================
# 4. محرك التشغيل الرئيسي
# ==========================================
def main():
    init_db() # تشغيل الترقية التلقائية وحماية البيانات
    log_visitor()
    
    if "user" not in st.session_state:
        st.session_state.user = None

    if not st.session_state.user:
        st.markdown('<div class="main-header"><h1>🇩🇿 RASSIM DZ TITANIUM ULTRA</h1><p>منصة التجارة الأسرع في الجزائر</p></div>', unsafe_allow_html=True)
        
        # عرض عداد الزوار والمشاركين
        u_count, v_count, a_count = get_stats()
        st.markdown(f"""
            <div class="stats-container">
                <div class="stat-box"><div class="stat-val">{u_count}</div><div>مشارك مسجل</div></div>
                <div class="stat-box"><div class="stat-val">{v_count}</div><div>زيارة إجمالية</div></div>
                <div class="stat-box"><div class="stat-val">{a_count}</div><div>إعلان معروض</div></div>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 حساب جديد"])
        with tab1:
            u = st.text_input("اسم المستخدم")
            p = st.text_input("كلمة السر", type="password")
            if st.button("دخول"):
                res = get_connection().execute("SELECT password, salt FROM users WHERE username=?", (u,)).fetchone()
                if res and res[0] == hashlib.pbkdf2_hmac('sha256', p.encode(), res[1].encode(), 100000).hex():
                    st.session_state.user = u
                    st.rerun()
                else: st.error("خطأ في البيانات")
        with tab2:
            nu = st.text_input("اسم جديد")
            np = st.text_input("سر جديد", type="password")
            if st.button("إنشاء الحساب"):
                salt = secrets.token_hex(16)
                h = hashlib.pbkdf2_hmac('sha256', np.encode(), salt.encode(), 100000).hex()
                try:
                    c = get_connection()
                    c.execute("INSERT INTO users (username, password, salt) VALUES (?,?,?)", (nu, h, salt))
                    c.commit()
                    st.success("تم التسجيل! يمكنك الدخول الآن.")
                except: st.error("الاسم مستخدم بالفعل")

    else:
        with st.sidebar:
            st.title(f"👋 مرحباً {st.session_state.user}")
            menu = st.radio("انتقل إلى:", ["السوق الذكي", "نشر إعلان", "إحصائياتي", "خروج"])
        
        conn = get_connection()
        if menu == "السوق الذكي": show_market(conn)
        elif menu == "نشر إعلان": post_ad(conn)
        elif menu == "خروج":
            st.session_state.user = None
            st.rerun()

if __name__ == "__main__":
    main()
# ==========================================
# 5. لوحة التحكم السرية (للمسؤول فقط)
# ==========================================
def admin_dashboard(conn):
    st.markdown("<h2 style='color:#d21034;'>🔐 لوحة تحكم الإدارة السرية</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["👥 المستخدمين", "📈 إحصائيات الزوار", "🚫 إدارة المحتوى"])
    
    with tab1:
        users_df = pd.read_sql_query("SELECT username, role FROM users", conn)
        st.dataframe(users_df, use_container_width=True)
        
    with tab2:
        visits_df = pd.read_sql_query("SELECT visit_date, ip FROM site_analytics ORDER BY visit_date DESC", conn)
        st.line_chart(visits_df.groupby('visit_date').count())
        st.write("أحدث الزيارات:", visits_df.head(20))
        
    with tab3:
        st.subheader("حذف إعلانات مخالفة")
        ads_to_manage = conn.execute("SELECT id, product, owner FROM ads").fetchall()
        for ad in ads_to_manage:
            col1, col2 = st.columns([3, 1])
            col1.write(f"📦 {ad[1]} (بواسطة: {ad[2]})")
            if col2.button("❌ حذف", key=f"del_{ad[0]}"):
                conn.execute("DELETE FROM ads WHERE id=?", (ad[0],))
                conn.commit()
                st.error(f"تم حذف إعلان {ad[1]}")
                st.rerun()

# تعديل بسيط في جزء القائمة الجانبية (Sidebar) داخل دالة main():
# ابحث عن الجزء الخاص بالـ sidebar واستبدله بهذا:
with st.sidebar:
    st.title(f"👋 مرحباً {st.session_state.user}")
    menu = st.radio("انتقل إلى:", ["السوق الذكي", "نشر إعلان", "خروج"])
    
    st.divider()
    # المنطقة السرية
    with st.expander("🛠 خيارات متقدمة"):
        admin_pass = st.text_input("كلمة سر الإدارة", type="password")
        if admin_pass == "racim2026": # يمكنك تغيير كلمة السر هنا
            show_admin = st.checkbox("فتح لوحة التحكم")
        else:
            show_admin = False

# ثم في الجزء السفلي من main() حيث تظهر الصفحات:
if st.session_state.user:
    if show_admin:
        admin_dashboard(conn)
    else:
        if menu == "السوق الذكي": show_market(conn)
        elif menu == "نشر إعلان": post_ad(conn)
