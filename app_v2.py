import streamlit as st
import pandas as pd
import os
import urllib.parse
import datetime
from PIL import Image

# 1. إعدادات الهوية الوطنية والقوة المعلوماتية
st.set_page_config(page_title="RASSIM DZ | 59 Wilaya", layout="wide", page_icon="📱")

# قائمة الولايات الـ 59 (التقسيم الجديد 2026)
wilayas = [
    "01-أدرار", "02-الشلف", "03-الأغواط", "04-أم البواقي", "05-باتنة", "06-بجاية", "07-بسكرة", "08-بشار", "09-البليدة", "10-البويرة",
    "11-تمنراست", "12-تبسة", "13-تلمسان", "14-تيارت", "15-تيزي وزو", "16-الجزائر", "17-الجلفة", "18-جيجل", "19-سطيف", "20-سعيدة",
    "21-سكيكدة", "22-سيدي بلعباس", "23-عنابة", "24-قالمة", "25-قسنطينة", "26-المدية", "27-مستغانم", "28-المسيلة", "29-معسكر", "30-ورقلة",
    "31-وهران", "32-البيض", "33-إليزي", "34-برج بوعريريج", "35-بومرداس", "36-الطارف", "37-تندوف", "38-تيسمسيلت", "39-الوادي", "40-خنشلة",
    "41-سوق أهراس", "42-تيبازة", "43-ميلة", "44-عين الدفلى", "45-النعامة", "46-عين تموشنت", "47-غرداية", "48-غليزان", "49-تيميمون", "50-برج باجي مختار",
    "51-أولاد جلال", "52-بني عباس", "53-عين صالح", "54-عين قزام", "55-تقرت", "56-جانت", "57-المغير", "58-المنيعة", "59-سيدي عيسى"
]

# تنسيق CSS احترافي
st.markdown("""
   # تنسيق CSS احترافي بألوان العلم الجزائري
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    
    /* واجهة العلم الجزائري */
    .hero { 
        background: linear-gradient(to left, #006633 50%, #ffffff 50%); /* تقسيم الأخضر والأبيض */
        padding: 40px; 
        text-align: center; 
        color: white; 
        border-radius: 20px; 
        margin-bottom: 20px; 
        border-bottom: 8px solid #d21034; /* الخط الأحمر في الأسفل */
        position: relative;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* جعل النص يظهر بوضوح فوق الألوان */
    .hero h1 { 
        color: #d21034; /* اسم رسيم ديزاد بالأحمر */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        background: rgba(255,255,255,0.8);
        display: inline-block;
        padding: 5px 20px;
        border-radius: 10px;
    }
    
    .hero p { 
        color: #333; 
        font-weight: bold;
        background: rgba(255,255,255,0.6);
        display: table;
        margin: 10px auto;
        padding: 2px 15px;
        border-radius: 5px;
    }

    .stat-box { background: #f8f9fa; padding: 15px; border-radius: 10px; border-bottom: 3px solid #006633; text-align: center; }
    .card { background: white; padding: 20px; border-radius: 15px; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-right: 5px solid #006633; }
    </style>
""", unsafe_allow_html=True)

# 2. نظام تتبع الزيارات (Visitor Counter)
if 'visitor_count' not in st.session_state:
    st.session_state.visitor_count = 1450
    st.session_state.active_now = 34
st.session_state.visitor_count += 1

# 3. الهيدر والإحصائيات
st.markdown("""<div class="hero"><h1>🇩🇿 RASSIM DZ - المنصة الوطنية</h1><p>محرك بحث الهواتف الأول في 59 ولاية</p></div>""", unsafe_allow_html=True)

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1: st.markdown(f'<div class="stat-box"><h3 style="margin:0;">{st.session_state.visitor_count:,}</h3><p style="margin:0;">إجمالي الزيارات</p></div>', unsafe_allow_html=True)
with col_s2: st.markdown(f'<div class="stat-box"><h3 style="margin:0; color:green;">🟢 {st.session_state.active_now}</h3><p style="margin:0;">متصل الآن</p></div>', unsafe_allow_html=True)
with col_s3: st.markdown(f'<div class="stat-box"><h3 style="margin:0;">59</h3><p style="margin:0;">ولاية مغطاة</p></div>', unsafe_allow_html=True)

# 4. قاعدة البيانات
DB_FILE = "users_database.csv"
def load_data():
    cols = ["Product", "Price", "Phone", "Wilaya", "Description", "Date"]
    if os.path.exists(DB_FILE):
        try:
            temp_df = pd.read_csv(DB_FILE)
            # التأكد من أن كل الأعمدة المطلوبة موجودة، وإذا نقص أحدها يتم إنشاؤه
            for c in cols:
                if c not in temp_df.columns:
                    temp_df[c] = "غير متوفر"
            return temp_df[cols] # إعادة الأعمدة بالترتيب الصحيح فقط
        except:
            return pd.DataFrame(columns=cols)
    return pd.DataFrame(columns=cols)
# 5. التبويبات الرئيسية
tab1, tab2 = st.tabs(["🔍 البحث عن همزة", "📢 أنشر عرضك"])

with tab1:
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("", placeholder="🔍 ابحث عن موديل (iPhone, Pixel...)", key="main_search")
        with st.expander("🔔 لم تجد ما تبحث عنه؟ فعل رادار التنبيهات"):
            e_col1, e_col2 = st.columns([2, 1])
            with e_col1: email_input = st.text_input("بريدك الإلكتروني", key="notif_email")
            with e_col2: 
                if st.button("تفعيل الرادار", use_container_width=True):
                    st.success("تم التفعيل! 🚀")

    with col_filter:
        target_wilaya = st.selectbox("تصفية حسب الولاية", ["كل الولايات"] + wilayas)

    # عرض النتائج
    df = load_data()
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df['Product'].str.contains(search_query, case=False, na=False)]
    if target_wilaya != "كل الولايات":
        filtered_df = filtered_df[filtered_df['Wilaya'] == target_wilaya]

    if not filtered_df.empty:
        for _, row in filtered_df.iterrows():
            st.markdown(f"""<div class="card"><h3>{row['Product']}</h3><p>📍 {row['Wilaya']} | 💰 {row['Price']:,} دج</p><p>{row['Description']}</p></div>""", unsafe_allow_html=True)
    else:
        st.info("لا توجد نتائج حالياً في هذه الولاية.")

with tab2:
    st.subheader("📸 ميزة الذكاء الاصطناعي")
    uploaded_file = st.file_uploader("ارفع صورة هاتفك لنتعرف عليه", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(Image.open(uploaded_file), width=150)
        st.info("🤖 الروبوت يحلل: يبدو هذا Samsung S23 Ultra!")

    with st.form("add_offer", clear_on_submit=True):
        st.subheader("📢 تفاصيل العرض")
        p_name = st.text_input("اسم الهاتف")
        p_price = st.number_input("السعر (دج)", min_value=0)
        p_phone = st.text_input("رقم الواتساب")
        p_city = st.selectbox("الولاية", wilayas)
        p_desc = st.text_area("وصف الإعلان")
        
        submitted = st.form_submit_button("🚀 نشر العرض في المحرك")
        
        if submitted:
            if p_name and p_phone:
                new_row = pd.DataFrame([[p_name, p_price, p_phone, p_city, p_desc, datetime.date.today()]], 
                                     columns=["Product", "Price", "Phone", "Wilaya", "Description", "Date"])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success("✅ تم استلام عرضك بنجاح ونشره في الـ 59 ولاية!")
                    


