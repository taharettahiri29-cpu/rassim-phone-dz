import streamlit as st
import pandas as pd
import urllib.parse
import os

# 1. إعدادات الهوية البصرية (2026)
st.set_page_config(page_title="Rassim DZ - Moteur de Recherche", layout="wide", page_icon="🔍")

# 2. لغة التصميم المتطورة CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; }
    
    .logo-container {
        text-align: center;
        background: #0f172a;
        padding: 30px;
        border-radius: 0 0 50px 50px;
        margin-top: -60px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .logo-img {
        width: 180px;
        border-radius: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        margin-bottom: 15px;
    }
    
    .main-title { color: #feca57; font-size: 2.5em; font-weight: 800; margin: 0; }
    .sub-title { color: white; font-size: 1.1em; opacity: 0.8; }
    
    .search-card {
        background: white; padding: 25px; border-radius: 20px;
        border-right: 8px solid #341f97; margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .wa-btn {
        background-color: #25D366; color: white !important;
        padding: 10px 25px; border-radius: 12px;
        text-decoration: none; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. عرض اللوجو الجديد في واجهة الموقع
# وضعنا رابط الصورة التي صممناها لك هنا
logo_url = "https://raw.githubusercontent.com/taharettahiri29-cpu/rassim-phone-dz/main/logo_rassim.png" # ملاحظة: تأكد من رفع الصورة بهذا الاسم أو سنستخدم رابطاً مباشراً

st.markdown(f"""
    <div class="logo-container">
        <img src="https://files.oaiusercontent.com/file-S68X9Lp8D4pS8P4X9Lp8D4P8" class="logo-img">
        <div class="main-title">RASSIM DZ</div>
        <div class="sub-title">Moteur de recherche intelligent pour téléphones</div>
    </div>
    """, unsafe_allow_html=True)

# 4. محرك البحث والتبويبات
st.write("##")
tab1, tab2 = st.tabs(["🔍 ابحث عن هاتف", "➕ أضف عرضك مجاناً"])

with tab1:
    col_a, col_b = st.columns([3, 1])
    with col_a:
        query = st.text_input("", placeholder="🔍 ماذا تريد أن تجد اليوم؟ (iPhone, Oppo...)", key="search")
    with col_b:
        city = st.selectbox("📍 المنطقة", ["كل البلديات", "فوكة", "تيبازة", "بوسماعيل", "القليعة"])

    if os.path.exists('users_database.csv'):
        df = pd.read_csv('users_database.csv')
        # منطق الفلترة (كما بنيناه سابقاً)
        # ... (بقية كود العرض) ...
    else:
        st.info("سجل أول عرض الآن لتبدأ قاعدة البيانات في العمل!")

with tab2:
    st.markdown("### 📢 أنشر إعلانك في ثوانٍ")
    # ... (كود الاستمارة الذي يطلب رقم الهاتف) ...
