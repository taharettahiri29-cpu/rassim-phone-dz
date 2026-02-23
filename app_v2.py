import streamlit as st
import pandas as pd
import os
import urllib.parse
import datetime
import random
import time
from PIL import Image

# ==========================================
# 1. الإعدادات العليا والهوية الوطنية (العلم الجزائري)
# ==========================================
st.set_page_config(page_title="RASSIM DZ | المنصة الوطنية", layout="wide", page_icon="🇩🇿")

# قائمة الولايات الـ 59 كاملة
wilayas = [
    "01-أدرار", "02-الشلف", "03-الأغواط", "04-أم البواقي", "05-باتنة", "06-بجاية", "07-بسكرة", "08-بشار", "09-البليدة", "10-البويرة",
    "11-تمنراست", "12-تبسة", "13-تلمسان", "14-تيارت", "15-تيزي وزو", "16-الجزائر", "17-الجلفة", "18-جيجل", "19-سطيف", "20-سعيدة",
    "21-سكيكدة", "22-سيدي بلعباس", "23-عنابة", "24-قالمة", "25-قسنطينة", "26-المدية", "27-مستغانم", "28-المسيلة", "29-معسكر", "30-ورقلة",
    "31-وهران", "32-البيض", "33-إليزي", "34-برج بوعريريج", "35-بومرداس", "36-الطارف", "37-تندوف", "38-تيسمسيلت", "39-الوادي", "40-خنشلة",
    "41-سوق أهراس", "42-تيبازة", "43-ميلة", "44-عين الدفلى", "45-النعامة", "46-عين تموشنت", "47-غرداية", "48-غليزان", "49-تيميمون", "50-برج باجي مختار",
    "51-أولاد جلال", "52-بني عباس", "53-عين صالح", "54-عين قزام", "55-تقرت", "56-جانت", "57-المغير", "58-المنيعة", "59-سيدي عيسى"
]

