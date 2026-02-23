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
import random
import json
import smtplib
import base64
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps
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
OLD_DB = "rassim_titanium_pro_2026.db" 

# إعدادات متقدمة
AI_ENABLED = True
CHATBOT_ENABLED = True
PRICE_PREDICTION_ENABLED = True
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .main-header {
        background: linear-gradient(135deg, #006633 0%, #006633 48%, #d21034 50%, #ffffff 52%, #ffffff 100%);
        padding: 60px; border-radius: 40px; text-align: center; box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        border-bottom: 12px solid #d21034; margin-bottom: 40px; color: white;
        animation: glow 2s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { box-shadow: 0 25px 50px rgba(0,102,51,0.3); }
        to { box-shadow: 0 25px 70px rgba(210,16,52,0.5); }
    }
    .ad-card { 
        background: white; border-radius: 25px; padding: 25px; 
        border-right: 15px solid #006633; margin-bottom: 25px; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); transition: 0.4s;
    }
    .ad-card:hover { transform: translateY(-5px); border-right-color: #d21034; box-shadow: 0 15px 35px rgba(0,0,0,0.2); }
    .price-tag { 
        background: linear-gradient(135deg, #d21034, #ff416c); 
        color: white; padding: 10px 25px; border-radius: 15px; 
        font-weight: 900; font-size: 1.6rem; 
    }
    .chat-bubble { padding: 12px; border-radius: 18px; margin-bottom: 8px; max-width: 85%; position: relative; }
    .chat-sent { background: #dcf8c6; align-self: flex-start; margin-right: auto; border-bottom-left-radius: 2px; }
    .chat-received { background: #f0f0f0; align-self: flex-end; margin-left: auto; border-bottom-right-radius: 2px; }
    .badge-premium { background: gold; color: black; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.8rem; }
    .ai-suggestion { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); color: white; padding: 20px; border-radius: 25px; border: 1px solid rgba(255,255,255,0.2); }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. محرك الاتصال الأساسي
# ==========================================
@st.cache_resource
def get_connection():
    conn = sqlite3.connect(DB, check_same_thread=False)
    return conn

def get_image_base64(image_file):
    return base64.b64encode(image_file.read()).decode()

# ==========================================
# 3. محرك الذكاء الاصطناعي (AI ENGINE) - كامل كما هو مع تحسينات
# ==========================================
class AIEngine:
    def __init__(self):
        self.conn = get_connection()
        
    def get_similar_ads(self, ad_id, limit=5):
        try:
            ads_data = self.conn.execute("SELECT id, product, description, category FROM ads WHERE status='active' AND id != ?", (ad_id,)).fetchall()
            if len(ads_data) < 2: return []
            texts = [f"{a[1]} {a[2]} {a[3]}".lower() for a in ads_data]
            vectorizer = TfidfVectorizer(max_features=100)
            tfidf_matrix = vectorizer.fit_transform(texts)
            similarity_matrix = cosine_similarity(tfidf_matrix)
            indices = similarity_matrix[0].argsort()[-limit:][::-1]
            return [ads_data[i] for i in indices if i < len(ads_data)]
        except: return []

    def predict_price(self, category, wilaya):
        try:
            prices = self.conn.execute("SELECT price FROM ads WHERE category=? AND wilaya=? AND price > 0", (category, wilaya)).fetchall()
            if len(prices) < 3: return None
            p_list = [p[0] for p in prices]
            return {'predicted': int(np.median(p_list)), 'avg': int(np.mean(p_list)), 'min': min(p_list), 'max': max(p_list), 'sample_size': len(p_list)}
        except: return None

    def analyze_user_behavior(self, username):
        viewed = self.conn.execute("""SELECT a.category, a.price FROM ad_views v JOIN ads a ON v.ad_id = a.id WHERE v.viewer_ip IN (SELECT ip FROM visitors) LIMIT 10""").fetchall()
        if not viewed: return None
        cats = [v[0] for v in viewed if v[0]]
        return {'favorite_category': Counter(cats).most_common(1)[0][0] if cats else "أخرى", 'average_budget': np.mean([v[1] for v in viewed if v[1]>0])}

# ==========================================
# 4. نظام المراسلة والدردشة (LATEST)
# ==========================================
def show_chat_system(conn):
    st.header("💬 مركز الرسائل الذكي")
    user = st.session_state.user
    contacts = conn.execute("""
        SELECT DISTINCT CASE WHEN from_user = ? THEN to_user ELSE from_user END as contact,
        MAX(date) as last_msg, (SELECT COUNT(*) FROM messages WHERE to_user=? AND from_user=contact AND read=0)
        FROM messages WHERE from_user = ? OR to_user = ? GROUP BY contact ORDER BY last_msg DESC
    """, (user, user, user, user)).fetchall()
    
    if not contacts:
        st.info("لا توجد مراسلات حالية.")
        return

    col1, col2 = st.columns([1, 2])
    with col1:
        selected_contact = st.radio("المحادثات:", [c[0] for c in contacts])
    
    with col2:
        if selected_contact:
            conn.execute("UPDATE messages SET read=1 WHERE from_user=? AND to_user=?", (selected_contact, user))
            conn.commit()
            msgs = conn.execute("SELECT from_user, message, date FROM messages WHERE (from_user=? AND to_user=?) OR (from_user=? AND to_user=?) ORDER BY date ASC", (user, selected_contact, selected_contact, user)).fetchall()
            
            chat_box = st.container(height=400)
            for m in msgs:
                cls = "chat-sent" if m[0] == user else "chat-received"
                chat_box.markdown(f'<div class="chat-bubble {cls}"><b>{m[0]}</b><br>{m[1]}<br><small>{m[2][11:16]}</small></div>', unsafe_allow_html=True)
            
            with st.form("send_chat", clear_on_submit=True):
                txt = st.text_input("رسالتك...")
                if st.form_submit_button("إرسال") and txt:
                    conn.execute("INSERT INTO messages(from_user, to_user, message, date) VALUES(?,?,?,datetime('now'))", (user, selected_contact, txt))
                    conn.commit(); st.rerun()

# ==========================================
# 5. صفحة السوق والعرض (ENHANCED MARKET)
# ==========================================
def show_market(conn):
    st.markdown("<h1 style='text-align:center; color:white;'>💎 سوق تيتانيوم الترا 2026</h1>", unsafe_allow_html=True)
    
    # فلترة متقدمة
    with st.expander("🔍 أدوات البحث المتقدم"):
        c1, c2, c3 = st.columns(3)
        search = c1.text_input("اسم المنتج...")
        cat = c2.selectbox("الفئة", ["الكل", "إلكترونيات", "عقارات", "سيارات", "خدمات"])
        wilaya = c3.selectbox("الولاية", ["الكل"] + [f"{i:02d}" for i in range(1, 59)])
    
    query = "SELECT * FROM ads WHERE status='active'"
    params = []
    if cat != "الكل": query += " AND category=?"; params.append(cat)
    if wilaya != "الكل": query += " AND wilaya=?"; params.append(wilaya)
    if search: query += " AND (product LIKE ? OR description LIKE ?)"; params.extend([f'%{search}%', f'%{search}%'])
    
    ads = conn.execute(query + " ORDER BY featured DESC, id DESC", params).fetchall()
    
    for ad in ads:
        with st.container():
            st.markdown(f"""
                <div class="ad-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="flex:2">
                            <h2 style="color:#006633; margin:0;">{ad[1]} {f'<span class="badge-premium">⭐ مميز</span>' if ad[9] else ''}</h2>
                            <p style="color:#555;">{ad[5][:150]}...</p>
                            <p>📍 {ad[4]} | 👤 {ad[7]} | 👁️ {ad[8]}</p>
                        </div>
                        <div style="flex:1; text-align:center;">
                            {f'<img src="data:image/png;base64,{ad[11]}" style="width:150px; border-radius:15px; margin-bottom:10px;">' if ad[11] and len(ad[11]) > 100 else ''}
                            <div class="price-tag">{ad[2]:,} دج</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            b1, b2, b3, b4 = st.columns(4)
            if b1.button("💬 مراسلة", key=f"m_{ad[0]}"):
                conn.execute("INSERT INTO messages(from_user, to_user, message, date) VALUES(?,?,?,datetime('now'))", (st.session_state.user, ad[7], f"بخصوص: {ad[1]}"))
                conn.commit(); st.success("تم فتح المحادثة!"); time.sleep(1); st.rerun()
            if b2.button("❤️ حفظ", key=f"f_{ad[0]}"):
                conn.execute("INSERT OR IGNORE INTO favorites(username, ad_id, saved_date) VALUES(?,?,datetime('now'))", (st.session_state.user, ad[0]))
                conn.commit(); st.toast("تم الحفظ!")
            if b3.button("📞 إظهار الهاتف", key=f"p_{ad[0]}"): st.info(f"رقم البائع: {ad[3]}")
            
            # AI Recommendations
            if AI_ENABLED:
                with st.expander("🔮 منتجات مشابهة قد تهمك"):
                    ai = AIEngine()
                    sim_ads = ai.get_similar_ads(ad[0])
                    for s in sim_ads: st.write(f"- {s[1]} (تصنيف: {s[3]})")

# ==========================================
# 6. نشر إعلان (LATEST WITH IMAGE UPLOAD)
# ==========================================
def post_ad(conn):
    st.header("📢 أنشئ إعلانك الاحترافي")
    ai = AIEngine()
    
    with st.form("ad_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        p_name = col1.text_input("اسم المنتج *")
        p_cat = col2.selectbox("التصنيف", ["إلكترونيات", "عقارات", "سيارات", "خدمات", "أخرى"])
        p_price = col1.number_input("السعر (دج)", min_value=0)
        p_wilaya = col2.selectbox("الولاية", [f"{i:02d}" for i in range(1, 59)])
        p_desc = st.text_area("وصف دقيق للمنتج")
        p_phone = st.text_input("رقم الهاتف للتواصل")
        p_img = st.file_uploader("ارفع صورة المنتج", type=['png', 'jpg', 'jpeg'])
        
        # توقع السعر
        if p_cat and p_wilaya:
            pred = ai.predict_price(p_cat, p_wilaya)
            if pred: st.info(f"💡 نصيحة تيتانيوم: متوسط سعر السوق لهذا النوع في ولايتك هو {pred['predicted']:,} دج")

        if st.form_submit_button("🚀 نشر الإعلان الآن"):
            img_str = get_image_base64(p_img) if p_img else ""
            conn.execute("""INSERT INTO ads(product, price, phone, wilaya, description, date, owner, category, images) 
                         VALUES(?,?,?,?,?,datetime('now'),?,?,?)""", 
                         (p_name, p_price, p_phone, p_wilaya, p_desc, st.session_state.user, p_cat, img_str))
            conn.commit()
            st.balloons(); st.success("تم النشر بنجاح!")

# ==========================================
# 7. لوحة التحكم والتشغيل (MAIN)
# ==========================================
def main():
    if "user" not in st.session_state: st.session_state.user = None
    conn = get_connection()
    
    if not st.session_state.user:
        # صفحة الدخول (كما في الكود الأصلي)
        st.markdown('<div class="main-header"><h1>🇩🇿 RASSIM DZ TITANIUM ULTRA</h1><p>الجيل القادم من التجارة الإلكترونية</p></div>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 عضوية جديدة"])
        with tab1:
            u = st.text_input("اسم المستخدم")
            p = st.text_input("كلمة السر", type="password")
            if st.button("دخول"):
                res = conn.execute("SELECT password, salt, role FROM users WHERE username=?", (u,)).fetchone()
                if res and res[0] == hashlib.pbkdf2_hmac('sha256', p.encode(), res[1].encode(), 100000).hex():
                    st.session_state.user = u
                    st.session_state.role = res[2]
                    st.rerun()
                else: st.error("بيانات خاطئة")
        with tab2:
            nu = st.text_input("اسم المستخدم الجديد")
            np = st.text_input("كلمة السر الجديدة", type="password")
            if st.button("تسجيل"):
                salt = secrets.token_hex(16)
                h = hashlib.pbkdf2_hmac('sha256', np.encode(), salt.encode(), 100000).hex()
                try:
                    conn.execute("INSERT INTO users(username, password, salt) VALUES(?,?,?)", (nu, h, salt))
                    conn.commit(); st.success("تم التسجيل!")
                except: st.error("الاسم موجود")
    else:
        # لوحة التحكم
        with st.sidebar:
            st.title(f"مرحباً {st.session_state.user}")
            unread = conn.execute("SELECT COUNT(*) FROM messages WHERE to_user=? AND read=0", (st.session_state.user,)).fetchone()[0]
            menu = st.radio("القائمة الرئيسية", ["🔍 السوق الذكي", "📢 نشر إعلان", f"📩 الرسائل ({unread})", "🤖 مساعد AI", "📊 الإحصائيات", "🚪 خروج"])
            
        if "السوق" in menu: show_market(conn)
        elif "نشر" in menu: post_ad(conn)
        elif "الرسائل" in menu: show_chat_system(conn)
        elif "AI" in menu:
            st.markdown('<div class="ai-suggestion">', unsafe_allow_html=True)
            st.header("🤖 مساعد RASSIM الذكي")
            ai = AIEngine()
            stats = ai.analyze_user_behavior(st.session_state.user)
            if stats: st.write(f"بناءً على تصفحك، أنت مهتم بـ: **{stats['favorite_category']}**")
            st.markdown('</div>', unsafe_allow_html=True)
        elif "الإحصائيات" in menu:
            st.header("📈 نبض السوق")
            data = conn.execute("SELECT category, COUNT(*) FROM ads GROUP BY category").fetchall()
            if data:
                fig = px.pie(names=[d[0] for d in data], values=[d[1] for d in data], title="توزيع الإعلانات")
                st.plotly_chart(fig)
        elif "خروج" in menu:
            st.session_state.user = None; st.rerun()

if __name__ == "__main__":
    main()
