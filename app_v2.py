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
# 1. إعدادات النخبة TITANIUM ULTRA MAX 2026
# ==========================================
st.set_page_config(page_title="RASSIM DZ TITANIUM ULTRA", layout="wide", page_icon="🇩🇿")
DB = "rassim_titanium_max_2026.db"

# إعدادات المجلدات
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# التصميم (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background: #f0f2f6; }
    .main-header {
        background: linear-gradient(135deg, #006633 0%, #d21034 100%);
        padding: 40px; border-radius: 20px; text-align: center; color: white; margin-bottom: 30px;
    }
    .stats-container {
        display: flex; justify-content: space-around; background: white; padding: 20px;
        border-radius: 15px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stat-box { text-align: center; }
    .stat-val { font-size: 2rem; font-weight: 900; color: #d21034; }
    .ad-card { 
        background: white; border-radius: 20px; padding: 20px; 
        border-right: 10px solid #006633; margin-bottom: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    .price-tag { background: #d21034; color: white; padding: 5px 15px; border-radius: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. إدارة قاعدة البيانات والزيارات
# ==========================================
def init_db():
    conn = sqlite3.connect(DB)
    # جدول المستخدمين
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, salt TEXT, role TEXT DEFAULT 'user')")
    # جدول الإعلانات
    conn.execute("""CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT, product TEXT, price REAL, phone TEXT, 
        wilaya TEXT, description TEXT, date TEXT, owner TEXT, views INTEGER DEFAULT 0, 
        featured INTEGER DEFAULT 0, category TEXT, images TEXT, status TEXT DEFAULT 'active')""")
    # جدول الرسائل
    conn.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, from_user TEXT, to_user TEXT, message TEXT, date TEXT, read INTEGER DEFAULT 0)")
    # جدول الزوار
    conn.execute("CREATE TABLE IF NOT EXISTS site_analytics (ip TEXT, visit_date TEXT)")
    conn.commit()
    return conn

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)

def log_visitor():
    conn = get_connection()
    # محاكاة لعنوان IP بسيط (في Streamlit Cloud يفضل استخدام طرق أخرى لكن هذه تعمل كعداد)
    conn.execute("INSERT INTO site_analytics (ip, visit_date) VALUES (?, datetime('now'))", ("guest_ip",))
    conn.commit()

def get_stats():
    conn = get_connection()
    users_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    visitors_count = conn.execute("SELECT COUNT(*) FROM site_analytics").fetchone()[0]
    ads_count = conn.execute("SELECT COUNT(*) FROM ads WHERE status='active'").fetchone()[0]
    return users_count, visitors_count, ads_count

# ==========================================
# 3. محرك الذكاء الاصطناعي (AI ENGINE)
# ==========================================
class AIEngine:
    def __init__(self):
        self.conn = get_connection()
        
    def get_similar_ads(self, ad_id, limit=3):
        try:
            ads_data = self.conn.execute("SELECT id, product, category FROM ads WHERE status='active' AND id != ?", (ad_id,)).fetchall()
            if len(ads_data) < 2: return []
            return ads_data[:limit] # تبسيط مؤقت للسرعة
        except: return []

# ==========================================
# 4. الواجهات (UI)
# ==========================================
def show_market(conn):
    st.markdown("<h2 style='text-align:right;'>🛒 السوق الحالي</h2>", unsafe_allow_html=True)
    
    # فلترة
    c1, c2 = st.columns(2)
    cat_filter = c1.selectbox("الفئة", ["الكل", "إلكترونيات", "عقارات", "سيارات"])
    wilaya_filter = c2.selectbox("الولاية", ["الكل"] + [f"{i:02d}" for i in range(1, 59)])

    query = "SELECT * FROM ads WHERE status='active'"
    params = []
    if cat_filter != "الكل": query += " AND category=?"; params.append(cat_filter)
    if wilaya_filter != "الكل": query += " AND wilaya=?"; params.append(wilaya_filter)
    
    ads = conn.execute(query + " ORDER BY id DESC", params).fetchall()

    for ad in ads:
        with st.container():
            # تصحيح الـ KeyError: ننادي الأعمدة بالأرقام لأننا نستخدم fetchall()
            # ad[1]=product, ad[2]=price, ad[4]=wilaya, ad[10]=category
            st.markdown(f"""
                <div class="ad-card">
                    <div style="display:flex; justify-content:space-between;">
                        <div>
                            <h3 style="margin:0;">{ad[1]}</h3>
                            <p style="color:gray; font-size:0.9rem;">الفئة: {ad[10]} | الولاية: {ad[4]}</p>
                            <p>{ad[5][:100]}...</p>
                            <span class="price-tag">{ad[2]:,} دج</span>
                        </div>
                        <div>
                            <small>👤 {ad[7]}</small><br>
                            <small>📅 {ad[6]}</small>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"📞 التواصل مع البائع", key=f"btn_{ad[0]}"):
                st.success(f"رقم الهاتف: {ad[3]}")

def post_ad(conn):
    st.header("📢 نشر إعلان جديد")
    with st.form("new_ad"):
        name = st.text_input("اسم المنتج")
        price = st.number_input("السعر (دج)", min_value=0)
        cat = st.selectbox("الفئة", ["إلكترونيات", "عقارات", "سيارات", "أخرى"])
        wilaya = st.selectbox("الولاية", [f"{i:02d}" for i in range(1, 59)])
        desc = st.text_area("وصف المنتج")
        phone = st.text_input("رقم الهاتف")
        if st.form_submit_button("نشر"):
            conn.execute("INSERT INTO ads(product, price, phone, wilaya, description, date, owner, category) VALUES(?,?,?,?,?,datetime('now'),?,?)",
                         (name, price, phone, wilaya, desc, st.session_state.user, cat))
            conn.commit()
            st.success("تم النشر!")

# ==========================================
# 5. التشغيل الرئيسي
# ==========================================
def main():
    init_db()
    log_visitor()
    
    if "user" not in st.session_state: st.session_state.user = None

    if not st.session_state.user:
        st.markdown('<div class="main-header"><h1>🇩🇿 RASSIM DZ TITANIUM ULTRA</h1></div>', unsafe_allow_html=True)
        
        # عرض الإحصائيات في الصفحة الرئيسية
        u_count, v_count, a_count = get_stats()
        st.markdown(f"""
            <div class="stats-container">
                <div class="stat-box"><div class="stat-val">{u_count}</div><div>مشارك</div></div>
                <div class="stat-box"><div class="stat-val">{v_count}</div><div>زائر</div></div>
                <div class="stat-box"><div class="stat-val">{a_count}</div><div>إعلان نشط</div></div>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔐 دخول")
            user = st.text_input("المستخدم")
            pw = st.text_input("السر", type="password")
            if st.button("دخول"):
                res = get_connection().execute("SELECT password, salt FROM users WHERE username=?", (user,)).fetchone()
                if res and res[0] == hashlib.pbkdf2_hmac('sha256', pw.encode(), res[1].encode(), 100000).hex():
                    st.session_state.user = user
                    st.rerun()
        with col2:
            st.subheader("📝 تسجيل")
            nu = st.text_input("مستخدم جديد")
            np = st.text_input("سر جديد", type="password")
            if st.button("تسجيل جديد"):
                salt = secrets.token_hex(16)
                h = hashlib.pbkdf2_hmac('sha256', np.encode(), salt.encode(), 100000).hex()
                try:
                    conn = get_connection()
                    conn.execute("INSERT INTO users(username, password, salt) VALUES(?,?,?)", (nu, h, salt))
                    conn.commit()
                    st.success("تم!")
                except: st.error("موجود مسبقاً")

    else:
        with st.sidebar:
            st.header(f"👋 أهلاً {st.session_state.user}")
            menu = st.radio("القائمة", ["السوق", "نشر إعلان", "الإحصائيات", "خروج"])
        
        conn = get_connection()
        if menu == "السوق": show_market(conn)
        elif menu == "نشر إعلان": post_ad(conn)
        elif menu == "الإحصائيات":
            u_count, v_count, a_count = get_stats()
            st.metric("إجمالي المشاركين", u_count)
            st.metric("إجمالي الزيارات", v_count)
            st.metric("الإعلانات", a_count)
        elif menu == "خروج":
            st.session_state.user = None
            st.rerun()

if __name__ == "__main__":
    main()
