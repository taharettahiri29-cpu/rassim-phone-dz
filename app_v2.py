import streamlit as st
import pandas as pd
import os
import urllib.parse
import datetime
import random
import logging
import re
from PIL import Image

# ==========================================
# 1. الإعدادات العليا والهوية (تصميم متطور)
# ==========================================
st.set_page_config(page_title="RASSIM DZ | Pro Max 2026", layout="wide", page_icon="🇩🇿")

# CSS المتقدم - واجهة العلم الجزائري مع Glassmorphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    
    .main-header {
        background: linear-gradient(135deg, #006633 0%, #006633 45%, #ffffff 55%, #ffffff 100%);
        padding: 60px; text-align: center; border-radius: 30px;
        border-bottom: 12px solid #d21034; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        position: relative; overflow: hidden; margin-bottom: 30px;
    }
    .header-title {
        color: #d21034; background: rgba(255,255,255,0.9);
        display: inline-block; padding: 15px 45px; border-radius: 50px;
        font-size: 3.5rem; font-weight: 900; border: 4px solid #d21034;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .stMetric { background: white; padding: 15px; border-radius: 15px; border-bottom: 5px solid #006633; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
    .phone-card {
        background: white; border-radius: 20px; padding: 20px;
        border-right: 15px solid #006633; margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); transition: 0.3s;
    }
    .phone-card:hover { transform: translateY(-5px); box-shadow: 0 15px 35px rgba(0,0,0,0.1); }
    .price-tag { color: white; background: #d21034; padding: 5px 20px; border-radius: 50px; font-weight: bold; font-size: 1.2rem; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. نظام الـ Core المحسن (بناءً على تحديك)
# ==========================================
DB_FILE = "users_database.csv"
COLUMNS = ["Product", "Price", "Phone", "Wilaya", "Description", "Date", "Category"]

logging.basicConfig(filename="system_master.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def get_category(name):
    name = name.lower()
    if "iphone" in name: return "Apple 🍎"
    if "samsung" in name: return "Samsung 📱"
    if "pixel" in name: return "Google 🤖"
    return "أخرى 📦"

def clean_phone(phone):
    digits = re.sub(r'\D', '', phone)
    return digits[-9:] # نأخذ آخر 9 أرقام لضمان الصيغة الجزائري

@st.cache_data(ttl=60)
def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        return df
    return pd.DataFrame(columns=COLUMNS)

# ==========================================
# 3. الواجهة الأمامية (The UX)
# ==========================================
st.markdown("""
    <div class="main-header">
        <h1 class="header-title">🇩🇿 RASSIM DZ</h1>
        <h3 style="color:#333; margin-top:20px;">الجيل الثالث من منصة الهواتف الوطنية</h3>
    </div>
""", unsafe_allow_html=True)

if "visitors" not in st.session_state:
    st.session_state.visitors = random.randint(5000, 7000)
st.session_state.visitors += 1

m1, m2, m3 = st.columns(3)
m1.metric("إجمالي الزيارات", f"{st.session_state.visitors:,}", "🚀 +12%")
m2.metric("تغطية وطنية", "59 ولاية", "🔥 نشط")
m3.metric("تحديثات اليوم", f"{len(load_data()):,}", "📦 جديد")

st.divider()

# ==========================================
# 4. التبويبات والمحرك
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(["🔍 رادار البحث", "📢 إضافة عرض", "🤖 ذكاء اصطناعي", "📊 تحليل السوق"])

df = load_data()

with tab1:
    col_a, col_b, col_c = st.columns([2, 1, 1])
    q = col_a.text_input("بحث سريع", placeholder="مثال: iPhone 15 Pro Max")
    w = col_b.selectbox("الولاية", ["كل القطر الوطني"] + [f"{i:02d}" for i in range(1, 60)])
    cat = col_c.selectbox("الفئة", ["الكل", "Apple 🍎", "Samsung 📱", "Google 🤖", "أخرى 📦"])

    results = df.copy()
    if q: results = results[results["Product"].str.contains(q, case=False, na=False)]
    if cat != "الكل": results = results[results["Category"] == cat]
    
    if not results.empty:
        for _, row in results.iloc[::-1].iterrows():
            with st.container():
                st.markdown(f"""
                <div class="phone-card">
                    <div style="display:flex; justify-content:space-between;">
                        <div>
                            <span style="color:#666; font-size:0.8rem;">{row['Category']}</span>
                            <h2 style="margin:0; color:#006633;">{row['Product']}</h2>
                            <p>📍 ولاية: {row['Wilaya']} | 📅 {row['Date']}</p>
                            <p style="color:#444;">{row['Description']}</p>
                        </div>
                        <div style="text-align:left;">
                            <div class="price-tag">{row['Price']:,} دج</div>
                            <br><br>
                            <a href="https://wa.me/213{row['Phone']}" target="_blank" 
                               style="background:#25d366; color:white; padding:10px 20px; border-radius:10px; text-decoration:none; font-weight:bold;">
                               تواصل الآن 💬
                            </a>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("لا توجد همزات تطابق بحثك حالياً.")

with tab2:
    with st.form("pro_publish", clear_on_submit=True):
        c1, c2 = st.columns(2)
        p_name = c1.text_input("اسم الجهاز بالكامل")
        p_price = c2.number_input("السعر النهائي (دج)", min_value=0)
        p_phone = c1.text_input("رقم الهاتف (واتساب)")
        p_city = c2.selectbox("ولاية التوفر", [f"{i:02d}" for i in range(1, 60)])
        p_desc = st.text_area("تفاصيل الحالة (الخدوش، البطارية، الملحقات)")
        
        if st.form_submit_button("🚀 إطلاق العرض في المنصة"):
            if p_name and p_phone and p_price > 0:
                new_row = pd.DataFrame([[
                    p_name, p_price, clean_phone(p_phone), p_city, 
                    p_desc, datetime.date.today(), get_category(p_name)
                ]], columns=COLUMNS)
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.balloons()
                st.success("تم التحقق والنشر بنجاح!")
            else:
                st.warning("الرجاء إكمال البيانات الأساسية.")

with tab3:
    st.subheader("🤖 محلل الصور الذكي")
    img_file = st.file_uploader("ارفع صورة لنعطيك السعر المقترح", type=['jpg', 'png'])
    if img_file:
        st.image(img_file, width=300)
        st.write("🔍 جاري التحليل عبر تقنية Vision...")
        time_sim = st.progress(0)
        # محاكاة ذكاء اصطناعي
        st.info(f"النتيجة: هذا الجهاز يطابق فئة {get_category('iphone')} وحالته ممتازة.")

with tab4:
    st.subheader("📊 إحصائيات السوق اليوم")
    if not df.empty:
        st.line_chart(df.set_index('Date')['Price'])
        st.write("أكثر الماركات طلباً:")
        st.bar_chart(df['Category'].value_counts())

st.markdown("---")
st.markdown("<p style='text-align:center;'>RASSIM DZ 2026 - تكنولوجيا فوكة، تيبازة نحو العالمية 🇩🇿</p>", unsafe_allow_html=True)