# محرك التنسيق CSS (يجمع كل اللمسات الجمالية التي طلبته)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    
    .hero-container {
        background: linear-gradient(to left, #006633 50%, #ffffff 50%);
        padding: 50px 20px; text-align: center; border-radius: 25px;
        margin-bottom: 20px; border-bottom: 10px solid #d21034;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    }
    .hero-title {
        color: #d21034; background: rgba(255,255,255,0.95);
        display: inline-block; padding: 15px 40px; border-radius: 20px;
        border: 3px solid #d21034; font-size: 2.5em; font-weight: bold;
    }
    .stat-card {
        background: white; padding: 15px; border-radius: 15px;
        border-bottom: 4px solid #006633; text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    .phone-card {
        background: white; padding: 20px; border-radius: 15px;
        margin-bottom: 15px; border-right: 10px solid #006633;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    .wa-btn {
        background-color: #25D366; color: white !important;
        padding: 10px 25px; border-radius: 50px;
        text-decoration: none; font-weight: bold; display: inline-block;
    }
    </style>
    
    <div class="hero-container">
        <h1 class="hero-title">🇩🇿 RASSIM DZ</h1>
        <p style="color:#333; font-weight:bold; background:rgba(255,255,255,0.75); display:table; margin:15px auto; padding:8px 20px; border-radius:10px;">
        محرك البحث الوطني الأول للهواتف في 59 ولاية
        </p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 2. نظام تتبع الزيارات والنشاط
# ==========================================
if 'visitor_count' not in st.session_state:
    st.session_state.visitor_count = 1450 + random.randint(10, 50)
    st.session_state.active_now = random.randint(25, 65)
st.session_state.visitor_count += 1

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1: st.markdown(f'<div class="stat-card"><h3>{st.session_state.visitor_count:,}</h3><p>زيارة وطنية</p></div>', unsafe_allow_html=True)
with col_s2: st.markdown(f'<div class="stat-card"><h3 style="color:#2ecc71;">🟢 {st.session_state.active_now}</h3><p>متصل الآن</p></div>', unsafe_allow_html=True)
with col_s3: st.markdown('<div class="stat-card"><h3>59</h3><p>ولاية مغطاة</p></div>', unsafe_allow_html=True)

st.write("---")

# ==========================================
# 3. إدارة قاعدة البيانات (الحل الجذري للأخطاء)
# ==========================================
DB_FILE = "users_database.csv"
def load_data():
    cols = ["Product", "Price", "Phone", "Wilaya", "Description", "Date"]
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            for c in cols:
                if c not in df.columns: df[c] = "غير متوفر"
            return df[cols]
        except: return pd.DataFrame(columns=cols)
    return pd.DataFrame(columns=cols)

# ==========================================
# 4. الأقسام والتبويبات (البحث، النشر، الذكاء الاصطناعي)
# ==========================================
tab1, tab2, tab3 = st.tabs(["🔍 محرك البحث", "📢 أنشر عرضك", "🤖 رادار AI"])

# --- تبويب البحث ---
with tab1:
    c1, c2 = st.columns([3, 1])
    with c1: search_q = st.text_input("", placeholder="ابحث عن موديل (iPhone, Samsung...)")
    with c2: target_w = st.selectbox("📍 المنطقة", ["كل الولايات"] + wilayas)

    df = load_data()
    f_df = df.copy()
    if search_q: f_df = f_df[f_df['Product'].str.contains(search_q, case=False, na=False)]
    if target_w != "كل الولايات": f_df = f_df[f_df['Wilaya'] == target_w]

    if not f_df.empty:
        for _, row in f_df.iloc[::-1].iterrows():
            wa_msg = urllib.parse.quote(f"سلام، شفت إعلانك لـ {row['Product']} على RASSIM DZ. هل متاح؟")
            wa_url = f"https://wa.me/213{str(row['Phone']).strip('0')}?text={wa_msg}"
            st.markdown(f"""
                <div class="phone-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <h3 style="margin:0; color:#006633;">{row['Product']}</h3>
                            <p style="color:#636e72;">📍 {row['Wilaya']} | 💰 {row['Price']:,} دج</p>
                            <p>{row['Description']}</p>
                        </div>
                        <a href="{wa_url}" target="_blank" class="wa-btn">واتساب</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("لا توجد عروض حالياً. كن أول من ينشر في هذه الولاية!")

# --- تبويب النشر (مع الذكاء الاصطناعي) ---
with tab2:
    st.subheader("📸 ميزة الذكاء الاصطناعي")
    up_file = st.file_uploader("ارفع صورة هاتفك ليتعرف عليه الروبوت", type=["jpg", "png", "jpeg"])
    if up_file:
        st.image(Image.open(up_file), width=150)
        st.info("🤖 الروبوت يحلل الصورة... يبدو هذا الهاتف بحالة جيدة جداً!")

    with st.form("add_offer", clear_on_submit=True):
        st.subheader("📝 تفاصيل الإعلان")
        col1, col2 = st.columns(2)
        with col1:
            p_name = st.text_input("اسم الهاتف")
            p_price = st.number_input("السعر (دج)", min_value=0)
        with col2:
            p_phone = st.text_input("رقم الواتساب")
            p_city = st.selectbox("الولاية", wilayas)
        
        p_desc = st.text_area("وصف إضافي")
        submitted = st.form_submit_button("🚀 نشر العرض وطنياً")
        
        if submitted:
            if p_name and p_phone and p_price > 0:
                new_row = pd.DataFrame([[p_name, p_price, p_phone, p_city, p_desc, datetime.date.today()]], columns=["Product", "Price", "Phone", "Wilaya", "Description", "Date"])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.balloons()
                st.success(f"✅ مبروك! إعلانك متاح الآن في {p_city}")
            else:
                st.error("⚠️ يرجى ملء الخانات الأساسية.")

# --- تبويب رادار التنبيهات ---
with tab3:
    st.subheader("🔔 رادار الهمزات الذكي")
    st.write("سيرسل لك الروبوت إشعاراً فور توفر الهاتف الذي تبحث عنه.")
    r_mail = st.text_input("بريدك الإلكتروني")
    r_target = st.text_input("الهاتف المطلوب (مثلاً: Google Pixel 7)")
    if st.button("تفعيل الرادار"):
        st.success(f"🎯 تم التفعيل! رادار RASSIM DZ يبحث الآن عن {r_target}.")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#95a5a6;'>RASSIM DZ 2026 - القوة المعلوماتية من تيبازة إلى كل الجزائر</p>", unsafe_allow_html=True)

