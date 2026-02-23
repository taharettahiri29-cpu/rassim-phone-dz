import streamlit as st
import pandas as pd
import os
import urllib.parse
import datetime
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="RASSIM DZ | 59 Wilaya", layout="wide", page_icon="🇩🇿")

# 2. الهوية البصرية (العلم الجزائري) - تأكد من نسخ هذا الجزء كما هو
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    
    .hero-container {
        background: linear-gradient(to left, #006633 50%, #ffffff 50%);
        padding: 50px 20px;
        text-align: center;
        border-radius: 25px;
        margin-bottom: 25px;
        border-bottom: 10px solid #d21034;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    }
    
    .hero-title {
        color: #d21034;
        background: rgba(255,255,255,0.95);
        display: inline-block;
        padding: 15px 40px;
        border-radius: 20px;
        border: 3px solid #d21034;
        font-size: 2.5em;
        font-weight: bold;
    }
    
    .hero-subtitle {
        color: #1a1a1a;
        background: rgba(255,255,255,0.8);
        display: table;
        margin: 15px auto;
        padding: 8px 20px;
        border-radius: 10px;
    }
    .card { background: white; padding: 20px; border-radius: 15px; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-right: 5px solid #006633; }
    </style>
    
    <div class="hero-container">
        <h1 class="hero-title">🇩🇿 RASSIM DZ</h1>
        <p class="hero-subtitle">المنصة الوطنية الأولى لتداول الهواتف في 59 ولاية</p>
    </div>
""", unsafe_allow_html=True)

# 3. قائمة الولايات الـ 59
wilayas = [
    "01-أدرار", "02-الشلف", "03-الأغواط", "04-أم البواقي", "05-باتنة", "06-بجاية", "07-بسكرة", "08-بشار", "09-البليدة", "10-البويرة",
    "11-تمنراست", "12-تبسة", "13-تلمسان", "14-تيارت", "15-تيزي وزو", "16-الجزائر", "17-الجلفة", "18-جيجل", "19-سطيف", "20-سعيدة",
    "21-سكيكدة", "22-سيدي بلعباس", "23-عنابة", "24-قالمة", "25-قسنطينة", "26-المدية", "27-مستغانم", "28-المسيلة", "29-معسكر", "30-ورقلة",
    "31-وهران", "32-البيض", "33-إليزي", "34-برج بوعريريج", "35-بومرداس", "36-الطارف", "37-تندوف", "38-تيسمسيلت", "39-الوادي", "40-خنشلة",
    "41-سوق أهراس", "42-تيبازة", "43-ميلة", "44-عين الدفلى", "45-النعامة", "46-عين تموشنت", "47-غرداية", "48-غليزان", "49-تيميمون", "50-برج باجي مختار",
    "51-أولاد جلال", "52-بني عباس", "53-عين صالح", "54-عين قزام", "55-تقرت", "56-جانت", "57-المغير", "58-المنيعة", "59-سيدي عيسى"
]

# 4. وظائف البيانات
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

# 5. التبويبات (هنا ستعود المعلومات للظهور)
tab1, tab2 = st.tabs(["🔍 البحث عن هاتف", "📢 أنشر إعلانك"])

with tab1:
    search_query = st.text_input("🔍 ابحث عن موديل...", placeholder="مثال: iPhone 13")
    target_wilaya = st.selectbox("📍 اختر الولاية", ["كل الولايات"] + wilayas)
    
    df = load_data()
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df['Product'].str.contains(search_query, case=False, na=False)]
    if target_wilaya != "كل الولايات":
        filtered_df = filtered_df[filtered_df['Wilaya'] == target_wilaya]

    if not filtered_df.empty:
        for _, row in filtered_df.iterrows():
            st.markdown(f"""<div class="card"><h3>{row['Product']}</h3><p>💰 {row['Price']:,} دج | 📍 {row['Wilaya']}</p></div>""", unsafe_allow_html=True)
    else:
        st.info("لا توجد عروض حالياً.")

with tab2:
    with st.form("add_new"):
        name = st.text_input("اسم الهاتف")
        price = st.number_input("السعر", min_value=0)
        phone = st.text_input("رقم الهاتف")
        city = st.selectbox("الولاية", wilayas)
        desc = st.text_area("الوصف")
        submit = st.form_submit_button("🚀 نشر الإعلان")
        
        if submit and name and phone:
            new_data = pd.DataFrame([[name, price, phone, city, desc, datetime.date.today()]], columns=["Product", "Price", "Phone", "Wilaya", "Description", "Date"])
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("تم النشر!")
